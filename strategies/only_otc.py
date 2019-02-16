# IQ Option- Operando em OTC- Técnica 100% - Estocástico+RSI
# https://www.youtube.com/watch?v=cofXogyAMXo
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


class Otc100:
    def __init__(self, api: IQ_Option, active: Active, graphic_analysis: GraphicAnalysis):
        self.api = api
        self.active = active
        self.graphic_analysis = graphic_analysis

    def analize(self) -> float:
        isOtc = self.active.name.endswith('OTC')

        if (isOtc):
            purchase_time = 60 - ((time.time() + 30) % 60)

            if (purchase_time <= 15):
                candles = self.graphic_analysis.candles
                # open = array(list(map(lambda x: x.open, candles)))
                close = array(list(map(lambda x: x.close, candles)))
                high = array(list(map(lambda x: x.max, candles)))
                low = array(list(map(lambda x: x.min, candles)))
                # volume = array(list(map(lambda x: x.volume, candles)))

                real = ta.RSI(close, timeperiod=2)
                slowk, slowd = ta.STOCH(high, low, close, fastk_period=3, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
                # slowk, slowd = STOCH(high, low, close, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
                rsi = real[len(real)-1]
                k = slowk[len(slowk)-1]
                d = slowd[len(slowd)-1]

                if (rsi > 90 and k > d):
                    return -1

                print(purchase_time)

        return 0

