class TrafficUnit:
    def __init__(self, queue):
        self.__action = queue.add_process()

    def response_time(self):
        return self.__action.value
