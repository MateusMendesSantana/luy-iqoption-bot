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


class RSIStoch:
    def __init__(self, api: IQ_Option, active: Active, graphic_analysis: GraphicAnalysis):
        self.api = api
        self.active = active
        self.graphic_analysis = graphic_analysis

    def analize(self) -> float:
        purchase_time = 60 - ((time.time() + 30) % 60)

        if (purchase_time <= 10):
            candles = self.graphic_analysis.candles

            rev = list(reversed(candles))

            if(rev[0].is_doji() or rev[1].is_doji() or rev[2].is_doji() or rev[3].is_doji()):
                return 0

            # open = array(list(map(lambda x: x.open, candles)))
            close = array(list(map(lambda x: x.close, candles)))
            high = array(list(map(lambda x: x.max, candles)))
            low = array(list(map(lambda x: x.min, candles)))
            # volume = array(list(map(lambda x: x.volume, candles)))

            rsi = list(reversed(ta.RSI(close, timeperiod=2)))
            slowk, slowd = ta.STOCH(high, low, close, fastk_period=3, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
            slowk = list(reversed(slowk))
            slowd = list(reversed(slowd))

            if (rsi[0] > 95 and slowk[0] > 80 and slowd[0] > 80):
                return -1
            if (rsi[0] < 5 and slowk[0] < 20 and slowd[0] < 20):
                return 1

        return 0

