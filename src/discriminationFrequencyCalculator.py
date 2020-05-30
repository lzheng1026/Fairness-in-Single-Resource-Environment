import pickle
import csv
from Simulator import Job
import time

'''
Given a list of jobs, calculate the discrimination frequency
'''

# Loading Data
file_names = ["FCFS_exponential.pkl",'FCFS_pareto_highvar.pkl', 'FCFS_pareto_lowvar.pkl', 'SRPT_exponential.pkl', 'SRPT_pareto_highvar.pkl',
              'SRPT_pareto_lowvar.pkl']
#full_file_name = file_name + ".pkl"
for full_file_name in file_names:
    file_name = full_file_name[:-4]
    file = open(full_file_name, 'rb')
    data = pickle.load(file)

    # Paramters
    throwout = 10000
    length = len(data)

    disFreq_result = ['m','n','df']
    counter = 0

    for job_num in range(throwout, length):

        start = time.time()

        arrive_time = data[job_num].arrival
        end_time = data[job_num].exit
        job_size = data[job_num].service_time

        # calculate n - the number of jobs that came after it that ended before it
        n = 0
        if 'FCFS' not in file_name:
            for job_num_after in range(job_num + 1, length):
                if end_time < data[job_num_after].arrival:
                    break
                if data[job_num_after].exit < end_time:
                    n += 1
        data[job_num].n = n

        # calculate m
        m = data[job_num].m

        # calculate dis freq
        data[job_num].disfreq = m + n

        # append result to list
        result = [m, n, m + n]
        disFreq_result.append(result)

        # time
        end = time.time()

        counter += 1

    # save file
    # with open(f'{file_name}_disfreq_result.pkl', 'wb') as f:
    #     pickle.dump(disFreq_result, f)

    with open(f'{file_name}_disfreq_result.csv', 'w') as fp:
        writer = csv.writer(fp)
        writer.writerows(disFreq_result)

    file.close()
