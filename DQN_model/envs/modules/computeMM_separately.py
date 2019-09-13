from .computeMxyga import *
from .computeR import *
from .computeMxyg_head import *
from .computeR_head import *
import numpy as np
from math import *

# alpha -> list of alpha for each module ~ [alpha_1, alpha_2, ...]    
def computeMM_separately(alpha):

    N_mod=len(alpha) # number of modules
    
    M = computeMxyga(alpha)
    R = computeR(alpha)
    MM = np.zeros((N_mod,N_mod))
    Mmod = np.zeros((N_mod,N_mod,N_mod))

    for i in range(N_mod):
        Mmod[i,:,:] = np.dot(np.dot(np.transpose(R[i,:,:]),M[i,:,:]),R[i,:,:])
        MM = MM + Mmod[i,:,:]
        
    if True:
        M_head=computeMxyg_head(alpha)
        R_head=computeR_head(alpha)
        MM = MM + np.dot(np.dot(np.transpose(R_head),M_head),R_head)

    return MM

# print(computeMM_separately([pi/4,pi/5,pi/3]))