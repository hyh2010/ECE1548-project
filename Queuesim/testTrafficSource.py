import unittest
import simpy
import numpy as np

from TrafficSource import TrafficSourceConstInterarrival
from Queue import QueueConstServiceTime

class testTrafficSource(unittest.TestCase):

    def setUp(self):
        service_time = 5
        env = simpy.Environment()
        self.__queue = QueueConstServiceTime(env, capacity=1, service_time=service_time)

    def test_single_source(self):
        interarrival_time = 2
        number_of_packets = 5
        source = TrafficSourceConstInterarrival(self.__queue, interarrival_time)
        source.add_traffic_generator_process(number_of_packets)
        self.__queue.env().run()
        response_times = [x.response_time() for x in source.traffic()]

        expected_response_times = [5, 8, 11, 14, 17]
        np.testing.assert_almost_equal(response_times, expected_response_times)

    def test_single_source_unlimited(self):
        interarrival_time = 2
        source = TrafficSourceConstInterarrival(self.__queue, interarrival_time)
        source.add_traffic_generator_process_unlimited()
        self.__queue.env().run(30)
        response_times = [x.response_time() for x in source.traffic() if x.response_time() != None]

        expected_response_times = [5, 8, 11, 14, 17] 
        np.testing.assert_almost_equal(response_times, expected_response_times)

    def test_multiple_sources(self):
        interarrival_time_source1 = 3
        number_of_packets_source1 = 3

        interarrival_time_source2 = 4
        number_of_packets_source2 = 2

        source1 = TrafficSourceConstInterarrival(self.__queue,
                                                 interarrival_time_source1)

        source2 = TrafficSourceConstInterarrival(self.__queue,
                                                 interarrival_time_source2)

        source1.add_traffic_generator_process(number_of_packets_source1)
        source2.add_traffic_generator_process(number_of_packets_source2)

        self.__queue.env().run()

        response_times_source1 = [x.response_time() for x in source1.traffic()]
        response_times_source2 = [x.response_time() for x in source2.traffic()]

        expected_response_times_source1 = [5, 12, 19]
        expected_response_times_source2 = [9, 15]

        np.testing.assert_almost_equal(response_times_source1, expected_response_times_source1)
        np.testing.assert_almost_equal(response_times_source2, expected_response_times_source2)

if __name__ == '__main__':
    unittest.main()
