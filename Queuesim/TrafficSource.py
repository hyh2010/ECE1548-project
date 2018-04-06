from abc import ABC, abstractmethod

from TrafficUnit import TrafficUnit

class TrafficSourceBase(ABC):
    def __init__(self, env, server):
        self.__traffic = []
        self.__env = env
        self.__server = server

    @abstractmethod
    def interarrival_time(self): pass

    def add_traffic_generator_process(self, n):
        self.__env.process(self.__generate(n))

    def traffic(self):
        return self.__traffic

    def __generate(self, n):
        # generates n units of traffic
        for i in range(n):
            yield self.__env.timeout(self.interarrival_time())
            self.__traffic.append(TrafficUnit(self.__server))

class TrafficSourceConstInterarrival(TrafficSourceBase):
    def __init__(self, env, server, interarrival_time):
        super().__init__(env, server)
        self.__interarrival_time = interarrival_time

    def interarrival_time(self):
        return self.__interarrival_time
