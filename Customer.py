import random

class Customer:
    def __init__(self, env, resource):
        self.__env__ = env
        self.__resource__ = resource
        self.__response_time__ = 0

    def arrive(self, service_time):
        arrival_time = self.__env__.now
        with self.__resource__.request() as request:
            yield request
            service_start_time = self.__env__.now
            yield self.__env__.timeout(service_time)
            departure_time = self.__env__.now
            self.__response_time__ = departure_time - arrival_time

    def response_time(self):
        return self.__response_time__

import unittest
import simpy
import numpy as np

class testCustomer(unittest.TestCase):
    class __Simulation__:
        def __init__(self):
            self.__customers__ = []

        def __customer_source__(self, env, resource):
            customer1 = Customer(env, resource)
            self.__customers__.append(customer1)
            env.process(customer1.arrive(5))
            yield env.timeout(3)
            customer2 = Customer(env, resource)
            self.__customers__.append(customer2)
            env.process(customer2.arrive(5))
            yield env.timeout(2)
            customer3 = Customer(env, resource)
            self.__customers__.append(customer3)
            env.process(customer3.arrive(5))

        def run(self):
            env = simpy.Environment()
            resource = simpy.Resource(env, capacity=1)
            env.process(self.__customer_source__(env, resource))
            env.run()

        def response_times(self):
            return [customer.response_time() for customer in self.__customers__]

    def test(self):
        simulation = self.__Simulation__()
        simulation.run()
        np.testing.assert_almost_equal(simulation.response_times(), [5, 7, 10])

if __name__ == '__main__':
    unittest.main()
