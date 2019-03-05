import math

class Martingale:
    def __init__(self):
        self.reset()

    def add_win(self):
        self.reset()

    def add_loose(self):
        self.entry+= self.entry

        if self.entry == 4:
            self.reset()

    def get_next_entry(self, profit: float):
        return math.pow(1.0 / profit, self.entry)

    def reset(self):
        self.entry = 1
        self.losses = 0
