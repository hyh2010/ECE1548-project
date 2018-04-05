from abc import ABC, abstractmethod

from TrafficUnit import TrafficUnit

class TrafficSourceBase(ABC):
    def __init__(self, env, server):
        self.__traffic__ = []
        self.__env__ = env
        self.__server__ = server

    @abstractmethod
    def interarrival_time(self): pass

    def traffic_generator(self, n):
        self.__env__.process(self.generate(n))

    def traffic(self):
        return self.__traffic__

    def generate(self, n):
        # generates n units of traffic
        for i in range(n):
            yield self.__env__.timeout(self.interarrival_time())
            self.__traffic__.append(TrafficUnit(self.__server__))
            print("Traffic generated at time %7.4f" % self.__env__.now)

class TrafficSourceConstantInterarrival(TrafficSourceBase):
    def __init__(self, env, server, interarrival_time):
        super().__init__(env, server)
        self.__interarrival_time__ = interarrival_time

    def interarrival_time(self):
        return self.__interarrival_time__
