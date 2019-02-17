from events import Events
import json
from iqoptionapi.api import IQOptionAPI

class Dispacher(Events):
    def __init__(self, api: IQOptionAPI):
        self.api = api
        self.api.websocket.on_message = self.on_message
        super().__init__(['buyComplete', 'buyV2_result'])

    def on_message(self, websocket, message):
        self.api.websocket_client.on_message(websocket, message)

        message = json.loads(str(message))

        if message["name"] == "buyComplete":
            locals()[message['name']](message)
        elif message["name"] == "buyV2_result":
            locals()[message['name']](message)
