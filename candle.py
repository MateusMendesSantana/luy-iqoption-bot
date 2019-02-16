import configuration as config

class Candle:

    def __init__(self, args):
        self.id = args['id']
        self.at = args['at']
        self._from = args['from']
        self.to = args['to']
        self.open = args['open']
        self.close = args['close']
        self.max = args['max']
        self.min = args['min']
        self.volume = args['volume']
        
    @property
    def direction(self):
        if self.open == self.close:
            return 0
        return -1 if self.open > self.close else 1

    @property
    def body_size(self):
        return abs(self.force)

    @property
    def top(self):
        return max(self.open, self.close)

    @property
    def bottom(self):
        return min(self.open, self.close)

    @property
    def wick(self):
        return self.max - self.top

    @property
    def shadow(self):
        return self.bottom - self.min

    @property
    def force(self):
        return ((self.close * 1000000) - (self.open * 1000000)) / 1000000

    def is_high(self) -> bool:
        return self.force > 0

    def is_low(self) -> bool:
        return self.force < 0

    def volume_difference(self, average_volume) -> float:
        return self.volume - average_volume

    def volume_indication(self, average_volume) -> float:
        return self.volume / average_volume

    def body_size_difference(self, average_body_size) -> float:
        return self.body_size - average_body_size

    def body_size_indication(self, average_body_size) -> float:
        return self.body_size / average_body_size

    def is_shot(self, average_body_size) -> bool:
        return self.body_size_indication(average_body_size) < config.SHORT_CANDLE

    def is_long(self, average_body_size) -> bool:
        return self.body_size_indication(average_body_size) > config.LONG_CANDLE

    def top_invasion(self, candle) -> bool:
        return candle.open > self.bottom and candle.open < self.top

    def botton_invasion(self, candle) -> bool:
        return candle.open > self.bottom and candle.close < self.top

    def check_body_invasion(self, candle) -> bool:
        return self.top_invasion(candle) or self.botton_invasion(candle)

    def check_body_inclusion(self, candle) -> bool:
        return self.top_invasion(candle) and self.botton_invasion(candle)

    def is_hammer(self):
        return (
            self.body_size != 0 and
            (self.shadow / self.body_size) > 2 and
            (self.wick / self.body_size) < .5
        )

    def is_inverted_hammer(self):
        return (
            self.body_size != 0 and
            (self.wick / self.body_size) > 2 and
            (self.shadow / self.body_size) < .5
        )

