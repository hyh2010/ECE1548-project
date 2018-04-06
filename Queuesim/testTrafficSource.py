import unittest
import simpy
import numpy as np

from TrafficSource import TrafficSourceConstantInterarrival
from Server import ServerConstantServiceTime

class testTrafficSource(unittest.TestCase):

    def setUp(self):
        service_time = 5
        self.__env__ = simpy.Environment()
        resource = simpy.Resource(self.__env__, capacity=1)
        self.__server__ = ServerConstantServiceTime(self.__env__, resource, service_time)

    def test_single_source(self):
        interarrival_time = 2
        number_of_packets = 5
        source = TrafficSourceConstantInterarrival(self.__env__, self.__server__, interarrival_time)
        source.traffic_generator(number_of_packets)
        self.__env__.run()
        response_times = [x.response_time() for x in source.traffic()]

        np.testing.assert_almost_equal(response_times, [5, 8, 11, 14, 17])

    def test_multiple_sources(self):
        interarrival_time_source1 = 3
        number_of_packets_source1 = 3

        interarrival_time_source2 = 4
        number_of_packets_source2 = 2

        source1 = TrafficSourceConstantInterarrival(self.__env__,
                                                    self.__server__,
                                                    interarrival_time_source1)

        source2 = TrafficSourceConstantInterarrival(self.__env__,
                                                    self.__server__,
                                                    interarrival_time_source2)

        source1.traffic_generator(number_of_packets_source1)
        source2.traffic_generator(number_of_packets_source2)

        self.__env__.run()

        response_times_source1 = [x.response_time() for x in source1.traffic()]
        response_times_source2 = [x.response_time() for x in source2.traffic()]

        np.testing.assert_almost_equal(response_times_source1, [5, 12, 19])
        np.testing.assert_almost_equal(response_times_source2, [9, 15])
