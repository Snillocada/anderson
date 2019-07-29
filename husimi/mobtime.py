import subprocess
from subprocess import PIPE

import matplotlib.pyplot as plt
import numpy as np
import csv
import sys

grains = int(sys.argv[4])
support = 6
population_num = 1e2
k = 2
l = sys.argv[1]
epsilon = 1e-100 
disorder_start = int(sys.argv[2])
disorder_end = int(sys.argv[3])
print("Disorder from {} to {} with {} grains".format(disorder_start, disorder_end, grains))
average_type = "mean"
start_wait = int(2e2)
num_iterations = int(2e2)
energy = 0

disorder_vec = np.linspace(disorder_start,disorder_end,grains)
time_aver_vec = np.array([])
half_time_aver = np.array([])
print("L = {}, K = {}".format(l,k))
for disorder in disorder_vec:
    x = subprocess.run("~/anderson/husimi/time_aver.exe {} {} {} {} {} {} {} {} {} {}".format(grains, support, population_num, k, l, epsilon, disorder, num_iterations, energy, start_wait),shell=True,stdout=PIPE).stdout.decode("utf-8").split(",")[:-1]
    res_vec = np.array([float(i) for i in x])
    half_res_vec = res_vec[int(len(res_vec)/2):len(res_vec)]
    half_time_aver = np.append(half_time_aver, np.average(half_res_vec))
    time_aver_vec = np.append(time_aver_vec, np.average(res_vec))
    print("Disorder = {}".format(disorder))

plt.plot(disorder_vec, time_aver_vec,label='Time Average of total')
plt.plot(disorder_vec, half_time_aver, '.', label='Time Aver of second half')
plt.title("Time average after {} iterations over {} iterations against disorder for husimi L{},K{}".format(start_wait, num_iterations,l,k))
plt.xlabel("Disorder")
plt.legend()
plt.ylabel("Time averaged mean imaginary part of resolvent")
plt.yscale('log')
plt.savefig('time_aver_{}_P{}_L{}_S{}.png'.format(average_type, population_num, l, disorder_start), bbox_inches='tight')

subprocess.run("gsutil mv time_aver_{}_P{}_L{}_S{}.png gs://anderson_loc/husimi/mob_edge/k{}/".format(average_type, population_num, l, disorder_start, k),shell=True)

