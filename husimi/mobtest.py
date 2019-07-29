import subprocess
from subprocess import PIPE

import matplotlib.pyplot as plt
import numpy as np
import csv

grains = 20
support = 6
population_num = 1e3
k = 2
l = 6
epsilon = 1e-100 
disorder_start = 20
disorder_end = 30
average_type = "mean"
start_wait = int(2e3)
num_iterations = int(1e3)
energy = 0

disorder_vec = np.linspace(disorder_start,disorder_end,grains)
time_aver_vec = np.array([])
print("L = {}, K = {}".format(l,k))
for disorder in disorder_vec:
    x = subprocess.run("~/anderson/husimi/time_aver.exe {} {} {} {} {} {} {} {} {} {}".format(grains, support, population_num, k, l, epsilon, disorder, num_iterations, energy, start_wait),shell=True,stdout=PIPE).stdout.decode("utf-8").split(",")[:-1]
    res_vec = np.array([float(i) for i in x])
    time_aver_vec = np.append(time_aver_vec, np.average(res_vec))
    print("Disorder = {}".format(disorder))

plt.plot(disorder_vec, time_aver_vec)
plt.title("Time average after {} iterations over {} iterations against disorder for husimi L{},K{}".format(start_wait, num_iterations,l,k))
plt.xlabel("Disorder")
plt.ylabel("Time averaged mean imaginary part of resolvent")
plt.yscale('log')
plt.savefig('time_aver_{}_P{}_L{}_K{}.png'.format(average_type, population_num, l, k), bbox_inches='tight')

subprocess.run("gsutil mv time_aver_{}_P{}_L{}_K{}.png gs://anderson_loc/husimi/mob_edge/".format(average_type, population_num, l, k),shell=True)
