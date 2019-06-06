import time
from threading import Thread


class Stream(Thread):
    def __init__(self, api, code, size, maxdict, check_in_period=.1):
        self.api = api
        self.code = code
        self.size = size
        self.maxdict = maxdict
        self.check_in_period = check_in_period
        self.on_check = []

        super(Stream, self).__init__()

    def subscribe_check(self, callback):
        self.on_check += callback

    def emit(self):
        for x in self.on_check:
            x(self.candles)

    def run(self):
        self.api.start_candles_stream(self.code, self.size, self.maxdict)

        while self.isAlive:
            self.emit()
            time.sleep(self.check_in_period)

    @property
    def candles(self):
        return self.api.get_realtime_candles(self.code, self.size)

    def stop(self):
        print("stop candle")
        self.api.stop_candles_stream(self.code, self.size)
