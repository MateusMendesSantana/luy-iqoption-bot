import time
import logging
import json
import random
import configuration as config
from iqoptionapi.stable_api import IQ_Option
import iqoptionapi.constants as OP_code
from operator import itemgetter, attrgetter, methodcaller
import configuration as config
from bot import Bot
from active import Active
from api.dispacher import Dispacher
from api.timesync import TimeSync
import threading


class Start:
    def __init__(self):
        self.api = IQ_Option(config.USERNAME, config.PASSWORD)
        self.dispacher = Dispacher(self.api.api)
        self.api.change_balance(config.MODE)
        self.timesync = TimeSync(self.api, self.dispacher)
        self.bots = []
        self.actives = []
        
        self.generate_actives()
        self.create_bots()

        while True:
            if self.timesync.is_desconected():
                self.stop_bots()
                print('disconnected trying to reconnect in {} seconds'.format(config.TIME_RECONNECT))
                time.sleep(config.TIME_RECONNECT)

                if(self.reconnect()):
                    print('successfully reconnected')
                    self.create_bots()

            time.sleep(.3)

    def stop_bots(self):
        for bot in self.bots:
            if bot:
                bot.stop()

    def create_bots(self):
        self.bots = []
        actives = self.get_operable_actives()
        
        for index, active in enumerate(actives):
            if index >= config.MAX_BOTS:
                break

            self.api.start_candles_stream(active.name, config.CANDLE_SIZE, config.MAX_CANDLES)
            bot = Bot(self, self.api, self.dispacher, self.timesync, active)
            self.bots.append(bot)
            bot.start()

    def get_balance(self):
        while True:
            try:
                respon = self.api.get_profile()

                if(respon["isSuccessful"] == True):
                    return respon["result"]["balance"]
            except:
                self.reconnect()
      
            time.sleep(.5)

    def get_operable_actives(self) -> list:
        f = lambda active : active.enabled and active.is_profitable()
        return list(filter(f, self.actives))

    def refresh_actives(self):
        if time.time() > self.last_refresh_actives + 60:
            self.last_refresh_actives = time.time()
            check, init_info = self.get_all_init()

            if check:
                actives = init_info['turbo']['actives']

                for active in self.actives:
                    active.set_data(actives[str(active.code)])

                self.sort_actives()

    def generate_actives(self):
        self.last_refresh_actives = time.time()
        init_info: dict = self.api.get_all_init().get('result')
        actives = init_info['turbo']['actives']
        self.actives = list(map(lambda code: Active(actives[code]), actives))
        
        self.sort_actives()

    def sort_actives(self):
        self.actives = sorted(self.actives, key=attrgetter('profit'), reverse=True)

    def reconnect(self):
        try:
            self.api.api.close()
            result = self.api.api.connect()
            self.api.api.websocket.on_message = self.dispacher.on_message
            return result
        except:
            print('fail to reconnect')

    def check_win(self, id_number):
        try:
            check, data = self.api.api.get_betinfo(id_number)
        except:
            return False, None

        result = None
        
        if(check):
            result = data["result"]["data"][str(id_number)]["win"]

        return check, result

    def start_candles_stream(self, ACTIVE, size, maxdict):
        if size in self.api.size:
            self.api.api.real_time_candles_maxdict_table[ACTIVE][size] = maxdict
            self.api.full_realtime_get_candle(ACTIVE,size,maxdict)
            self.api.start_candles_one_stream(ACTIVE,size)
        else:
            logging.error('**error** start_candles_stream please input right size')

    def get_all_init(self):
        self.api.api.api_option_init_all_result = None
        try:
            self.api.api.get_api_option_init_all()
        except:
            return False, None
        start = time.time()
        while True:
            if time.time() - start > 30 or self.api.api.api_option_init_all_result != None:
                break
        try:
            if self.api.api.api_option_init_all_result['isSuccessful']:
                return True, self.api.api.api_option_init_all_result['result']
        except:
            return False, None

    def buy(self, price, active, action, expirations):
        api = self.api.api
        api.buy_successful == None
        buy_call = api.buy
        buy_call(price, OP_code.ACTIVES[active], action, expirations)
        start = time.time()
        while api.buy_successful == None or api.buy_id == None:
            if time.time() - start > 60:
                return False, None
        if api.buy_id:
            return True, api.buy_id
        else:
            return False, None


if __name__ == "__main__":
    global start
    start = Start()
