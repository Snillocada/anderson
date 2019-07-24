import subprocess
from subprocess import PIPE

import matplotlib.pyplot as plt
import numpy as np
import csv

grains = 100
support = 6
population_num = 5e8
degree = 3
epsilon = 1e-100 
disorder = 16.5
average_type = "mean"

lambda_vec = np.linspace(0,population_num*300,300)

repeats = 1

sum_vec = np.zeros(600)

x = subprocess.run("~/anderson/code/mob_edge_fix_dis.exe {} {} {} {} {} {} {}".format(grains, support, population_num,degree, epsilon, disorder, average_type),shell=True,stdout=PIPE).stdout.decode("utf-8").split(",")[:-1]
mean_vec = [float(i) for i in x]
sum_vec += np.array(mean_vec)

aver_vec = sum_vec/repeats

exp_vec = aver_vec[0::2]
var_vec = aver_vec[1::2]

plt.plot(lambda_vec, exp_vec)
plt.title("Change in mean Im of resolvent for RRG pop_num = {}, disorder {}".format(population_num,disorder))
plt.xlabel("Num of Iterates")
plt.ylabel("Mean imaginary part of resolvent")
plt.yscale('log')
plt.savefig('mobility_mean_{}_D{}.png'.format(average_type, disorder), bbox_inches='tight')

plt.figure()
plt.plot(lambda_vec, var_vec)
plt.title("Change in var Im of resolvent for RRG pop_num = {}, disorder {}".format(population_num,disorder))
plt.xlabel("Num of Iterates")
plt.ylabel("Var imaginary part of resolvent")
plt.yscale('log')
plt.savefig('mobility_var_{}_D{}.png'.format(average_type, disorder), bbox_inches='tight')

with open('mobility_mean_{}_D{}_data.csv'.format(average_type, disorder),'w') as myfile1:
    wr1 = csv.writer(myfile1, quoting=csv.QUOTE_ALL)
    wr1.writerow(exp_vec.tolist())

with open('mobility_var_{}_D{}_data.csv'.format(average_type, disorder),'w') as myfile1:
    wr1 = csv.writer(myfile1, quoting=csv.QUOTE_ALL)
    wr1.writerow(var_vec.tolist())

subprocess.run("gsutil mv mobility_mean_{}_D{}.png gs://anderson_loc/figures/".format(average_type, disorder),shell=True)
subprocess.run("gsutil mv mobility_mean_{}_D{}_data.csv gs://anderson_loc/data/".format(average_type, disorder),shell=True)

subprocess.run("gsutil mv mobility_var_{}_D{}.png gs://anderson_loc/figures/".format(average_type, disorder),shell=True)
subprocess.run("gsutil mv mobility_var_{}_D{}_data.csv gs://anderson_loc/data/".format(average_type, disorder),shell=True)
