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


class SecondOtc:
    def __init__(self, api: IQ_Option, active: Active, graphic_analysis: GraphicAnalysis):
        self.api = api
        self.active = active
        self.graphic_analysis = graphic_analysis

    def analize(self) -> float:
        isOtc = self.active.name.endswith('OTC')

        if (isOtc):
            candles = self.graphic_analysis.candles
            # open = array(list(map(lambda x: x.open, candles)))
            close = array(list(map(lambda x: x.close, candles)))
            high = array(list(map(lambda x: x.max, candles)))
            low = array(list(map(lambda x: x.min, candles)))
            # volume = array(list(map(lambda x: x.volume, candles)))

            rsi_real = ta.RSI(close, timeperiod=18)
            cci_real = ta.CCI(high, low, close, timeperiod=18)
            rsi = [
                rsi_real[len(rsi_real)-1],
                rsi_real[len(rsi_real)-2],
                rsi_real[len(rsi_real)-3]
            ]
            cci = [
                cci_real[len(cci_real)-1],
                cci_real[len(cci_real)-2],
                cci_real[len(cci_real)-3]
            ]

            if (rsi[0] > 70 and cci[0] > 110 and cci[2] < 110):
                return -1
            if (rsi[0] < 30 and cci[0] < -110 and cci[2] > -110):
                return 1

        return 0

