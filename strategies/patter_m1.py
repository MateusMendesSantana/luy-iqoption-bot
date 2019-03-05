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


class PatternM1:
    def __init__(self, api: IQ_Option, active: Active, graphic_analysis: GraphicAnalysis):
        self.api = api
        self.active = active
        self.graphic_analysis = graphic_analysis

    def analize(self) -> float:
        if (time.time() % 60 <= 5):
            candles = self.graphic_analysis.candles

            rev = list(reversed(candles))

            if(rev[2].is_doji() or rev[3].is_doji() or rev[4].is_doji() or rev[5].is_doji()):
                return 0

            # alternando de 2 em 2, ultima cor
            if (rev[5].is_high() and rev[4].is_high() and rev[3].is_low() and rev[2].is_low()):
                return -1
            if (rev[2].is_high() and rev[3].is_high() and rev[4].is_low() and rev[5].is_low()):
                return 1

            # alternando, continuar alternando
            if (rev[2].is_high() and rev[3].is_low() and rev[4].is_high() and rev[5].is_low()):
                return 1
            if (rev[2].is_low() and rev[3].is_high() and rev[4].is_low() and rev[5].is_high()):
                return -1

            # cor do meio
            if (rev[2].is_low() and rev[3].is_high() and rev[4].is_high() and rev[5].is_low()):
                return 1
            if (rev[2].is_high() and rev[3].is_low() and rev[4].is_low() and rev[5].is_high()):
                return -1

            # 3 de mesma cor
            count = rev[2].direction + rev[3].direction + rev[4].direction + rev[5].direction
            if (count == 2):
                return -1
            if (count == -2):
                return 1

            # 4 da mesma cor
            if (count == -4):
                return 1
            if (count == 4):
                return -1

        return 0

