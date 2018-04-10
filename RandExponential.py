import random
from Queuesim import RandBase

class RandExponential(RandBase):
    def __init__(self, lambd):
        self.__lambd = lambd

    def generate(self):
        return random.expovariate(self.__lambd)
