import subprocess
from subprocess import PIPE

import matplotlib.pyplot as plt
import numpy as np

grains = 100
support = 6
population_num = 5e5
degree = 3
epsilon = 1e-150
disorder = 15
average_type = "mean"
energy = 3.0
num_iterations = 1e3

lambda_vec = np.linspace(-support,support,grains)+disorder

repeats = 1

sum_vec = np.zeros(grains)
for p in range(repeats):
        x = subprocess.run("~/anderson/code/mobility_edge.exe {} {} {} {} {} {} {} {} {}".format(grains, support, population_num,degree, epsilon, disorder, average_type, energy, num_iterations),shell=True,stdout=PIPE).stdout.decode("utf-8").split(",")[:-1]
        mean_vec = [float(i) for i in x]
        sum_vec += np.array(mean_vec)

aver_vec = sum_vec/repeats

plt.plot(lambda_vec, aver_vec)
plt.title("Varied disorder pop_num = {}, Iterations = {},  energy {}".format(population_num,num_iterations, energy))
plt.xlabel("Disorder")
plt.ylabel("Spectral Density")
plt.yscale('log')
plt.savefig('mobility_edge_{}_E{}.png'.format(average_type, energy), bbox_inches='tight')
subprocess.run("gsutil mv mobility_edge_{}_E{}.png gs://anderson_loc/figures/".format(average_type, energy),shell=True)

#average_type = "stddev"
#
#lambda_vec = np.linspace(-support,support,grains)+disorder
#
#sum_vec = np.zeros(grains)
#
#for p in range(repeats):
#    print(p)
#    x = subprocess.run("~/anderson/code/mobility_edge.exe {} {} {} {} {} {} {}".format(grains, support, population_num,degree, epsilon, disorder, average_type),shell=True,stdout=PIPE).stdout.decode("utf-8").split(",")[:-1]
#    mean_vec = [float(i) for i in x]
#    sum_vec += np.array(mean_vec)
#
#aver_vec = sum_vec/repeats

#plt.figure()
#plt.plot(lambda_vec, aver_vec)
#plt.title("Varied disorder for RRG pop_num = {}, degree {}".format(population_num,degree))
#plt.xlabel("Disorder")   
#plt.ylabel("Spectral Density") 
#plt.savefig('mobility_edge_{}_D{}.png'.format(average_type, degree), bbox_inches='tight')

#subprocess.run("gsutil mv mobility_edge_{}_D{}.png gs://anderson_loc/figures/".format(average_type, degree),shell=True)
