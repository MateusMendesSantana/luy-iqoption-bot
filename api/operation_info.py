from iqoptionapi.api import IQOptionAPI
from api.dispacher import Dispacher
import datetime
import time
from api.base import Base
from promise import Promise
import logging


class OperationInfo(Base):

    name = "api_game_betinfo"

    def __init__(self, api: IQOptionAPI, dispacher: Dispacher):
        super.__init__(api, dispacher)
        self.promise: Promise = None
        self.dispacher.api_game_betinfo_result+= self.on_result

    def __call__(self, id_number_list):
        data = {"currency": "USD"}

        if type(id_number_list) is list:
            for idx, val in enumerate(id_number_list):
                data["id["+str(idx)+"]"] = int(val)
        elif id_number_list is None:
            logging.error('ERROR - can not input None type, please input buy id')
        else:
            data["id[0]"] = int(id_number_list)

        self.send_websocket_request(self.name, data)
        self.promise = Promise()

        return self.promise()

    def on_result(self, message):
        try:
            if message["msg"]["isSuccessful"]:
                self.promise.resolve(message)
            else:
                self.promise.reject(message)
        except:
            self.promise.reject(message)
