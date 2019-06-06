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


class SimpleRSI:
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

            rsi_real = ta.RSI(close, timeperiod=8)
            last_position = rsi_real[len(rsi_real)-1]
            penultimate_position = rsi_real[len(rsi_real)-2]

            if (penultimate_position > 80 and last_position < 75):
                return -1
            if (penultimate_position < 20 and last_position > 25):
                return 1

        return 0

