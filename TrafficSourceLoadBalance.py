from TrafficSourcePoissonArrival import TrafficSourcePoissonArrival
from TrafficUnitEnhanced import TrafficUnitEnhanced

class TrafficSourceLoadBalance(TrafficSourcePoissonArrival):
    def __init__(self, queue, lambd, mu, n, rho_t):
        super().__init__(queue, lambd)
        self.__n = n
        self.__mu = mu
        self.__rho_t = rho_t
        self.__interarrival_times = []
        self.__rho_estimates = []
        self.__rho1_estimates_times = []
        self.__rho1_estimates = []
        self.__load_balance = []
        self.queue().registerTrafficSource(self)
        self.rho1_estimates_times_controller = []
        self.rho1_estimates_controller = []
        self.load_balance_controller = []
        self.rho1_estimates_no_mu_times_controller = []
        self.rho1_estimates_no_mu_controller = []
        self.load_balance_no_mu_controller = []
    def __request_reassignment_if_necessary(self):
        self.__load_balance.append(0)
        if (len(self.traffic()) >= self.__n):
            delay_data = []
            censored_delay_data = []
            for x in self.traffic()[-self.__n:]:
                if (x.response_time() != None):
                    delay_data.append(x.response_time())
                else:
                    censored_delay_data.append(self.queue().env().now - x.creation_time())
            m = len(delay_data)
            lambd_estimate = self.__mu - m / (sum(delay_data) + sum(censored_delay_data))
            rho_estimate = lambd_estimate / self.__mu
            self.__rho_estimates.append(rho_estimate)
            lambd1_estimate=self.__n/sum(self.__interarrival_times[-self.__n:])
            rho1_estimate = lambd1_estimate/self.__mu
            self.__rho1_estimates_times.append(self.queue().env().now)
            self.__rho1_estimates.append(rho1_estimate)
            if (rho_estimate >= self.__rho_t):
                if (rho1_estimate < self.__rho_t):
                    self.__load_balance[-1]=1

    def n(self):
        return self.__n

    def rho_estimates(self):
        return self.__rho_estimates

    def rho1_estimates(self):
        return self.__rho1_estimates_times, self.__rho1_estimates

    def load_balance(self):
        return self.__load_balance

    def interarrival_times(self):
        return self.__interarrival_times
    def generate_single_traffic(self):
        # override the traffic generation function to generate TrafficUnitEnhanced
        interarrival_time = self.interarrival_time()
        yield self.queue().env().timeout(interarrival_time)
        self.__interarrival_times.append(interarrival_time)
        self.traffic().append(TrafficUnitEnhanced(self.queue(), self))
        self.__request_reassignment_if_necessary()

