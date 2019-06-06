from collections import OrderedDict

from api.base import Base
from api.dispacher import Dispacher
from api.timesync import TimeSync
import time

class ListInfoData(Base):

    def __init__(self, api, dispacher: Dispacher, timesync: TimeSync):
        super().__init__(api, dispacher, timesync)
        self.__name = "listInfoData"
        self.clear()
        self.dispacher.listInfoData += self.on_data

    def __call__(self, id, timeout = 90):
        self.clear()
        self.id = id
        start = time.time()

        while True:
            if time.time() - start > timeout or self.is_desconected():
                return None
            elif self.game_state == 1:
                return self.result

    def clear(self):
        self.result = None
        self.id = None
        self.message = None
        self.game_state = None

    def on_data(self, message):
        for get_m in message["msg"]:
            if self.id == get_m["id"]:
               self.result = get_m["win"]
               self.game_state = get_m["game_state"]
               break

