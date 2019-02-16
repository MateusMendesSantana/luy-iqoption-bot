import math

class B:
    def __init__(self):
        self.reset()

    def add_win(self):
        self.entry+= 1

        if self.entry == 4:
            self.reset()

    def add_loose(self):
        self.reset()

    def get_next_entry(self, profit: float):
        return math.pow(profit + 1, self.entry)

    def reset(self):
        self.entry = 0
