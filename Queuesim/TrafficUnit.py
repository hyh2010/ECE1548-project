class TrafficUnit:
    def __init__(self, queue):
        self.__action = queue.add_process()

    def response_time(self):
        try:
            return self.__action.value
        except AttributeError:
            # Traffic still in the queue
            pass
