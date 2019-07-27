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
    num_iterations = 2e2
    graph_type = "husimi"

    k = int(sys.argv[2])
    l = int(sys.argv[1])
    c_top = int(sys.argv[3])

    N = l*500
    matrices = 100

    print("l = {}, k = {}".format(l,k))
    for c_expo in range(c_top):
        c = pow(2,c_expo)
        print("c={}".format(c))
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
                A += c*np.identity(N)
            eig_vec = np.append(eig_vec,LA.eigvalsh(A))

        plot = plt.hist(eig_vec,bins = 100, density=True, histtype = 'step',label='c={}'.format(c))
    plt.title("N={}, for {}, k={}, l={}".format(N,graph_type,k,l))
    plt.xlabel('Lambda')
    plt.ylabel('Spectral Density')
    plt.legend()
    plt.ylim(0,1)
    plt.savefig('varied_disorder_{}_c_top{}_L{}_K{}.png'.format(graph_type,c_top,l,k), bbox_inches='tight')

    subprocess.run("gsutil mv varied_disorder_{}_c_top{}_L{}_K{}.png gs://anderson_loc/husimi/figures/".format(graph_type,c_top,l,k),shell=True)

if __name__ == "__main__":
    main()
