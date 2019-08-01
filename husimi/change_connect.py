import subprocess
from subprocess import PIPE

import matplotlib.pyplot as plt
import numpy as np
import csv
import sys

grains = 50
support = 6
population_num = 2e2
k_top = int(sys.argv[1])
degree = k_top
k_vec = list((np.array(range(k_top)) + 2))
epsilon = 1e-100 
disorder_start = int(sys.argv[2])
disorder_end = int(sys.argv[3])
print("Disorder from {} to {} with {} grains".format(disorder_start, disorder_end, grains))
average_type = "mean"
start_wait = int(4e2)
num_iterations = int(2e2)
energy = 0
plt.figure(figsize = (12,9))
for k in k_vec:
    l = 4
    disorder_vec = np.linspace(disorder_start,disorder_end,grains)
    time_aver_vec = np.array([])
    print("L = {}, K = {}".format(l,k))
    for disorder in disorder_vec:
        x = subprocess.run("~/anderson/husimi/time_aver.exe {} {} {} {} {} {} {} {} {} {}".format(grains, support, population_num, k, l, epsilon, disorder, num_iterations, energy, start_wait),shell=True,stdout=PIPE).stdout.decode("utf-8").split(",")[:-1]
        res_vec = np.array([float(i) for i in x])
        time_aver = np.average(res_vec)
        if time_aver < 1e-20:
            time_aver = 1e-20
        time_aver_vec = np.append(time_aver_vec, time_aver)
        print("Disorder = {}".format(disorder))
    
    p = plt.plot(disorder_vec, time_aver_vec,label='L={}, K={}'.format(l,k))
    
    l = 2 
    k2 = 2*k
    time_aver_vec = np.array([])
    print("L = {}, K = {}".format(l,k2))
    for disorder in disorder_vec:
        x = subprocess.run("~/anderson/husimi/time2_aver.exe {} {} {} {} {} {} {}".format(num_iterations*10,support, population_num*10, k2, epsilon, disorder, start_wait*10),shell=True,stdout=PIPE).stdout.decode("utf-8").split(",")[:-1]
        res_vec = np.array([float(i) for i in x])
        time_aver = np.average(res_vec)
        if time_aver < 1e-20:
            time_aver = 1e-20
        time_aver_vec = np.append(time_aver_vec, time_aver)
        print("Disorder = {}".format(disorder))
    
    p = plt.plot(disorder_vec, time_aver_vec,linestyle='dashed',color = p[-1].get_color(), label = 'L={}, K={}'.format(l,k2))
#plt.plot(disorder_vec, half_time_aver, '.', label='Time Aver of second half')
plt.title("Time average after {} iterations over {} iterations against disorder for husimi varied L".format(start_wait, num_iterations))
plt.xlabel("Disorder")
plt.legend()
plt.ylabel("Time averaged mean imaginary part of resolvent")
plt.yscale('log')
plt.savefig('varied_degree_{}_P{}_K{}_S{}.png'.format(average_type, population_num, degree, disorder_start), bbox_inches='tight')

subprocess.run("gsutil mv varied_degree_{}_P{}_K{}_S{}.png gs://anderson_loc/husimi/mob_edge/k{}/".format(average_type, population_num, degree, disorder_start, k),shell=True)

