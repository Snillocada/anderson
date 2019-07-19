import subprocess
from subprocess import PIPE

import matplotlib.pyplot as plt
import numpy as np

grains = 65
support = 5
population_num = 100000
degree = 3
epsilon = 0.0001
disorder = 15
average_type = "mean"

lambda_vec = np.linspace(-support,support,grains)+disorder

repeats = 30

sum_vec = np.zeros(grains)

for p in range(repeats):
        print(p)
        x = subprocess.run("~/anderson/code/mobility_edge.exe {} {} {} {} {} {} {}".format(grains, support, population_num,degree, epsilon, disorder, average_type),shell=True,stdout=PIPE).stdout.decode("utf-8").split(",")[:-1]
        mean_vec = [float(i) for i in x]
        sum_vec += np.array(mean_vec)

aver_vec = sum_vec/repeats

plt.plot(lambda_vec, aver_vec)
plt.title("Varied disorder for RRG pop_num = {}, degree {}".format(population_num,degree))
plt.xlabel("Disorder")
plt.ylabel("Spectral Density")
plt.savefig('mobility_edge_{}_D{}.png'.format(average_type, degree), bbox_inches='tight')
subprocess.run("gsutil mv mobility_edge_{}_D{}.png gs://anderson_loc/figures/".format(average_type, degree),shell=True)

average_type = "stddev"

lambda_vec = np.linspace(-support,support,grains)+disorder

repeats = 30

sum_vec = np.zeros(grains)

for p in range(repeats):
    print(p)
    x = subprocess.run("~/anderson/code/mobility_edge.exe {} {} {} {} {} {} {}".format(grains, support, population_num,degree, epsilon, disorder, average_type),shell=True,stdout=PIPE).stdout.decode("utf-8").split(",")[:-1]
    mean_vec = [float(i) for i in x]
    sum_vec += np.array(mean_vec)

aver_vec = sum_vec/repeats

plt.figure()
plt.plot(lambda_vec, aver_vec)
plt.title("Varied disorder for RRG pop_num = {}, degree {}".format(population_num,degree))
plt.xlabel("Disorder")   
plt.ylabel("Spectral Density") 
plt.savefig('mobility_edge_{}_D{}.png'.format(average_type, degree), bbox_inches='tight')

subprocess.run("gsutil mv mobility_edge_{}_D{}.png gs://anderson_loc/figures/".format(average_type, degree),shell=True)
