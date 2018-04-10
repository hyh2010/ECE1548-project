from Queuesim import Queue

class LoadBalanceQueue(Queue):
    # Detects queue overloading
    def __init__(self, env, capacity, rand_service_time):
        super().__init__(env, capacity, rand_service_time)
        self.__queue_length_previous_arrival = 0

    def serve(self):
        current_queue_length = self.number_in_queue() + 1
        if (current_queue_length > self.__queue_length_previous_arrival):
            print(self.env().now)
            print("Overload detected")
            print(self.__queue_length_previous_arrival)
            print(self.number_in_queue() + 1)
        self.__queue_length_previous_arrival = current_queue_length
        yield from super().serve()
