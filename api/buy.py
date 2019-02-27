import datetime
import time
import asyncio
from api.base import Base
from api.dispacher import Dispacher
from api.timesync import TimeSync
import logging
import threading


class Buy(Base):
    name = "buyV2"

    def __init__(self, api, dispacher: Dispacher, timesync: TimeSync):
        super().__init__(api, dispacher, timesync)

        self.active = None
        self.clear()
        self.dispacher.buyComplete += self.on_complete

    def __call__(self, price, active, direction, duration=1, timeout=30):
        self.clear()
        self.active = active

        exp, option = self.get_expiration_time(duration)
        data = {
            "price": price,
            "act": active,
            "exp": exp,
            "type": option,
            "direction": direction.lower(),
            "time": self.api.timesync.server_timestamp
        }

        self.send_websocket_request(self.name, data)
        start = time.time()

        while True:
            if time.time() - start > timeout or self.is_desconected():
                return False, None
            elif self.success != None:
                return self.success, self.result

    # thank Darth-Carrotpie's code
    # https://github.com/Lu-Yi-Hsun/iqoptionapi/issues/6
    def get_expiration_time(self, duration):
        # exp = int(self.api.timesync.server_timestamp)
        exp = int(time.time())

        if duration >= 1 and duration <= 5:
            option = "turbo"
            # Round to next full minute
            # datetime.datetime.now().second>30
            if (exp % 60) > 25:
                duration += 1

            exp = exp - (exp % 60) + (60 * duration)
        elif duration > 5:
            option = "binary"
            period = int(round(duration / 15))
            tmp_exp = exp - (exp % 60)  # nuima sekundes
            tmp_exp = tmp_exp - (tmp_exp % 3600)  # nuimam minutes
            j = 0
            while exp > tmp_exp + (j)*15*60:  # find quarter
                j = j+1
            if exp - tmp_exp > 5 * 60:
                quarter = tmp_exp + (j)*15*60
                exp = quarter + period*15*60
            else:
                quarter = tmp_exp + (j+1)*15*60
                exp = quarter + period*15*60
        else:
            logging.error("ERROR get_expiration_time DO NOT LESS 1")
            exit(1)
        return exp, option

    def clear(self):
        self.success = None
        self.result = None
        self.id = None

    def on_complete(self, message):
        if(message["msg"]["isSuccessful"] and message["msg"]["result"]['act'] == self.active):
            self.success = message["msg"]["isSuccessful"]
            self.result = message["msg"]["result"]
            self.id = message["msg"]["result"]['id']
