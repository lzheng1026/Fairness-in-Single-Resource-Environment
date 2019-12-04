import pickle
import csv
from Simulator import Job
'''
Given a list of jobs, calculate the discrimination frequency
'''

# Loading Data
file_name = "FCFS_exponential"
full_file_name = file_name + ".pkl"
file = open(full_file_name, 'rb')
data = pickle.load(file)

# Paramters
throwout = 10000
length = len(data)
print("processing " + str(length-throwout) + " jobs\n")

disFreq_result = list()
counter = 0

for job_num in range(throwout, length):

    arrive_time = data[job_num].arrival
    end_time = data[job_num].exit
    job_size = data[job_num].service_time

    n = 0
    m = 0

    # calculate n - the number of jobs that came after it that ended before it
    for job_num_after in range(job_num, length):
        if data[job_num_after].exit < end_time:
            n+=1

    # calculate m - the number of jobs bigger than it that ends before it
    for job_num_before in range(throwout, job_num):
        if data[job_num_before].service_time > job_size:
            m+=1

    disFreq_result.append([m+n])

    counter+=1

    # temp save
    if counter%1000==0:
        with open(f'{counter-1000}-{counter}_{file_name}_disfreq_result.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerows(disFreq_result)


# save file
with open(f'{file_name}_disfreq_result.pkl', 'wb') as f:
    pickle.dump(disFreq_result, f)

with open(f'{file_name}_disfreq_result.csv', 'w') as fp:
    writer = csv.writer(fp)
    writer.writerows(disFreq_result)



