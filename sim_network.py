import simpy

import Queuesim

class SimServer(Queuesim.ServerBase):
    def __init__(self, env, resource):
        super().__init__(env, resource)

    def service_time(self):
        return 5

def source(env, server):
    packet1 = Queuesim.TrafficUnit(server)
    yield env.timeout(3)
    packet2 = Queuesim.TrafficUnit(server)
    yield env.timeout(2)
    packet3 = Queuesim.TrafficUnit(server) 

env = simpy.Environment()
resource = simpy.Resource(env, capacity=1)
server = SimServer(env, resource)
env.process(source(env,server))
env.run()

