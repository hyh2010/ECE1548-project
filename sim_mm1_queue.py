import simpy
import math
import matplotlib.pyplot as plt

from QueueExponentialServiceTime import QueueExponentialServiceTime
from TrafficSourcePoissonArrival import TrafficSourcePoissonArrival


def exponentialpdf(x,lambd):
    if (x < 0): return 0
    return lambd * math.exp(-lambd*x)

lambd = 0.5
mu = 2
simulation_time = 500

env = simpy.Environment()
controller = QueueExponentialServiceTime(env, capacity=1, mu=mu)
switch = TrafficSourcePoissonArrival(controller, lambd)
switch.add_traffic_generator_process_unlimited()

env.run(simulation_time)

response_times = [x.response_time() for x in switch.traffic() if x.response_time() != None]

n, bins, patches = plt.hist(response_times, normed=1)

binmidpoints = (bins[:-1] + bins[1:])/2

y = [exponentialpdf(x, mu - lambd) for x in binmidpoints]

plt.plot(binmidpoints, y, label='theoretical pdf')

plt.xlabel('response time')
plt.title(r'$\mathrm{M/M/1\ Queue\ Simulation\ of\ %d\ Timeunits:}\ \lambda=%.1f,\ \mu=%.1f$' %(simulation_time, lambd, mu))

plt.legend()

plt.show()
