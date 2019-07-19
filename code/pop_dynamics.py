#! /usr/bin/env python3
import subprocess
from subprocess import PIPE

import matplotlib.pyplot as plt
import numpy as np

grains = 256
support = 7
population_num = 1000000
degree = 3
epsilon = 0.003
disorder = 20
graph_type = "RRG"

lambda_vec = np.linspace(-support, support, grains)

repeats = 16

sum_vec = np.zeros(grains)

for p in range(repeats):
    x = subprocess.run(args = ["~/anderson/code/pop_dynam.exe {} {} {} {} {} {}".format(grains, support, population_num, degree, epsilon, disorder)], shell=True, stdout=PIPE).stdout.decode("utf-8").split(",")[:-1]

    mean_vec = [float(i) for i in x]
    sum_vec += np.array(mean_vec)
    print(p)

aver_vec = sum_vec / repeats

plt.plot(lambda_vec, aver_vec)
plt.title("Pop number {}, epsilon {} for {} disorder = {}, degree {}".format(population_num, epsilon, graph_type,
                                                                             disorder, degree))
plt.xlabel("Lambda")
plt.ylabel("Spectral Density")

plt.savefig('pop_dynam_{}_W{}_D{}.png'.format(graph_type,disorder, degree), bbox_inches='tight')

subprocess.run("gsutil mv pop_dynam_{}_W{}_D{}.png gs://anderson_loc/figures/".format(graph_type,disorder, degree),shell=True)
