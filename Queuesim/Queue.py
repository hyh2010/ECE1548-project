import simpy

class Queue():

    def __init__(self, env, capacity, rand_service_time):
        self.__env = env
        self.__resource = simpy.Resource(env, capacity)
        self.__rand_service_time = rand_service_time
        self.__number_in_queue = 0
        self.service_times = []

    def add_process(self):
        return self.__env.process(self.serve())

    def env(self):
        return self.__env

    def number_in_queue(self):
        return self.__number_in_queue

    def serve(self):
        arrival_time = self.__env.now
        self.__number_in_queue += 1
        with self.__resource.request() as request:
            yield request
            service_start_time = self.__env.now
            service_time = self.__rand_service_time.generate()
            self.service_times.append(service_time)
            yield self.__env.timeout(service_time)
            departure_time = self.__env.now
            response_time = departure_time - arrival_time
        self.__number_in_queue -= 1
        return response_time
