class TrafficUnit:
    def __init__(self, server):
        self.__action = server.add_process()

    def response_time(self):
        return self.__action.value

