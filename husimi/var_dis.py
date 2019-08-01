import subprocess
from subprocess import PIPE

import matplotlib.pyplot as plt
import numpy as np
import csv
import sys

grains = 25
support = 6
population_num = 4e2
k = int(sys.argv[2])
l_top = int(sys.argv[1])
epsilon = 1e-100 
disorder_start = 18
disorder_end = 30
print("Disorder from {} to {} with {} grains".format(disorder_start, disorder_end, grains))
average_type = "mean"
start_wait = int(5e2)
num_iterations = int(2e2)
energy = 0

for i in range(int(l_top/2)-1):
    l = 2*(i+1) + 2
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

    plt.plot(disorder_vec, time_aver_vec,label='L={}'.format(l))
    #plt.plot(disorder_vec, half_time_aver, '.', label='Time Aver of second half')
plt.title("Time average after {} iterations over {} iterations against disorder for husimi varied L,K{}".format(start_wait, num_iterations,k))
plt.xlabel("Disorder")
plt.legend()
plt.ylabel("Time averaged mean imaginary part of resolvent")
plt.yscale('log')
plt.savefig('varied_aver_{}_P{}_L_top{}_S{}.png'.format(average_type, population_num, l_top, disorder_start), bbox_inches='tight')

subprocess.run("gsutil mv varied_aver_{}_P{}_L_top{}_S{}.png gs://anderson_loc/husimi/mob_edge/k{}/".format(average_type, population_num, l_top, disorder_start, k),shell=True)

