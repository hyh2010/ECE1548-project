from abc import ABC, abstractmethod

from TrafficUnit import TrafficUnit

class TrafficSourceBase(ABC):
    def __init__(self, server):
        self.__traffic = []
        self.__server = server

    @abstractmethod
    def interarrival_time(self): pass

    def add_traffic_generator_process(self, n):
        self.__server.env().process(self.__generate(n))

    def traffic(self):
        return self.__traffic

    def __generate(self, n):
        # generates n units of traffic
        for i in range(n):
            yield self.__server.env().timeout(self.interarrival_time())
            self.__traffic.append(TrafficUnit(self.__server))

class TrafficSourceConstInterarrival(TrafficSourceBase):
    def __init__(self, server, interarrival_time):
        super().__init__(server)
        self.__interarrival_time = interarrival_time

    def interarrival_time(self):
        return self.__interarrival_time
