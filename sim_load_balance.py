import simpy
import matplotlib.pyplot as plt
from LoadBalanceQueue import LoadBalanceQueue
from Queuesim import RandDeterministic, TrafficSourceConstInterarrival
from QueueMonitor import QueueMonitorQueueLength

interarrival_time = 1
service_time = 1.5
simulation_time = 10

monitor_sample_period = 0.1

env = simpy.Environment()
controller = LoadBalanceQueue(env, capacity=1, rand_service_time=RandDeterministic(service_time))
switch = TrafficSourceConstInterarrival(controller, interarrival_time=1)
switch.add_traffic_generator_process_unlimited()

monitor = QueueMonitorQueueLength(controller, monitor_sample_period)
monitor.add_process()

env.run(simulation_time)

plt.plot(monitor.sample_times(), monitor.queue_length_sequence())
plt.xlabel('time')
plt.ylabel('queue length')

plt.show()
