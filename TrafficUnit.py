def serve(env, resource, service_time):
    arrival_time = env.now
    with resource.request() as request:
        yield request
        service_start_time = env.now
        yield env.timeout(service_time)
        departure_time = env.now
        response_time = departure_time - arrival_time

    return response_time

class TrafficUnit:
    def __init__(self, env, resource):
        super().__init__()
        self.__resource__ = resource
        self.__action__ = env.process(serve(env, resource, 5))

    def response_time(self):
        return self.__action__.value

import unittest
import simpy
import numpy as np

class testTrafficUnit(unittest.TestCase):
    class __Simulation__:
        def __init__(self):
            self.__traffic__ = []

        def __traffic_source__(self, env, resource):
            traffic1 = TrafficUnit(env, resource)
            self.__traffic__.append(traffic1)
            yield env.timeout(3)
            traffic2 = TrafficUnit(env, resource)
            self.__traffic__.append(traffic2)
            yield env.timeout(2)
            traffic3 = TrafficUnit(env, resource)
            self.__traffic__.append(traffic3)

        def run(self):
            env = simpy.Environment()
            resource = simpy.Resource(env, capacity=1)
            env.process(self.__traffic_source__(env, resource))
            env.run()

        def response_times(self):
            return [x.response_time() for x in self.__traffic__]

    def test(self):
        simulation = self.__Simulation__()
        simulation.run()
        np.testing.assert_almost_equal(simulation.response_times(), [5, 7, 10])

if __name__ == '__main__':
    unittest.main()
