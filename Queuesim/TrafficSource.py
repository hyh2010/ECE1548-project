from abc import ABC, abstractmethod

from TrafficUnit import TrafficUnit

class TrafficSourceBase(ABC):
    def __init__(self, queue):
        self.__traffic = []
        self.__queue = queue

    @abstractmethod
    def interarrival_time(self): pass

    def add_traffic_generator_process(self, n):
        self.__queue.env().process(self.__generate(n))

    def add_traffic_generator_process_unlimited(self):
        self.__queue.env().process(self.__generate_unlimited())

    def traffic(self):
        return self.__traffic

    def __generate(self, n):
        # generates n units of traffic
        for i in range(n):
            yield self.__queue.env().timeout(self.interarrival_time())
            self.__traffic.append(TrafficUnit(self.__queue))

    def __generate_unlimited(self):
        # generates traffic forever
        while True:
            yield self.__queue.env().timeout(self.interarrival_time())
            self.__traffic.append(TrafficUnit(self.__queue))

class TrafficSourceConstInterarrival(TrafficSourceBase):
    def __init__(self, queue, interarrival_time):
        super().__init__(queue)
        self.__interarrival_time = interarrival_time

    def interarrival_time(self):
        return self.__interarrival_time
