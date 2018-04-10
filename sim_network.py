import simpy

import Queuesim

service_time = 5
interarrival_time = 2
number_of_packets = 5

env = simpy.Environment()
controller = Queuesim.Queue(env, capacity=1, rand_service_time=Queuesim.RandDeterministic(service_time))
switch = Queuesim.TrafficSourceConstInterarrival(controller, interarrival_time)
switch.add_traffic_generator_process(number_of_packets)
env.run()

for x in switch.traffic():
    print (x.response_time())
