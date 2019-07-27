#! /usr/bin/env python3
import subprocess
from subprocess import PIPE

import matplotlib.pyplot as plt
import numpy as np
import sys

from numpy import linalg as LA
import networkx as nx

def main():

    grains = 151
    support = 8
    population_num = 5e3
    epsilon = 1e-100
    disorder = float(sys.argv[3])
    num_iterations = 3e2
    graph_type = "husimi"

    k = int(sys.argv[2])
    l = int(sys.argv[1])

    print("l = {}, k = {}".format(l,k))

    lambda_vec = np.linspace(-support, support, grains)

    repeats = 1

    sum_vec = np.zeros(grains)

    for p in range(repeats):
        x = subprocess.run(args = ["~/anderson/husimi/husimi.exe {} {} {} {} {} {} {} {}".format(grains, support, population_num, k, l, epsilon, disorder, num_iterations)], shell=True, stdout=PIPE).stdout.decode("utf-8").split(",")[:-1]

        mean_vec = [float(i) for i in x]
        sum_vec += np.array(mean_vec)
        print(p)

    aver_vec = sum_vec / repeats

    print('pop finished')

    plt.plot(lambda_vec, aver_vec,label='Pop Dynam')
    plt.title("Pop number {}, for {} disorder = {}, k={}, l={}".format(population_num, graph_type, disorder, k, l))
    plt.xlabel("Lambda")
    plt.ylabel("Spectral Density")
    plt.yscale('log')
    plt.legend()

    plt.savefig('pop_dynam_{}_W{}_L{}_K{}.png'.format(graph_type,disorder,l,k), bbox_inches='tight')

    subprocess.run("gsutil mv pop_dynam_{}_W{}_L{}_K{}.png gs://anderson_loc/husimi/figures/".format(graph_type,disorder,l,k),shell=True)

if __name__ == "__main__":
    main()
