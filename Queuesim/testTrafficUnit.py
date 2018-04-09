import unittest
import simpy
import numpy as np

from TrafficUnit import TrafficUnit
from Queue import QueueConstServiceTime

class testTrafficUnit(unittest.TestCase):
    class __Simulation:

        def __init__(self):
            self.__traffic = []
            env = simpy.Environment()
            env.process(self.__traffic_source())
            service_time = 5
            self.__queue = QueueConstServiceTime(env, capacity=1, service_time=service_time)
            self.__env = env

        def __traffic_source(self):
            traffic1 = TrafficUnit(self.__queue)
            self.__traffic.append(traffic1)
            yield self.__env.timeout(3)
            traffic2 = TrafficUnit(self.__queue)
            self.__traffic.append(traffic2)
            yield self.__env.timeout(2)
            traffic3 = TrafficUnit(self.__queue) 
            self.__traffic.append(traffic3)

        def run(self, until=None):
            self.__env.run(until)

        def number_in_queue(self):
            return self.__queue.number_in_queue()

        def response_times(self):
            return [x.response_time() for x in self.__traffic]

    def test(self):
        simulation = self.__Simulation()
        simulation.run(until=1)
        self.assertEqual(simulation.number_in_queue(), 1)
        simulation.run(until=4)
        self.assertEqual(simulation.number_in_queue(), 2)
        simulation.run(until=6)
        self.assertEqual(simulation.number_in_queue(), 2)
        simulation.run(until=11)
        self.assertEqual(simulation.number_in_queue(), 1)
        simulation.run()
        self.assertEqual(simulation.number_in_queue(), 0)
        expected_response_times = [5, 7, 10]
        np.testing.assert_almost_equal(simulation.response_times(), expected_response_times)

if __name__ == '__main__':
    unittest.main()
