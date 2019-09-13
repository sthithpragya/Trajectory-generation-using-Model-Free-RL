from .computeMM_separately import *
from itertools import chain
from .computeGG import *
from .Z1_func import *
from .Z2_func import *

import numpy as np
from math import *
    
def compute_alphaddot(N_mod,alpha_in,F1,F2,b,L):

    alpha = [0]*N_mod
    for j in range(N_mod):
        alpha[j] = alpha_in[j]

    M = computeMM_separately(alpha)
    
    G = computeGG(alpha)

    Q_forces = np.zeros((N_mod,1))

    for j in range(N_mod):

        Z1 = Z1_func(alpha[j],b[j],L[j])
        Z2 = Z2_func(alpha[j],b[j],L[j])

        Q_forces[j] = np.dot(Z1,F1[j]) + np.dot(Z2,F2[j])    
    
    alphaddot = np.dot(np.linalg.inv(M),(Q_forces - G))
    alphaddot = list(chain.from_iterable(alphaddot))
    return alphaddot
    
# print(compute_alphaddot(3,[pi/4,pi/5,pi/3],[10,10,10],[20,20,20],[0.1,0.1,0.1],[0.2,0.2,0.2]).tolist())
# print(compute_alphaddot(3,[0,0,0],[1,1,1],[-1,-1,-1],[0.1,0.1,0.1],[0.2,0.2,0.2]))