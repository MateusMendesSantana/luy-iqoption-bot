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

        if (purchase_time <= 15):
            candles = self.graphic_analysis.candles
            # open = array(list(map(lambda x: x.open, candles)))
            close = array(list(map(lambda x: x.close, candles)))
            high = array(list(map(lambda x: x.max, candles)))
            low = array(list(map(lambda x: x.min, candles)))
            # volume = array(list(map(lambda x: x.volume, candles)))

            outReal = list(reversed(ta.SAR(
                high,
                low,
                0.02, /* optAcceleration_Factor, optional */
                0.2, /* optAF_Maximum, optional */
                0, /* startIdx, optional */
                3 /* endIdx, optional */
            )))
            rsi = list(reversed(ta.RSI(close, timeperiod=4)))

            if (rsi[0] > 80):
                return -1
            if (rsi[0] < 20):
                return 1

        return 0

