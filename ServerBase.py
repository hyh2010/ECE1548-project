from abc import ABC, abstractmethod

class ServerBase(ABC):

    def __init__(self, env, resource):
        self.__env__ = env
        self.__resource__ = resource

    @abstractmethod
    def service_time(self):
        pass

    def action(self):
        return self.__env__.process(self.serve())

    def serve(self):
        arrival_time = self.__env__.now
        with self.__resource__.request() as request:
            yield request
            service_start_time = self.__env__.now
            yield self.__env__.timeout(self.service_time())
            departure_time = self.__env__.now
            response_time = departure_time - arrival_time

        return response_time

