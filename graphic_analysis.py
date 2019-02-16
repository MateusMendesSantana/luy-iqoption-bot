import time
from statistics import median, mean
from candle import Candle
from trend import Trend


class GraphicAnalysis:
    candles = []

    def set_candles(self, candles: list):
        self.candles = candles

    def get_average_body_size_of_candles(self) -> float:
        body_sizes = list(
            map(lambda candle: candle.body_size, self.candles))
        return mean(body_sizes)

    def get_average_volume_of_candles(self) -> float:
        volumes = list(map(lambda candle: candle.volume, self.candles))
        return mean(volumes)

    def get_median_body_size_of_candles(self) -> float:
        body_sizes = list(
            map(lambda candle: candle.body_size, self.candles))
        return median(body_sizes)

    def get_median_volume_of_candles(self) -> float:
        volumes = list(map(lambda candle: candle.volume, self.candles))
        return median(volumes)

    def get_trends(self) -> list:
        trends = []
        avarage_body_size = self.get_average_body_size_of_candles()

        trend_candles = []

        dir = self.candles[0].direction
        for candle in self.candles:

            if(candle.is_shot(avarage_body_size) or candle.direction == dir):
                trend_candles.append(candle)
            else:
                trends.append(Trend(trend_candles))
                trend_candles = [candle]
                dir = candle.direction
        
        return trends

    def get_latest_trend(self) -> Trend:
        trends = self.get_trends()
        return trends[len(trends) - 1]
