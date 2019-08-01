import numpy as np
from numpy import linalg as LA
import networkx as nx
import matplotlib.pyplot as plt
import math
import sys
import subprocess
from subprocess import PIPE

from functools import reduce

def factors(n): 
    return set(reduce(list.__add__, 
        ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

N_vec = [9240*3,9240*2]
plt.figure(figsize=(15,10))  
for N in N_vec:
    fact_list = list(factors(N))[3:-1]
    fact_list.sort()
    fact_list = fact_list[0::3]

    k = 4
    l = 2

    dis = 22
    x= np.repeat(np.array(range(N)),k)
    curr_sum = 1
    while curr_sum != 0:
        A = np.zeros((N,N))
        for edge in np.random.permutation(x).reshape(-1,l):
            A[edge[l-1]][edge[0]] = 1
            A[edge[0]][edge[l-1]] = 1
            for i in range(l-1):
                A[edge[i]][edge[i+1]] = 1
                A[edge[i+1]][edge[i]] = 1
                #     curr_sum = 0
        curr_sum = np.sum(np.sum(A,axis = 1) != k)
    
    A += np.diag(np.random.uniform(-(dis/2), dis/2, N))
    
    print('yeet')
    
    vals, vecs = LA.eigh(A)
    
    # print(dist)
    x = vecs[0]
    IPR = 1/(np.dot(np.multiply(x,x),np.multiply(x,x)))
    print(IPR)
    
    IPR_vec = np.array([IPR])
    
    k = 2
    
    for l in fact_list:
        x= np.repeat(np.array(range(N)),k)
        curr_sum = 1
        while curr_sum != 0:
            A = np.zeros((N,N))
            for edge in np.random.permutation(x).reshape(-1,l):
                A[edge[l-1]][edge[0]] = 1
                A[edge[0]][edge[l-1]] = 1
                for i in range(l-1):
                    A[edge[i]][edge[i+1]] = 1
                    A[edge[i+1]][edge[i]] = 1
                    #     curr_sum = 0
            curr_sum = np.sum(np.sum(A,axis = 1) != k*2)
        A += np.diag(np.random.uniform(-(dis/2), dis/2, N))

        print('L={}'.format(l))

        vals, vecs = LA.eigh(A)

    # print(dist)
        x = vecs[0]
        IPR = 1/(np.dot(np.multiply(x,x),np.multiply(x,x)))
        print(IPR)
        IPR_vec = np.append(IPR_vec,IPR)
    
    fact_list = np.append(np.array([2]),fact_list)
    plt.plot(fact_list, IPR_vec,label = "N = {}".format(N))
plt.xscale('log')
plt.title('IPR against loop size for disorder {} for matrix size {}'.format(dis, N))
plt.ylabel('IPR')
plt.xlabel('Loop size')
plt.legend()

plt.savefig('IPR_dis{}_Nvec.png'.format(dis))

subprocess.run("gsutil mv IPR_dis{}_Nvec.png gs://anderson_loc/husimi/ipr/k{}/".format(dis,k),shell=True)
