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

    grains = 201
    support = 0.3
    population_num = 5e3+1
    epsilon = 1e-5
    num_iterations = 1e2
    graph_type = "husimi"
    translation = -2

    k = int(sys.argv[2])
    l = int(sys.argv[1])

    N = l*10
    matrices = 20

    print("l = {}, k = {}".format(l,k))

    lambda_vec = np.linspace(-support+translation, support+translation, grains)
    for disorder_vec in range(1):

        disorder = 0.4

        x = subprocess.run(args = ["~/anderson/husimi/translate.exe {} {} {} {} {} {} {} {} {}".format(grains, support, population_num, k, l, epsilon, disorder, num_iterations,translation)], shell=True, stdout=PIPE).stdout.decode("utf-8").split(",")[:-1]

        aver_vec = [float(i) for i in x]

#        eig_vec = np.array([])
#        for p in range(int(matrices/10)):
#            print(p)
#            for j in range(10):
#                y = np.repeat(np.array(range(N)),k)
#                curr_sum = 1
#                while curr_sum != 0:
#                    A = np.zeros((N,N))
#                    for edge in np.random.permutation(y).reshape(-1,l):
#                        A[edge[l-1]][edge[0]] = 1
#                        A[edge[0]][edge[l-1]] = 1
#                        for i in range(l-1):
#                            A[edge[i]][edge[i+1]] = 1
#                            A[edge[i+1]][edge[i]] = 1
#                    curr_sum = np.sum(np.sum(A,axis = 1) != k*(2))
#                A += np.diag(np.random.uniform(-disorder/2,disorder/2,N))
#            eig_vec = np.append(eig_vec,LA.eigvalsh(A))

        plt.plot(lambda_vec, aver_vec,label='Pop Dynam_{}'.format(disorder))
#        plot = plt.hist(eig_vec,bins = 100, density=True, histtype = 'step',label='Numerical_{}'.format(disorder))
        print('dis = {}'.format(disorder))

    plt.title('Pop number {}, for {} k={}, l={}'.format(population_num, graph_type, k, l))
    plt.xlabel("Lambda")
    plt.ylabel("Spectral Density")
#    plt.ylim(0,2.0)
    plt.yscale('log')
    plt.legend()

    plt.savefig('sml_dis_pop_{}_{}_L{}_K{}.png'.format(graph_type,population_num,l,k), bbox_inches='tight')

    subprocess.run('gsutil mv sml_dis_pop_{}_{}_L{}_K{}.png gs://anderson_loc/husimi/figures/'.format(graph_type,population_num,l,k),shell=True)

if __name__ == "__main__":
    main()
