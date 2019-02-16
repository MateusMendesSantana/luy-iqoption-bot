

class Dispacher():
    def __init__(self, api):
        self.api = api

    def on_message(self, websocket, message):
        if message["name"] == "buyComplete":
            locals()[message['name']]()

    def buyComplete(self, message):
        if message["msg"]["isSuccessful"]:
            result = message["msg"]["result"]
            self.api.operations[result['id']] = result