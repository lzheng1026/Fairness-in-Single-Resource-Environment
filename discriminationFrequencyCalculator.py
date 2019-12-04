import pickle
from Simulator import Job
'''
Given a list of jobs, calculate the discrimination frequency
'''

# Loading Data
file_name = ""
file = open(file_name, 'rb')
data = pickle.load(file)
length = len(data)

# Paramters
throwout = 10000
# self.arrival = arrival
# self.service_time = service_time
# self.exit = None

disFreq = dict()

for job_num in range(throwout, length):

    print(str(data[job_num].arrival))
    print(str(data[job_num].service_time))
    print(str(data[job_num].exit))
    break

    # calculate n - the number of jobs that came after it that ended before it
    # for num_job_after in range(job_num, length):
    #     pass
