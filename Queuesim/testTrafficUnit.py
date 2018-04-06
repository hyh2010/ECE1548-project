import unittest
import simpy
import numpy as np

from TrafficUnit import TrafficUnit
from Server import ServerConstServiceTime

class testTrafficUnit(unittest.TestCase):
    class __Simulation:

        def __init__(self):
            self.__traffic = []
            env = simpy.Environment()
            env.process(self.__traffic_source())
            service_time = 5
            self.__server = ServerConstServiceTime(env, service_time)
            self.__env = env

        def __traffic_source(self):
            traffic1 = TrafficUnit(self.__server)
            self.__traffic.append(traffic1)
            yield self.__env.timeout(3)
            traffic2 = TrafficUnit(self.__server)
            self.__traffic.append(traffic2)
            yield self.__env.timeout(2)
            traffic3 = TrafficUnit(self.__server) 
            self.__traffic.append(traffic3)

        def run(self):
            self.__env.run()

        def response_times(self):
            return [x.response_time() for x in self.__traffic]

    def test(self):
        simulation = self.__Simulation()
        simulation.run()
        expected_response_times = [5, 7, 10]
        np.testing.assert_almost_equal(simulation.response_times(), expected_response_times)

if __name__ == '__main__':
    unittest.main()
