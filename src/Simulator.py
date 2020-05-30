import numpy as np
import math
import random
import pickle
import queue as Q


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
        # proportional discrimination frequency measure
        self.m = 0
        self.n = None
        self.disfreq = None

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
        for i in range(num_arrivals):
            t += arrival.generate() if i != 0 else 0
            jobs.append(Job(t, service.generate()))

        eval(policy)(jobs)

        # for pickling purposes
        with open('{0}_exponential.pkl'.format(policy), 'wb') as f:
            pickle.dump(jobs, f)

    def simulateMBP1(self, num_arrivals, policy, k, p, alpha):
        arrival = BoundedPareto(k, p, alpha)
        t = 0
        jobs = []
        arrivals = [arrival.generate() for i in range(num_arrivals)]
        arrival_rate = 1 / np.mean(arrivals)

        # utilization fixed at 0.8
        service_rate = arrival_rate / 0.8
        service = Exponential(service_rate)

        for i in range(num_arrivals):
            t += arrivals[i] if i != 0 else 0
            jobs.append(Job(t, service.generate()))

        eval(policy)(jobs)
        # for pickling purposes
        filename = '{0}_pareto_lowvar.pkl'.format(policy) if alpha == 2.9 else '{0}_pareto_highvar.pkl'.format(policy)
        with open(filename, 'wb') as f:
            pickle.dump(jobs, f)


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

    for i, job in enumerate(jobs):
        j = i - 1
        while j >= 0:
            # job j was in system when job i arrived
            if jobs[j].exit > job.arrival:
                # job j has a greater service time (and remaining processing time) than job i
                if jobs[j].service_time > job.service_time and jobs[j].exit - job.arrival > job.service_time:
                    job.m += 1
            else:
                break
            j -= 1


def SRPT(jobs):
    # remaining processing time, job, index in jobs, service start time
    jobs_srpt = [[jobs[i].service_time, jobs[i], i, None] for i in range(len(jobs))]

    time = 0
    server = jobs_srpt[0]
    server[3] = time
    queue = Q.PriorityQueue()
    i = 1
    while queue.qsize() > 0 or i < len(jobs) or server:
        # all the jobs came in already
        if i >= len(jobs):
            time += server[0]
            jobs[server[2]].exit = time
            if queue.qsize() > 0:
                server = queue.get()
            else:
                server = None
        # server finishes before another job comes in
        elif time + server[0] <= jobs_srpt[i][1].arrival:
            time += server[0]
            jobs[server[2]].exit = time
            if queue.qsize() > 0:
                server = queue.get()
                server[3] = time
            else:
                server = jobs_srpt[i]
                time = server[1].arrival
                server[3] = time
                i += 1
        # job comes in before server finishes
        elif time + server[0] > jobs_srpt[i][1].arrival:
            time = jobs_srpt[i][1].arrival
            server[0] -= time - server[3]
            # cur job has less remaining processing time
            if server[0] <= jobs_srpt[i][0]:
                queue.put(jobs_srpt[i])
                server[3] = time
            # new job has less remaining processing time
            else:
                queue.put(server)
                server = jobs_srpt[i]
                server[3] = time
            i += 1


def Main():
    simulator = Simulator()

    simulator.simulateMM1(1000000, 'FCFS', 1, 0.8)
    simulator.simulateMBP1(1000000, 'FCFS', 1000, 10 ** 10, 1.5) # high var
    simulator.simulateMBP1(1000000, 'FCFS', 1970, 10 ** 10, 2.9) # low var

    simulator.simulateMM1(1000000, 'SRPT', 1, 0.8)
    simulator.simulateMBP1(1000000, 'SRPT', 1000, 10 ** 10, 1.5) # high var
    simulator.simulateMBP1(1000000, 'SRPT', 1970, 10 ** 10, 2.9) # low var


Main()
