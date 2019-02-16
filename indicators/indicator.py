
class Indicator():
    tred = 0

    def __init__(self, api):
        self.api = api

    def analyze_candles(self, candles):
        for candle in candles:
            self.tred += 1
