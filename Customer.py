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
        print("Hello")
        print(self.__env__)
        print(self.__resource__)

class testCustomer(unittest.TestCase):
    def test(self):
        env = simpy.Environment()
        resource = simpy.Resource(env, capacity=1)
        customer1 = Customer(env, resource)


if __name__ == '__main__':
    unittest.main()
