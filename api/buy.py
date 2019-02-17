import datetime
import time
from api.base import Base
from promise import Promise
from api.dispacher import Dispacher
import logging


class Buy(Base):
    """Class for IQ option buy websocket chanel."""
    # pylint: disable=too-few-public-methods

    name = "buyV2"

    def __init__(self, api, dispacher: Dispacher):
        super().__init__(api, dispacher)

        self.promise: Promise = None
        self.dispacher.buyComplete += self.on_complete
        self.dispacher.buyV2_result += self.on_result

    def __call__(self, price, active, direction, duration):
        """Method to send message to buyv2 websocket chanel.

        :param price: The buying price.
        :param active: The buying active.
        :param direction: The buying direction.
        """
        # thank Darth-Carrotpie's code
        # https://github.com/Lu-Yi-Hsun/iqoptionapi/issues/6
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
        self.promise = Promise()

        return self.promise

    # thank Darth-Carrotpie's code
    # https://github.com/Lu-Yi-Hsun/iqoptionapi/issues/6
    def get_expiration_time(self, duration):
        exp = int(self.api.timesync.server_timestamp)
        if duration >= 1 and duration <= 5:
            option = "turbo"
            # Round to next full minute
            # datetime.datetime.now().second>30
            if (exp % 60) > 30:
                exp = exp - (exp % 60) + 60*(duration+1)
            else:
                exp = exp - (exp % 60)+60*(duration)
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

    def on_complete(self, message):
        if self.promise:
            if message["msg"]["isSuccessful"]:
                result = message["msg"]["result"]
                self.promise.resolve(result)
            else:
                self.promise.reject()

            self.promise = None

    def on_result(self, message):
        if self.promise:
            if message["msg"]["isSuccessful"]:
                result = message["msg"]["result"]
                self.promise.resolve(result)
            else:
                self.promise.reject()

            self.promise = None
