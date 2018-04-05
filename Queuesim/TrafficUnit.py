class TrafficUnit:
    def __init__(self, server):
        self.__action__ = server.action()

    def response_time(self):
        return self.__action__.value

