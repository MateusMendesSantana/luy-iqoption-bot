import time
import datetime
import threading

from api.base import Base
from api.dispacher import Dispacher

class TimeSync(Base):

    def __init__(self, api, dispacher: Dispacher):
        super().__init__(api, dispacher, self)
        self.__name = "timeSync"
        self.__server_timestamp = time.time()
        self.__expiration_time = 1
        self.timestamp = time.time()

        self.dispacher.timeSync += self.on_data

    def on_data(self, message):
        self.timestamp = message["msg"] / 1000
        print('{} - {}'.format(int(time.time() - self.timestamp), threading.currentThread().getName()))