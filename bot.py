import time
import logging
import json
import random
import configuration as config
from statistics import median, mean
from iqoptionapi.stable_api import IQ_Option
from stream import Stream
from threading import Thread
from graphic_analysis import GraphicAnalysis
from strategies.dark_cloud import DarkCloud
from collections import namedtuple
from candle import Candle
from strategies.hammer import Hammer
from strategies.only_otc import Otc100
from strategies.first_otc import FirstOtc
from strategies.second_otc import SecondOtc
from candle_chart import CandleChart
from strategies.simple_rsi import SimpleRSI
from strategies.rsi_stoch import RSIStoch
from risk_management.b import B
import configuration as config
import math
from promise import Promise
from active import Active
from api.buy import Buy
from api.dispacher import Dispacher

class Bot(Thread):

    def __init__(self, profile, api, dispacher: Dispacher, active: Active, check_in_period=.2):
        self.buy = Buy(api.api, dispacher)
        self.profile = profile
        self.api = api
        self.active = active
        self.candle_size = config.CANDLE_SIZE
        self.max_candles = config.MAX_CANDLES
        self.check_in_period = check_in_period
        self.risk_management: B = B()
        self.do_stop = False

        self.check_time = time.time()
        self.check_win_time = time.time()

        self.id_number = None
        self.last_buy = 0

        # self.chart = CandleChart(active.name, 10)

        self.graphic_analysis = GraphicAnalysis()
        # dark_cloud = DarkCloud(active, self.graphic_analysis)
        # hammer = Hammer(active, self.graphic_analysis)
        # otc100 = Otc100(api, active, self.graphic_analysis)
        # first_otc = FirstOtc(api, active, self.graphic_analysis)
        # simple_rsi = SimpleRSI(api, active, self.graphic_analysis)
        # second_otc = SecondOtc(api, active, self.graphic_analysis)
        rsi_stoch = RSIStoch(api, active, self.graphic_analysis)

        self.strategies = []
        # self.strategies.append(dark_cloud)
        # self.strategies.append(hammer)
        # self.strategies.append(otc100)
        # self.strategies.append(first_otc)
        # self.strategies.append(second_otc)
        # self.strategies.append(simple_rsi)
        self.strategies.append(rsi_stoch)

        print('Robo {} criado.'.format(active.name))
        super(Bot, self).__init__()

    def run(self):
        while not self.do_stop:
            if time.time() >= self.check_time:
                self.check_time = time.time() + self.check_in_period

                if not self.active.enabled or not self.active.is_profitable():
                    self.stop()
                elif not self.in_buy():
                    if self.id_number:
                        if time.time() > self.check_win_time:
                            self.check_win_time = time.time() + 1
                            self.check_win(self.id_number)
                    else:
                        self.check()

        self.stop_stream()
        print('Stop Robot {}, {}'.format(self.active.name, self.active.enabled))

    def in_buy(self):
        return time.time() < self.last_buy + config.OPERATION_TIME

    def check(self):
        candles = self.get_candles()
        # self.chart.setCandles(candles)
        self.graphic_analysis.set_candles(candles)
        probability = self.analize_strategies()

        if(abs(probability) >= config.OPERATION_WHEN_WIN):
            # balance = self.profile.get_balance()
            self.profile.refresh_actives()
            # operation_money = max(balance * config.OPERATION_MONEY, 1)
            entry = self.risk_management.get_next_entry(self.active.profit)
            money = max(config.OPERATION_MONEY * entry, 1)
            action = 'call' if probability > 0 else 'put'
            promise: Promise = self.do_buy(money, action)

            promise.then(self.on_sucess_buy)
            promise.catch(self.on_failed_buy)


    def get_candles(self):
        candles: list = self.api.get_realtime_candles(
            self.active.name, self.candle_size)

        return list(map(lambda key: Candle(candles[key]), candles))

    def analize_strategies(self):
        probabilities = list(map((lambda x: x.analize()), self.strategies))
        probabilities = list(filter((lambda x: x != 0), probabilities))

        if(len(probabilities) == 0):
            return 0
        else:
            return mean(probabilities)

    def do_buy(self, money, action, expirations_mode=1):
        self.last_buy = time.time()
        return self.buy(money, self.active.code, action, expirations_mode)

    def on_sucess_buy(self, result: dict):
        self.last_buy = time.time()
        print(self.get_buy_message('success', self.active.name, result['action'], result['money']))

    def on_failed_buy(self):
        print(self.get_buy_message('success', self.active.name, '', ''))

    def get_buy_message(self, status, active_name, action, money):
        message = '{} to buy {}, action {}, money ${}'

        return message.format(status, active_name, action, money)

    def stop_stream(self):
        try:
            self.api.stop_candles_stream(self.active.name, config.CANDLE_SIZE)
        except:
            return

    def check_win(self, id_number):
        if id_number in self.api.api.listinfodata.listinfodata_dict:
            listinfodata_dict = self.api.api.listinfodata.get(id_number)

            if listinfodata_dict["game_state"] == 1:
                self.api.api.listinfodata.delete(id_number)
                ans = listinfodata_dict["win"] # win loose equal

                if(ans):
                    if ans == 'win':
                        self.risk_management.add_win()
                    elif ans == 'loose':
                        self.risk_management.add_loose()

                    print('{} operation {}: {}'.format(ans, self.active.name, self.id_number))
                    self.id_number = None
                else:
                    print('error {}({}) was not possible to verify win'.format(self.active.name, self.id_number))
                    self.id_number = None
    
    def stop(self):
        self.do_stop = True


