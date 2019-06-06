import math

class Martingale:
    def __init__(self):
        self.reset()

    def add_win(self):
        self.reset()

    def add_loose(self):
        self.losses+= 1

        if self.losses == 3:
            self.reset()

    def get_next_entry(self, profit: float):
        return math.pow(2, self.losses)

    def reset(self):
        self.losses = 0
