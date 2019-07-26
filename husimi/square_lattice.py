import numpy as np
from numpy import linalg as LA
import networkx as nx
import matplotlib.pyplot as plt
import subprocess
import sys

def main():
    N = int(sys.argv[1])
    dim = int(sys.argv[2])

    print("N={}, dim={}".format(N,dim))

    plane_node_number = pow(N,2)

    x = np.zeros([plane_node_number,plane_node_number])
    y = np.append(np.ones(N-1),[0])
    np.fill_diagonal(x[1:],y)
    np.fill_diagonal(x[:,1:],y)
    np.fill_diagonal(x[N:],1)
    np.fill_diagonal(x[:,N:],1)
    if dim == 3:
        for i in range(N):
            if i == 0:
                mat = x
            elif i == 1:
                mat = np.identity(N*N)
            else:
                mat = np.zeros([N*N,N*N])
            for j in range(N-1):
                if j == i:
                    mat = np.append(mat,np.identity(N*N),axis = 1)
                elif (j == i-1) or (j == i+1):
                    mat = np.append(mat,x,axis = 1)
                else:
                    mat = np.append(mat,np.zeros([N*N,N*N]),axis = 1)
            if i == 0:
                final_mat = mat
            else:
                final_mat = np.append(final_mat,mat,axis=0)
    elif dim ==2:
        final_mat = x
    plt.hist(LA.eigvalsh(final_mat),bins = int(pow(2,dim)*N), density=True)
    plt.title("Spectral Density for a square lattice with {} hypercubes in dimension {}".format(N,dim))
    plt.ylabel('Spectral Density')
    plt.xlabel('Lambda')
    plt.show()
    plt.savefig('square_lattice_N={}_dim={}.png'.format(N,dim),bbox_inches='tight')
    subprocess.run("gsutil mv square_lattice_N={}_dim={}.png gs://anderson_loc/square/".format(N,dim),shell=True)
    
if __name__=="__main__":
    main()
