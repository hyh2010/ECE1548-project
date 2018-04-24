import simpy
import matplotlib.pyplot as plt

from Queuesim import Queue
from QueueLoadBalance import QueueLoadBalance
from RandExponential import RandExponential
from TrafficSourceLoadBalance import TrafficSourceLoadBalance

lambd1 = 0.1
lambd2 = 0.8
mu = 1
rho_t = 0.75

n1 = 20
n2 = 160

n = 180

save_as1 = "algorithm1.png"
save_as2 = "algorithm2.png"
save_as3 = "algorithm3.png"

def open_subplots(title):
    subplt1=plt.subplot(3,1,1)
    plt.title(title)
    plt.ylabel(r'$\hat{\rho}$')
    subplt2=plt.subplot(3,1,2,sharex=subplt1, sharey=subplt1)
    plt.ylabel(r'$\hat{\rho_1}$')
    subplt3=plt.subplot(3,1,3,sharex=subplt1, sharey=subplt1)
    plt.xlabel(r'time')
    plt.ylabel(r're-assign')
    plt.ylim(-0.1, 1.1)
    return subplt1, subplt2, subplt3

def plot_single_graph(plt, data, marker, label):
    plt.plot(data['x'], data['y'], marker, label=label)
    plt.legend()

title1 = r"$\mathrm{M/M/1\ Queue\ Load\ Estimation:}\ \lambda_1=%.1f,\ \lambda_2=%.1f, \mu=%.1f, \rho_t=%.2f$" %(lambd1, lambd2, mu, rho_t) + "\n" + r"sample_size_sw1=%d, sample_size_sw2=%d" %(n1, n2)

title2 = r"$\mathrm{M/M/1\ Queue\ Load\ Estimation:}\ \lambda_1=%.1f,\ \lambda_2=%.1f, \mu=%.1f, \rho_t=%.2f$" %(lambd1, lambd2, mu, rho_t) + "\n" + r"sample_size_sw1=%d, sample_size_sw2=%d, sample_size_controller=%d" %(n1, n2, n)

simulation_time = 2000

env=simpy.Environment()
controller = QueueLoadBalance(env, capacity=1, rand_service_time=RandExponential(mu), mu=mu, n=n, rho_t=rho_t)
sw1 = TrafficSourceLoadBalance(controller, lambd1, mu, n1, rho_t)
sw2 = TrafficSourceLoadBalance(controller, lambd2, mu, n2, rho_t)
sw1.add_traffic_generator_process_unlimited()
sw2.add_traffic_generator_process_unlimited()

env.run(simulation_time)

traffic_creation_times_sw1 = [x.creation_time() for x in sw1.traffic()]

traffic_creation_times_sw2 = [x.creation_time() for x in sw2.traffic()]

rho1_estimates_times_sw1, rho1_estimates_sw1 = sw1.rho1_estimates()
rho1_estimates_times_sw2, rho1_estimates_sw2 = sw2.rho1_estimates()

subplt1, subplt2, subplt3 = open_subplots(title1)
plot_single_graph(subplt1, {'x':traffic_creation_times_sw1[n1-1:], 'y':sw1.rho_estimates()}, '-', 'sw1')
plot_single_graph(subplt2, {'x':rho1_estimates_times_sw1, 'y':rho1_estimates_sw1}, '-', 'sw1')
plot_single_graph(subplt3, {'x':traffic_creation_times_sw1, 'y':sw1.reassign()}, '-', 'sw1')

plot_single_graph(subplt1, {'x':traffic_creation_times_sw2[n2-1:], 'y':sw2.rho_estimates()}, '--', 'sw2')
plot_single_graph(subplt2, {'x':rho1_estimates_times_sw2, 'y':rho1_estimates_sw2}, '--', 'sw2')
plot_single_graph(subplt3, {'x':traffic_creation_times_sw2, 'y':sw2.reassign()}, '--', 'sw2')

plt.savefig(save_as1)

plt.clf()

subplt1, subplt2, subplt3 = open_subplots(title2)
plot_single_graph(subplt1, {'x':controller.traffic_arrival_times(), 'y':controller.rho_estimates()}, '-', 'controller')
plot_single_graph(subplt2, {'x':sw1.rho1_estimates_times_controller, 'y':sw1.rho1_estimates_controller}, '-', 'sw1')
plot_single_graph(subplt3, {'x':traffic_creation_times_sw1, 'y':sw1.load_balance_controller}, '-', 'sw1')

plot_single_graph(subplt2, {'x':sw2.rho1_estimates_times_controller, 'y':sw2.rho1_estimates_controller}, '--', 'sw2')
plot_single_graph(subplt3, {'x':traffic_creation_times_sw2, 'y':sw2.load_balance_controller}, '--', 'sw2')

plt.savefig(save_as2)

plt.clf()

subplt1, subplt2, subplt3 = open_subplots(title2)
plot_single_graph(subplt1, {'x':controller.traffic_arrival_times_no_mu(), 'y':controller.rho_estimates_no_mu()}, '-', 'controller')
plot_single_graph(subplt2, {'x':sw1.rho1_estimates_no_mu_times_controller, 'y':sw1.rho1_estimates_no_mu_controller}, '-', 'sw1')
plot_single_graph(subplt3, {'x':traffic_creation_times_sw1, 'y':sw1.load_balance_no_mu_controller}, '-', 'sw1')

plot_single_graph(subplt2, {'x':sw2.rho1_estimates_no_mu_times_controller, 'y':sw2.rho1_estimates_no_mu_controller}, '--', 'sw2')
plot_single_graph(subplt3, {'x':traffic_creation_times_sw2, 'y':sw2.load_balance_no_mu_controller}, '--', 'sw2')

plt.savefig(save_as3)
