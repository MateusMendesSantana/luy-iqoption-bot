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
from strategies.patter_m1 import PatternM1
from risk_management.b import B
import configuration as config
import math
from promise import Promise
from active import Active
from api.buy import Buy
from api.dispacher import Dispacher
from api.operation_info import OperationInfo
from api.list_info_data import ListInfoData
from api.timesync import TimeSync
from risk_management.matingale import Martingale

class Bot(Thread):

    def __init__(self, profile, api, dispacher: Dispacher, timesync: TimeSync, active: Active, check_in_period=.2):
        self.buy = Buy(api.api, dispacher, timesync)
        self.operation_info = OperationInfo(api.api, dispacher, timesync)
        self.list_info_data = ListInfoData(api.api, dispacher, timesync)
        self.profile = profile
        self.api = api
        self.active = active
        self.candle_size = config.CANDLE_SIZE
        self.max_candles = config.MAX_CANDLES
        self.check_in_period = check_in_period
        # self.risk_management: B = B()
        self.risk_management: Martingale = Martingale()
        self.do_stop = False

        self.check_time = time.time()

        self.id_number = None
        self.last_buy = 0

        # self.chart = CandleChart(active.name, 10)

        self.graphic_analysis = GraphicAnalysis()
        # dark_cloud = DarkCloud(active, self.graphic_analysis)
        # hammer = Hammer(active, self.graphic_analysis)
        # otc100 = Otc100(api, active, self.graphic_analysis)
        first_otc = FirstOtc(api, active, self.graphic_analysis)
        # simple_rsi = SimpleRSI(api, active, self.graphic_analysis)
        # second_otc = SecondOtc(api, active, self.graphic_analysis)
        # rsi_stoch = RSIStoch(api, active, self.graphic_analysis)
        # petternM1 = PatternM1(api, active, self.graphic_analysis)

        self.strategies = []
        # self.strategies.append(dark_cloud)
        # self.strategies.append(hammer)
        # self.strategies.append(otc100)
        self.strategies.append(first_otc)
        # self.strategies.append(second_otc)
        # self.strategies.append(simple_rsi)
        # self.strategies.append(rsi_stoch)
        # self.strategies.append(petternM1)

        print('Robo {} criado.'.format(active.name))
        super(Bot, self).__init__()

    def run(self):
        while not self.do_stop:
            time.sleep(self.check_in_period)

            if not self.active.enabled or not self.active.is_profitable():
                self.stop()
            else:
                self.check()

        self.stop_stream()
        print('Stop Robot {}, {}'.format(self.active.name, self.active.enabled))

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
            check, result = self.buy(money, self.active.code, action)

            message = self.get_buy_message(check, action, money)
            print(message)

            if(check):
                self.last_buy = time.time()
                self.check_win()

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

    def get_buy_message(self, success, action, money):
        message = '{} to buy {}, action {}, money ${}'
        status = 'success' if success else 'failed'

        return message.format(status, self.active.name, action, money)

    def stop_stream(self):
        try:
            self.api.stop_candles_stream(self.active.name, config.CANDLE_SIZE)
        except:
            pass

    def check_win(self):
        result = self.list_info_data(self.buy.id)
        
        if result != None:
            if result == 'win':
                self.risk_management.add_win()
            elif result == 'loose':
                self.risk_management.add_loose()

            print('{} operation {}: {}'.format(result, self.active.name, self.buy.id))
        else:
            print('error {}({}) was not possible to verify status'.format(self.active.name, self.buy.id))

    def stop(self):
        self.do_stop = True


