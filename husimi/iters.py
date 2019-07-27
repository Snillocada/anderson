import subprocess
from subprocess import PIPE

import matplotlib.pyplot as plt
import numpy as np
import csv

grains = 100
support = 6
population_num = 5e3
k = 2
l = 4
epsilon = 1e-100 
disorder = 16
average_type = "mean"
num_iterations = 2000
energy = 0

lambda_vec = np.linspace(0,population_num*num_iterations,num_iterations)

repeats = 1

sum_vec = np.zeros(num_iterations)

x = subprocess.run("~/anderson/husimi/no_iters.exe {} {} {} {} {} {} {} {} {}".format(grains, support, population_num, k, l, epsilon, disorder, num_iterations, energy),shell=True,stdout=PIPE).stdout.decode("utf-8").split(",")[:-1]
mean_vec = [float(i) for i in x]
sum_vec += np.array(mean_vec)

aver_vec = sum_vec/repeats

exp_vec = aver_vec

plt.plot(lambda_vec, exp_vec)
plt.title("Change in mean Im of resolvent for husimi pop_num = {}, disorder {}".format(population_num,disorder))
plt.xlabel("Num of Iterates")
plt.ylabel("Mean imaginary part of resolvent")
plt.yscale('log')
plt.savefig('mobility_{}_D{}.png'.format(average_type, disorder), bbox_inches='tight')

with open('mobility_{}_D{}_data.csv'.format(average_type, disorder),'w') as myfile1:
    wr1 = csv.writer(myfile1, quoting=csv.QUOTE_ALL)
    wr1.writerow(exp_vec.tolist())

subprocess.run("gsutil mv mobility_{}_D{}.png gs://anderson_loc/husimi/iters/".format(average_type, disorder),shell=True)
subprocess.run("gsutil mv mobility_{}_D{}_data.csv gs://anderson_loc/husimi/data/".format(average_type, disorder),shell=True)
