import subprocess
from subprocess import PIPE

import matplotlib.pyplot as plt
import numpy as np
import csv

grains = 513
support = 15
population_num = 50000
degree = 3
epsilon_vec = [0.001,0.0001,0.00001]
disorder = 10

lambda_vec = np.linspace(-support,support,grains)

repeats = 100
inde = 1
for epsilon in epsilon_vec:
    inde += 1
    sum_vec = np.zeros(grains)
    for p in range(repeats):
        print(p)
        x = subprocess.run("~/anderson/code/IPR.exe {} {} {} {} {} {}".format(grains, support, population_num, degree, epsilon, disorder),shell=True,stdout=PIPE).stdout.decode("utf-8").split(",")[:-1]
        mean_vec = [float(i) for i in x]
        sum_vec += np.array(mean_vec)
    aver_vec = sum_vec/repeats
    with open('IPR_W{}_D{}_data_{}.csv'.format(disorder, degree,inde),'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(aver_vec.tolist())
            
    plt.plot(lambda_vec, aver_vec, label="eta = {}".format(epsilon))
plt.title("IPR for RRG disorder = {}, degree {}".format(disorder, degree))
plt.xlabel("Lambda")
plt.ylabel("Spectral Density")
plt.yscale('log')
plt.legend()
plt.savefig('IPR_W{}_D{}.png'.format(disorder, degree), bbox_inches='tight')
subprocess.run("gsutil mv IPR_W{}_D{}.png gs://anderson_loc/figures/".format(disorder, degree),shell=True)
