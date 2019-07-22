import subprocess
from subprocess import PIPE

import matplotlib.pyplot as plt
import numpy as np
import csv

grains = 100
support = 6
population_num = 100000
degree = 3
epsilon = 0.000000001
disorder = 17
average_type = "mean"

lambda_vec = np.linspace(-support,support,grains)+disorder

repeats = 150

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
plt.yscale('log')
plt.savefig('mobility_edge_{}_D{}.png'.format(average_type, disorder), bbox_inches='tight')

with open('mobility_edge_{}_D{}_data.csv'.format(average_type, disorder),'w') as myfile1:
    wr1 = csv.writer(myfile1, quoting=csv.QUOTE_ALL)
    wr1.writerow(aver_vec.tolist())

subprocess.run("gsutil mv mobility_edge_{}_D{}.png gs://anderson_loc/figures/".format(average_type, disorder),shell=True)
subprocess.run("gsutil mv mobility_edge_{}_D{}_data.csv gs://anderson_loc/data/".format(average_type, disorder),shell=True)

average_type = "stddev"

lambda_vec = np.linspace(-support,support,grains)+disorder

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
plt.yscale('log')
plt.savefig('mobility_edge_{}_D{}.png'.format(average_type, disorder), bbox_inches='tight')

with open('mobility_edge_{}_D{}_data.csv'.format(average_type, disorder),'w') as myfile2:
    wr2 = csv.writer(myfile2, quoting=csv.QUOTE_ALL)
    wr2.writerow(aver_vec.tolist())

subprocess.run("gsutil mv mobility_edge_{}_D{}.png gs://anderson_loc/figures/".format(average_type, disorder),shell=True)
subprocess.run("gsutil mv mobility_edge_{}_D{}_data.csv gs://anderson_loc/data/".format(average_type, disorder),shell=True)
