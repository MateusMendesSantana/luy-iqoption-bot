import time
import logging
import json
import random
import configuration as config
from iqoptionapi.stable_api import IQ_Option
import iqoptionapi.constants as OP_code
from operator import itemgetter, attrgetter, methodcaller
import configuration as config
from active import Active
from api.dispacher import Dispacher
from api.timesync import TimeSync
from candle import Candle
import threading


class Analize:
    def __init__(self):
        self.api = IQ_Option(config.USERNAME, config.PASSWORD)
        self.dispacher = Dispacher(self.api.api)
        self.api.change_balance(config.MODE)
        self.timesync = TimeSync(self.api, self.dispacher)
        self.actives = []
        
        self.generate_actives()

        acts: list = self.get_operable_actives()

        for index, active in enumerate(acts):
            candles: list = list(reversed(self.api.api.getcandles(active.code, 1, 10000, time.time())))

            for index, candle in candles:
                if index < len(candles) - 10:
                    candle: Candle = candle
                    
                    win = 0
                    losses = 0

                    if candles[index + 1].direction + candles[index + 2].direction + candles[index + 3].direction
                        pass




    def get_balance(self):
        while True:
            try:
                respon = self.api.get_profile()

                if(respon["isSuccessful"] == True):
                    return respon["result"]["balance"]
            except:
                pass
      
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


if __name__ == "__main__":
    global analize
    analize = Analize()
