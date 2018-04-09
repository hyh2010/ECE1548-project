from abc import ABC, abstractmethod

class QueueMonitorBase(ABC):
    # Periodically monitors states of a Queue

    def __init__(self, queue, sample_period):
        self.__queue = queue
        self.__sample_period = sample_period

    @abstractmethod
    def monitor_action(self): pass

    def queue(self):
        return self.__queue

    def add_process(self):
        return self.__queue.env().process(self.__monitor())

    def __monitor(self):
        while True:
            yield self.__queue.env().timeout(self.__sample_period)
            self.monitor_action()

class QueueMonitorQueueLength(QueueMonitorBase):
    # Monitors the length of a Queue
    def __init__(self, queue, sample_period):
        super().__init__(queue, sample_period)
        self.__sample_times = []
        self.__queue_length_sequence = []

    def monitor_action(self):
        self.__sample_times.append(self.queue().env().now)
        self.__queue_length_sequence.append(self.queue().number_in_queue())

    def queue_length_sequence(self):
        return self.__queue_length_sequence

    def sample_times(self):
        return self.__sample_times
