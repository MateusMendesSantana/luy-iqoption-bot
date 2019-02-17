from iqoptionapi.api import IQOptionAPI
from api.dispacher import Dispacher


class Base(object):

    def __init__(self, api: IQOptionAPI, dispacher: Dispacher):
        """
        :param api: The instance of :class:`IQOptionAPI
            <iqoptionapi.api.IQOptionAPI>`.
        """
        self.api = api
        self.dispacher = dispacher

    def send_websocket_request(self, name, msg):
        """Send request to IQ Option server websocket.

        :param str name: The websocket chanel name.
        :param dict msg: The websocket chanel msg.

        :returns: The instance of :class:`requests.Response`.
        """
        return self.api.send_websocket_request(name, msg)
