from Queuesim import Queue

class LoadBalanceQueue(Queue):
    # Detects queue overloading
    def __init__(self, env, capacity, rand_service_time, mu, n, rho_t):
        super().__init__(env, capacity, rand_service_time)
        self.__mu = mu
        self.__n = n
        self.__rho_t = rho_t
        self.__interarrival_times = []
        self.__traffic_sources = []
        self.__traffic_arrival_times = []
        self.__traffic_arrival_times_no_mu = []
        self.__previous_arrival_time = env.now
        self.__rho_estimates = []
        self.__rho_estimates_no_mu = []

    def add_process(self, traffic_source):
        return self.env().process(self.serve(traffic_source))

    def traffic_arrival_times(self):
        return self.__traffic_arrival_times

    def traffic_arrival_times_no_mu(self):
        return self.__traffic_arrival_times_no_mu

    def rho_estimates(self):
        return self.__rho_estimates

    def rho_estimates_no_mu(self):
        return self.__rho_estimates_no_mu

    def load_balance(self, traffic_source):  
        interarrival_time = self.env().now - self.__previous_arrival_time
        self.__interarrival_times.append(interarrival_time)
        self.__previous_arrival_time = self.env().now
        for x in self.__traffic_sources:
            if (traffic_source == x):
                x.load_balance_controller.append(0)
                x.load_balance_no_mu_controller.append(0)
        if (len(self.__interarrival_times)>= self.__n):
            self.__traffic_arrival_times.append(self.env().now)
            lambd_estimate = self.__n/sum(self.__interarrival_times[-self.__n:])
            rho_estimate = lambd_estimate/self.__mu
            self.__rho_estimates.append(rho_estimate)
            for x in self.__traffic_sources:
                if (traffic_source == x):
                    if (len(x.interarrival_times()) >= x.n()):
                        lambd1_estimate = x.n()/sum(x.interarrival_times()[-x.n():])
                        rho1_estimate = lambd1_estimate/self.__mu
                        x.rho1_estimates_controller.append(rho1_estimate)
                        x.rho1_estimates_times_controller.append(self.env().now)
                        if (rho_estimate >= self.__rho_t):
                            if (rho1_estimate < self.__rho_t):
                                x.load_balance_controller[-1] = 1

        # same algorithm but with estimated mu
        if (len(self.service_times)>= self.__n):
            self.__traffic_arrival_times_no_mu.append(self.env().now)
            mu_estimate = self.__n/sum(self.service_times[-self.__n:])
            rho_estimate = lambd_estimate/mu_estimate
            self.__rho_estimates_no_mu.append(rho_estimate)
            for x in self.__traffic_sources:
                if (traffic_source == x):
                    if (len(x.interarrival_times()) >= x.n()):
                        rho1_estimate = lambd1_estimate/mu_estimate
                        x.rho1_estimates_no_mu_controller.append(rho1_estimate)
                        x.rho1_estimates_no_mu_times_controller.append(self.env().now)
                        if (rho_estimate >= self.__rho_t):
                            if (rho1_estimate < self.__rho_t):
                                x.load_balance_no_mu_controller[-1] = 1

    def serve(self, traffic_source):
        self.load_balance(traffic_source)
        return (yield from super().serve())

    def registerTrafficSource(self, traffic_source):
        self.__traffic_sources.append(traffic_source)
