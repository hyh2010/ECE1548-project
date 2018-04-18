from Queuesim import TrafficUnit

class TrafficUnitEnhanced(TrafficUnit):
    def __init__(self, queue, traffic_source):
        self.action = queue.add_process(traffic_source)
        self.__creation_time = queue.env().now

    def creation_time(self):
        return self.__creation_time
