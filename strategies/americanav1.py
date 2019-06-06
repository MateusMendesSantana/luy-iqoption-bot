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
from talib import MA_Type


class AmericanaV1:
    def __init__(self, api: IQ_Option, active: Active, graphic_analysis: GraphicAnalysis):
        self.api = api
        self.active = active
        self.graphic_analysis = graphic_analysis

    def analize(self) -> float:
        purchase_time = 60 - ((time.time() + 30) % 60)

        if (purchase_time <= 8):
            candles = self.graphic_analysis.candles

            rev = list(reversed(candles))

            if(rev[0].is_doji() or rev[1].is_doji() or rev[2].is_doji() or rev[3].is_doji()):
                return 0

            # open = array(list(map(lambda x: x.open, candles)))
            close = array(list(map(lambda x: x.close, candles)))
            high = array(list(map(lambda x: x.max, candles)))
            low = array(list(map(lambda x: x.min, candles)))
            # volume = array(list(map(lambda x: x.volume, candles)))

            upper, middle, lower = ta.BBANDS(close, timeperiod=19, nbdevup=2, nbdevdn=2, matype=0)
            slowk, slowd = ta.STOCH(high, low, close, fastk_period=19, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
            slowk = list(reversed(slowk))
            slowd = list(reversed(slowd))

            last_candle: Candle = rev[0]

            if (last_candle.top >= upper and slowk[0] > 95 and slowd[0] > 85):
                return -1
            if (last_candle.bottom <= lower and slowk[0] < 15 and slowd[0] < 15):
                return 1

        return 0

