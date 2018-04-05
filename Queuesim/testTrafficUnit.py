import unittest
import simpy
import numpy as np

from TrafficUnit import TrafficUnit
from Server import ServerConstantServiceTime

class testTrafficUnit(unittest.TestCase):
    class __Simulation__:

        def __init__(self):
            self.__traffic__ = []
            env = simpy.Environment()
            resource = simpy.Resource(env, capacity=1)
            env.process(self.__traffic_source__())
            service_time = 5
            self.__server__ = ServerConstantServiceTime(env, resource, service_time)
            self.__env__ = env

        def __traffic_source__(self):
            traffic1 = TrafficUnit(self.__server__)
            self.__traffic__.append(traffic1)
            yield self.__env__.timeout(3)
            traffic2 = TrafficUnit(self.__server__)
            self.__traffic__.append(traffic2)
            yield self.__env__.timeout(2)
            traffic3 = TrafficUnit(self.__server__) 
            self.__traffic__.append(traffic3)

        def run(self):
            self.__env__.run()

        def response_times(self):
            return [x.response_time() for x in self.__traffic__]

    def test(self):
        simulation = self.__Simulation__()
        simulation.run()
        np.testing.assert_almost_equal(simulation.response_times(), [5, 7, 10])
