from iqoptionapi.stable_api import IQ_Option


class Api:
    def __init__(self, api):
        self.api: IQ_Option = api

    def get_candles(self, active_name, interval, count, endtime):
        self.api.api.candles.candles_data = None

        while True:
            try:
                self.api.api.getcandles(
                    OP_code.ACTIVES[ACTIVES], interval, count, endtime)

                while self.api.check_connect and self.api.candles.candles_data == None:
                    pass
                if self.api.api.candles.candles_data != None:
                    break
            except:
                return False, None

        return True, self.api.candles.candles_data
