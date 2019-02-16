# Minha primeira estrategia OTC
from trend import Trend
from iqoptionapi.stable_api import IQ_Option
from graphic_analysis import GraphicAnalysis
from candle import Candle
from numpy import array
from active import Active
import talib as ta
import numpy as np
import time
import math


class FirstOtc:
    def __init__(self, api: IQ_Option, active: Active, graphic_analysis: GraphicAnalysis):
        self.api = api
        self.active = active
        self.graphic_analysis = graphic_analysis

    def analize(self) -> float:
        isOtc = self.active.name.endswith('OTC')

        if (isOtc or True):
            candles = self.graphic_analysis.candles
            # open = array(list(map(lambda x: x.open, candles)))
            close = array(list(map(lambda x: x.close, candles)))
            high = array(list(map(lambda x: x.max, candles)))
            low = array(list(map(lambda x: x.min, candles)))
            # volume = array(list(map(lambda x: x.volume, candles)))

            rsi: list = ta.RSI(close, timeperiod=4).reverse()
            cci: list = ta.CCI(high, low, close, timeperiod=4).reverse()

            if (rsi[0] > 90 and cci[0] > 100):
                return -1
            if (rsi[0] < 10 and cci[0] < -100):
                return 1

        return 0

