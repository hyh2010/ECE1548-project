import simpy

import Queuesim

service_time = 5
interarrival_time = 2
number_of_packets = 5

env = simpy.Environment()
server = Queuesim.ServerConstServiceTime(env, capacity=1, service_time=service_time)
source = Queuesim.TrafficSourceConstInterarrival(server, interarrival_time)
source.add_traffic_generator_process(number_of_packets)
env.run()

for x in source.traffic():
    print (x.response_time())

