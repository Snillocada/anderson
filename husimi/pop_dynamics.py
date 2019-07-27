#! /usr/bin/env python3
import subprocess
from subprocess import PIPE

import matplotlib.pyplot as plt
import numpy as np
import sys
import csv

from numpy import linalg as LA
import networkx as nx

def main():

    grains = 151
    support = 5
    population_num = 5e3
    epsilon = 1e-20
    disorder = float(sys.argv[3])
    num_iterations = 2e2
    graph_type = "husimi"

    k = int(sys.argv[2])
    l = int(sys.argv[1])

    N = l*1000
    matrices = 20

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

    eig_vec = np.array([])
    for p in range(int(matrices/10)):
        print(p)
        for j in range(10):
            y = np.repeat(np.array(range(N)),k)
            curr_sum = 1
            while curr_sum != 0:
                A = np.zeros((N,N))
                for edge in np.random.permutation(y).reshape(-1,l):
                    A[edge[l-1]][edge[0]] = 1
                    A[edge[0]][edge[l-1]] = 1
                    for i in range(l-1):
                        A[edge[i]][edge[i+1]] = 1
                        A[edge[i+1]][edge[i]] = 1
                curr_sum = np.sum(np.sum(A,axis = 1) != k*(2))
            A += np.diag(np.random.uniform(-disorder/2,disorder/2,N))
        eig_vec = np.append(eig_vec,LA.eigvalsh(A))

    plt.plot(lambda_vec, aver_vec,label='Pop Dynam')
    plot = plt.hist(eig_vec,bins = 100, density=True, histtype = 'step',label='Numerical')
    plt.title("Pop number {}, for {} disorder = {}, k={}, l={}".format(population_num, graph_type, disorder, k, l))
    plt.xlabel("Lambda")
    plt.ylabel("Spectral Density")
#    plt.ylim(0,1.0)
    plt.yscale(sys.argv[4])
    plt.legend()

    plt.savefig('pop_dynam_{}_W{}_L{}_K{}.png'.format(graph_type,disorder,l,k), bbox_inches='tight')

    subprocess.run("gsutil mv pop_dynam_{}_W{}_L{}_K{}.png gs://anderson_loc/husimi/figures/".format(graph_type,disorder,l,k),shell=True)

    with open('pop_dynam_{}_W{}_L{}_K{}_pop_data.csv'.format(graph_type,disorder,l,k),'w') as myfile1:
        wr1 = csv.writer(myfile1, quoting=csv.QUOTE_ALL)
        wr1.writerow(aver_vec.tolist())

    with open('pop_dynam_{}_W{}_L{}_K{}_mat_data.csv'.format(graph_type,disorder,l,k),'w') as myfile2:
        wr2 = csv.writer(myfile2, quoting=csv.QUOTE_ALL)
        wr2.writerow(eig_vec.tolist())

if __name__ == "__main__":
    main()
