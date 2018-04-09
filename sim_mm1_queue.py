import simpy
import math
import matplotlib.pyplot as plt
from scipy import stats

from QueueExponentialServiceTime import QueueExponentialServiceTime
from TrafficSourcePoissonArrival import TrafficSourcePoissonArrival
from QueueMonitor import QueueMonitorQueueLength

def exponentialpdf(x,lambd):
    if (x < 0): return 0
    return lambd * math.exp(-lambd*x)

lambd = 0.5
mu = 2
simulation_time = 2000
monitor_sample_period = 0.5/lambd

env = simpy.Environment()
controller = QueueExponentialServiceTime(env, capacity=1, mu=mu)
switch = TrafficSourcePoissonArrival(controller, lambd)
switch.add_traffic_generator_process_unlimited()

monitor = QueueMonitorQueueLength(controller, monitor_sample_period)
monitor.add_process()

env.run(simulation_time)

response_times = [x.response_time() for x in switch.traffic() if x.response_time() != None]

queue_length_sequence = monitor.queue_length_sequence()
max_queue_length = max(queue_length_sequence)
queue_length_relative_frequency = stats.relfreq(queue_length_sequence, numbins=max_queue_length+1).frequency


theoretical_stationary_pmf = []
for i in range(max_queue_length + 1):
    theoretical_stationary_pmf.append(math.pow((lambd/mu),i) * (1 - lambd/mu))

plt.figure(figsize=(6,6))

plt.subplot(2,1,1)
plt.plot(monitor.sample_times(), queue_length_sequence)
plt.xlabel('time')
plt.ylabel('queue length')

title_string = r'$\mathrm{M/M/1\ Queue\ Simulation:}\ \lambda=%.1f,\ \mu=%.1f$' %(lambd, mu)
plt.title(title_string)

plt.subplot(2,1,2)
plt.plot(theoretical_stationary_pmf, 'bo', label='theoretical stationary pmf')
plt.plot(queue_length_relative_frequency, 'r^', label='simulation relative frequency')
plt.xlabel('queue length')
plt.xticks(range(max_queue_length + 1))
plt.legend()
plt.savefig('queue_length.png')


plt.figure()
n, bins, patches = plt.hist(response_times, normed=1)

binmidpoints = (bins[:-1] + bins[1:])/2

y = [exponentialpdf(x, mu - lambd) for x in binmidpoints]

plt.plot(binmidpoints, y, label='theoretical pdf')
plt.xlabel('response time')
plt.legend()

plt.savefig('response_time.png')
