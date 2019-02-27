from iqoptionapi.api import IQOptionAPI
from api.dispacher import Dispacher
import datetime
import time
from api.base import Base
import logging
from api.timesync import TimeSync


class OperationInfo(Base):

    name = "api_game_betinfo"

    def __init__(self, api: IQOptionAPI, dispacher: Dispacher, timesync: TimeSync):
        super().__init__(api, dispacher, timesync)
        self.clear()
        self.dispacher.api_game_betinfo_result+= self.on_result

    def __call__(self, id_number_list, timeout = 90):
        self.clear()
        data = {"currency": "USD"}

        if type(id_number_list) is list:
            for idx, val in enumerate(id_number_list):
                data["id["+str(idx)+"]"] = int(val)
        elif id_number_list is None:
            logging.error('ERROR - can not input None type, please input buy id')
        else:
            data["id[0]"] = int(id_number_list)

        self.send_websocket_request(self.name, data)
        start = time.time()

        while True:
            if time.time() - start > timeout or self.is_desconected():
                return False, None
            elif self.success == True:
                return self.success, self.result

    def clear(self):
        self.result = None
        self.success = None

    def on_result(self, message):
        self.success = message["msg"]["isSuccessful"]
        self.result = message["msg"]["result"]
