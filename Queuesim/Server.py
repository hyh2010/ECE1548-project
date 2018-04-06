import simpy

from abc import ABC, abstractmethod

class ServerBase(ABC):

    def __init__(self, env, capacity):
        self.__env = env
        self.__resource = simpy.Resource(env, capacity)

    @abstractmethod
    def service_time(self): pass

    def add_process(self):
        return self.__env.process(self.serve())

    def env(self):
        return self.__env

    def serve(self):
        arrival_time = self.__env.now
        with self.__resource.request() as request:
            yield request
            service_start_time = self.__env.now
            yield self.__env.timeout(self.service_time())
            departure_time = self.__env.now
            response_time = departure_time - arrival_time

        return response_time

class ServerConstServiceTime(ServerBase):
    def __init__(self, env, capacity, service_time):
        super().__init__(env, capacity)
        self.__service_time = service_time

    def service_time(self):
        return self.__service_time

