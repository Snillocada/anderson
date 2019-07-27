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

    grains = 156
    support = 0.225
    population_num = 5e2
    epsilon = 1e-5
    num_iterations = 5e2
    graph_type = "husimi"
    translation = -2

    k = int(sys.argv[2])
    l = int(sys.argv[1])

    N = l*10
    matrices = 20

    print("l = {}, k = {}".format(l,k))

    lambda_vec = np.linspace(translation, support+translation, grains)
    output_vec = np.array([])
    dis_vec = np.array([])
    for disorder_vec in range(70):

        disorder = disorder_vec/200
        dis_vec = np.append(dis_vec,disorder)

        x = subprocess.run(args = ["~/anderson/husimi/translate.exe {} {} {} {} {} {} {} {} {}".format(grains, support, population_num, k, l, epsilon, disorder, num_iterations,translation)], shell=True, stdout=PIPE).stdout.decode("utf-8").split(",")[:-1]

        aver_vec = [float(i) for i in x]

        gap_end = lambda_vec[np.searchsorted(aver_vec,1e-3)]
        gap_start = np.flip(lambda_vec)[np.searchsorted(np.flip(aver_vec),1e-3)]
#        print("GS -> {}, GE -> {}".format(gap_start,gap_end)) 
        if (gap_end == -2.0):
            gap_width = 0
        else:
            gap_width = gap_end-gap_start
        output_vec = np.append(output_vec,gap_width)

        print('dis = {}'.format(disorder))

    plt.plot(dis_vec, output_vec)
    plt.title('Gap width against disorder, pop {}, for {} k={}, l={}'.format(population_num, graph_type, k, l))
    plt.xlabel("Disorder")
    plt.ylabel("Gap Width")

    plt.savefig('gap_width_pop_{}_{}_L{}_K{}.png'.format(graph_type,population_num,l,k), bbox_inches='tight')

    subprocess.run('gsutil mv gap_width_pop_{}_{}_L{}_K{}.png gs://anderson_loc/husimi/figures/'.format(graph_type,population_num,l,k),shell=True)

if __name__ == "__main__":
    main()
