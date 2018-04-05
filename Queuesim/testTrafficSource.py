import unittest
import simpy
import numpy as np

from TrafficSource import TrafficSourceConstantInterarrival
from Server import ServerConstantServiceTime

class testTrafficSource(unittest.TestCase):
    def test_single_source(self):
        env = simpy.Environment()
        resource = simpy.Resource(env, capacity=1)
        service_time = 5
        server = ServerConstantServiceTime(env, resource, service_time)
        interarrival_time = 2
        source = TrafficSourceConstantInterarrival(env, server, interarrival_time)
        number_of_packets = 5
        source.traffic_generator(number_of_packets)
        env.run()
        response_times = [traffic.response_time() for traffic in source.traffic()]
        np.testing.assert_almost_equal(response_times, [5, 8, 11, 14, 17])
