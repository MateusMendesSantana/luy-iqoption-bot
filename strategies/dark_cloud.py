from candle import Candle
from graphic_analysis import GraphicAnalysis
from trend import Trend
from candle import Candle
from active import Active


class DarkCloud:

    def __init__(self, active: Active, graphic_analysis: GraphicAnalysis):
        self.active = active
        self.graphic_analysis = graphic_analysis

    def analize(self) -> float:
        trend: Trend = self.graphic_analysis.get_latest_trend()

        last_candle = trend.last_candle
        penultimate_candle = trend.penultimate_candle
        average_body_size = self.graphic_analysis.get_average_body_size_of_candles()
        
        if(trend.is_high() and
           penultimate_candle.is_high() and
           penultimate_candle.is_long(average_body_size) and
           last_candle.is_low()): # and
           # last_candle.check_body_invasion(penultimate_candle)):
            print('Dark Cloud -100%')
            return -1
        else:
            return 0
