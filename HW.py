import numpy as np
import math
import random
import pickle


class BoundedPareto:
    def __init__(self, k, p, alpha):
        self.k = k
        self.p = p
        self.alpha = alpha

    def generate(self):
        area = random.random()
        x = self.k / (1 + area * ((self.k / self.p) ** self.alpha - 1)) ** (1 / self.alpha)
        return x

    def getNthMoment(self, n):
        moment = self.k ** self.alpha / (1 - (self.k / self.p) ** self.alpha)
        moment *= self.alpha * (self.k ** (n - self.alpha) - self.p ** (n - self.alpha)) / (self.alpha - n)

        return moment


class Exponential:
    def __init__(self, rate):
        self.rate = rate

    def generate(self):
        area = random.random()
        x = -math.log(1 - area, math.e) / self.rate
        return x


class Job:
    def __init__(self, arrival, service_time):
        self.arrival = arrival
        self.service_time = service_time
        self.exit = None


class Simulator:
    def simulateMM1(self, num_arrivals, trials, service_rate, arrival_rate):
        response_times = []
        arrival = Exponential(arrival_rate)
        service = Exponential(service_rate)
        for i in range(trials):
            t = 0
            jobs = []
            for i in range(num_arrivals + 1):
                t += arrival.generate() if i != 0 else 0
                jobs.append(Job(t, service.generate()))

            time = 0

            for job in jobs:
                # if job was in queue
                if time > job.arrival:
                    time += job.service_time
                # if job just arrived and server is empty
                else:
                    time = job.arrival + job.service_time
                job.exit = time
            response_times.append(jobs[-1].exit - jobs[-1].arrival)
        print('M/M/1 Queue')
        print('Service Rate: {0}\tArrival Rate: {1}'.format(service_rate, arrival_rate))
        print('Sample Mean: {0}\tExpected Mean: {1}'.format(round(np.mean(response_times), 3),
                                                            round(1 / (service_rate - arrival_rate), 3)))
        print()

    def simulateMBP1(self, num_arrivals, trials, k, p, alpha):
        queue_times = []
        arrival = BoundedPareto(k, p, alpha)
        try:
            with open('k_{0}.pkl'.format(k), 'rb') as f:
                data = pickle.load(f)
                queue_times = data[0]
                avg_arrival_rate = data[1]
        except FileNotFoundError:
            avg_arrival_rate = 0
            for i in range(trials):
                t = 0
                jobs = []
                arrivals = [arrival.generate() for i in range(num_arrivals + 1)]
                arrival_rate = 1 / np.mean(arrivals)
                avg_arrival_rate += arrival_rate
                service_rate = arrival_rate / 0.8
                service = Exponential(service_rate)
                for i in range(num_arrivals + 1):
                    t += arrivals[i] if i != 0 else 0
                    jobs.append(Job(t, service.generate()))

                time = 0

                for job in jobs:
                    # if job was in queue
                    if time > job.arrival:
                        time += job.service_time
                    # if job just arrived and server is empty
                    else:
                        time = job.arrival + job.service_time
                    job.exit = time
                queue_times.append(jobs[-1].exit - jobs[-1].arrival - jobs[-1].service_time)
            avg_arrival_rate /= trials
            with open('k_{0}.pkl'.format(k), 'wb') as f:
                pickle.dump([queue_times, avg_arrival_rate], f)

        sample_mean = np.mean(queue_times)
        sample_var = sum([(queue_time - sample_mean) ** 2 for queue_time in queue_times]) / (len(queue_times) - 1)

        expected_mean = 0.8 / 0.2 * arrival.getNthMoment(2) / 2 / arrival.getNthMoment(1)
        expected_var = expected_mean ** 2 + avg_arrival_rate * arrival.getNthMoment(3) / 3 / 0.8

        print('M/BP/1 Queue')
        print('Alpha: {0}'.format(alpha))
        print('Sample Mean: {0}\tSample Var: {1}'.format(round(sample_mean, 3), round(sample_var, 3)))
        print('Expected Mean: {0}\tExpected Var: {1}'.format(round(expected_mean, 3), round(expected_var, 3)))
        print()


def Main():
    simulator = Simulator()
    # 4.3
    simulator.simulateMM1(2000, 200, 1, 0.5)
    simulator.simulateMM1(2000, 200, 2, 1)
    simulator.simulateMM1(2000, 200, 1, 0.7)
    simulator.simulateMM1(2000, 200, 1, 0.9)

    # 20.1
    simulator.simulateMBP1(50000, 5000, 1000, 10 ** 10, 1.5)
    simulator.simulateMBP1(50000, 5000, 1970, 10 ** 10, 2.9)


Main()
