from events import Events
import json
from iqoptionapi.api import IQOptionAPI

class Dispacher(Events):
    operations = [
        'timeSync',
        'candle-generated',
        'candles-generated',
        'heartbeat',
        'profile',
        'candles',
        'buyComplete',
        'buyV2_result',
        'listInfoData',
        'api_option_init_all_result',
        'instruments',
        'financial-information',
        'strike-list',
        'api_game_betinfo_result',
        'traders-mood-changed',
        'order-placed-temp',
        'order',
        'positions',
        'deferred-orders',
        'position-history',
        'available-leverages',
        'order-canceled',
        'position-closed',
        'overnight-fee',
        'api_game_getoptions_result',
        'sold-options',
        'tpsl-changed',
        'position-changed',
        'auto-margin-call-changed',
        'instrument-quotes-generated'
    ]

    def __init__(self, api: IQOptionAPI):
        self.api = api
        self.api.websocket.on_message = self.on_message
        super().__init__(self.operations)

    def on_message(self, websocket, message):
        self.api.websocket_client.on_message(websocket, message)

        message = json.loads(str(message))

        locals()[message['name']](message)
