import random


RANDOM_SEED = 42
NEW_CUSTOMERS = 5 # Total number of customers
INTERVAL_CUTOMERS = 10.0 # Generate new customers roughly every x seconds
MIN_PATIENCE = 1
MAX_PATIENCE = 3

import unittest
import simpy

class Customer:
    def __init__(self, env, resource):
        self.__env__ = env
        self.__resource__ = resource
        self.__response_time__ = 0

    def arrive(self, service_time):
        arrival_time = self.__env__.now
        print("Customer arrives at %7.4f" % arrival_time)
        with self.__resource__.request() as request:
            yield request
            service_start_time = self.__env__.now
            waiting_time = service_start_time - arrival_time
            print("Customer waiting time %7.4f" % waiting_time)
            yield self.__env__.timeout(service_time)
            departure_time = self.__env__.now
            print("Customer leaves at %7.4f" % departure_time)
            self.__response_time__ = departure_time - arrival_time

class testCustomer(unittest.TestCase):
    #class __Simulation__:

    def __customer_source__(self, env, resource):
        customer1 = Customer(env, resource)
        env.process(customer1.arrive(5))
        yield env.timeout(3)
        customer2 = Customer(env, resource)
        env.process(customer2.arrive(3))
        yield env.timeout(2)
        customer3 = Customer(env, resource)
        env.process(customer3.arrive(2))

    def test(self):
        env = simpy.Environment()
        resource = simpy.Resource(env, capacity=1)
        env.process(self.__customer_source__(env, resource))
        env.run()

if __name__ == '__main__':
    unittest.main()
