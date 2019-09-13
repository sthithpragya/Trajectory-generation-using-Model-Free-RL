from .computeMM_separately import *
from .computeGG import *
from .Z1_func import *
from .Z2_func import *

import numpy as np
from math import *

def compute_forces(N_mod,alpha_in,alphaddot,b,L,Fmin):

    alpha = [0]*N_mod
    for j in range(N_mod):
        alpha[j] = alpha_in[j]    

    M = computeMM_separately(alpha)        
    
    G = computeGG(alpha)
    
    alphaddot = np.array(alphaddot).reshape(3,1)
    Q = np.add(np.dot(M,alphaddot),G)
    
    F1 = [0]*N_mod
    F2 = [0]*N_mod

    for j in range(N_mod):
        Z1 = Z1_func(alpha[j],b[j],L[j])
        Z2 = Z2_func(alpha[j],b[j],L[j])

        if Q[j] >= np.dot((Z1 + Z2),Fmin):
            fr = Fmin
            fl = (Q[j] - np.dot(Z2,Fmin)) / Z1

        else:
            fl = Fmin
            fr = (Q[j] - np.dot(Z1,Fmin)) / Z2

        F1[j] = fl
        F2[j] = fr
    
    Force = np.zeros((N_mod,2))
    Force[:,0] = F1
    Force[:,1] = F2
    
    return Force

# print(compute_forces(3,[pi/4,pi/5,pi/3],[pi/3,pi/3,pi/3],[0.1,0.1,0.1],[0.2,0.2,0.2],100))
    
    
    