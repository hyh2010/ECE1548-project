import simpy

from QueueExponentialServiceTime import QueueExponentialServiceTime
from TrafficSourcePoissonArrival import TrafficSourcePoissonArrival

import matplotlib.pyplot as plt

# Queue has load 0.25:
lambd = 1.2
mu = 1
number_of_packets = 1000

env = simpy.Environment()
controller = QueueExponentialServiceTime(env, capacity=1, mu=mu)
switch = TrafficSourcePoissonArrival(controller, lambd)
switch.add_traffic_generator_process(number_of_packets)

env.run()

response_times = [x.response_time() for x in switch.traffic()]

n, bins, patches = plt.hist(response_times)

plt.show()
