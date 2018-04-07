import random
from Queuesim import QueueBase

class QueueExponentialServiceTime(QueueBase):
    def __init__(self, env, capacity, mu):
        super().__init__(env, capacity)
        self.__mu = mu

    def service_time(self):
        return random.expovariate(self.__mu)
