from trend import Trend
from graphic_analysis import GraphicAnalysis
from candle import Candle
from active import Active


class Hammer:
    def __init__(self, active: Active, graphic_analysis: GraphicAnalysis):
        self.active = active
        self.graphic_analysis = graphic_analysis

    def analize(self) -> float:
        trend: Trend = self.graphic_analysis.get_latest_trend()

        last_candle = trend.last_candle
        average_body_size = self.graphic_analysis.get_average_body_size_of_candles()

        if(trend.is_low() and
           last_candle.is_shot(average_body_size) and
           last_candle.body_size != 0 and
           (last_candle.shadow / last_candle.body_size) > 2 and
           (last_candle.wick / last_candle.body_size) < .5):
            print('hammer 100%')
            return 1
        else:
            return 0
