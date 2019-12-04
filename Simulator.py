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

    def __str__(self):
        return ("Arrival: {0}\tService Time:{1}\tExit Time:{2}".format(self.arrival, self.service_time, self.exit))


# job size distributions: exponential, bounded pareto(low var and high var), same job size, hyperexponential
# arrival process: poisson
# policies: SRPT (PS)
#           FCFS LCFS, SJF, LJF
# 1,000,000 jobs throw out 10,000
# fix utilization at 0.8

class Simulator:
    def simulateMM1(self, num_arrivals, policy, service_rate, arrival_rate):
        arrival = Exponential(arrival_rate)
        service = Exponential(service_rate)
        t = 0
        jobs = []
        for i in range(num_arrivals + 1):
            t += arrival.generate() if i != 0 else 0
            jobs.append(Job(t, service.generate()))

        eval(policy)(jobs)

        # for pickling purposes
        # with open('{0}_exponential.pkl'.format(policy), 'wb') as f:
        #     pickle.dump(jobs, f)

    def simulateMBP1(self, num_arrivals, policy, k, p, alpha):
        arrival = BoundedPareto(k, p, alpha)
        t = 0
        jobs = []
        arrivals = [arrival.generate() for i in range(num_arrivals + 1)]
        arrival_rate = 1 / np.mean(arrivals)

        # utilization fixed at 0.8
        service_rate = arrival_rate / 0.8
        service = Exponential(service_rate)

        for i in range(num_arrivals + 1):
            t += arrivals[i] if i != 0 else 0
            jobs.append(Job(t, service.generate()))

        eval(policy)(jobs)

        # for pickling purposes
        # with open('{0}_pareto_lowvar.pkl'.format(policy), 'wb') as f:
        #     pickle.dump(jobs, f)

# policies

def FCFS(jobs):
    time = 0
    for job in jobs:
        # if job was in queue
        if time > job.arrival:
            time += job.service_time
        # if job just arrived and server is empty
        else:
            time = job.arrival + job.service_time
        job.exit = time

def Main():
    simulator = Simulator()

    simulator.simulateMM1(1000000, 'FCFS', 1, 0.8)
    simulator.simulateMBP1(1000000, 'FCFS', 1000, 10 ** 10, 1.5)
    simulator.simulateMBP1(1000000, 'FCFS', 1970, 10 ** 10, 2.9)


Main()
