from iqoptionapi.api import IQOptionAPI
from api.dispacher import Dispacher
import time

class Base(object):

    def __init__(self, api: IQOptionAPI, dispacher: Dispacher, timesync):
        self.api = api
        self.dispacher = dispacher
        self.timesync = timesync

    def send_websocket_request(self, name, msg):
        return self.api.send_websocket_request(name, msg)

    def is_desconected(self):
        return abs(self.timesync.timestamp - time.time()) > 10

