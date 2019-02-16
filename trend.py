from candle import Candle

class Trend:
    def __init__(self, candles: list):
        self.candles = candles

    @property
    def first_candle(self) -> Candle:
        return self.candles[0]

    @property
    def last_candle(self) -> Candle:
        return self.candles[len(self.candles) - 1]

    @property
    def penultimate_candle(self) -> Candle:
        return self.candles[len(self.candles) - 2]

    @property
    def direction(self) -> float:
        return self.last_candle.top - self.first_candle.bottom

    def is_high(self):
        return self.direction > 0

    def is_low(self):
        return self.direction < 0

    @property
    def force(self) -> float:
        return self.direction / len(self.candles)

    @property
    def height(self) -> float:
        return abs(self.direction)
