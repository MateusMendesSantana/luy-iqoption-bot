import configuration as config

class Active:

    def __init__(self, data: dict):
        self.set_data(data)

        if(self.enabled):
            print('{} profit {}%'.format(self.name, self.profit * 100))

    def set_data(self, data: dict):
        self.code = data['id']
        self.name = data['name'].replace('front.', '')
        self.profit = (100.0 - data["option"]["profit"]["commission"]) / 100.0
        self.enabled = data['enabled']

    def is_profitable(self):
        return self.profit >= config.OPERATION_WHEN_PROFIT
        
