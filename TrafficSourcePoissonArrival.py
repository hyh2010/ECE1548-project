import random
from Queuesim import TrafficSourceBase

class TrafficSourcePoissonArrival(TrafficSourceBase):
    def __init__(self, queue, lambd):
        super().__init__(queue)
        self.__lambd = lambd

    def interarrival_time(self):
        return random.expovariate(self.__lambd)
