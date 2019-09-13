from math import *
import numpy as np

def xy_from_alpha(alpha,b,L,init_pos): # all input as lists; init_pos -> [x, y]
    
    x = 0
    y = 0
    
    N_mod = len(alpha)
    
    gamma = init_pos
    
    # print('HERE HERE HERE', L)
    # print('HERE HERE HERE', alpha)


    for i in range(N_mod):
        # print(L[i]) 
        li = sqrt(L[i] ** 2 - np.dot((b[i] ** 2),(cos(alpha[i] / 2) ** 2)))
        x = x - np.dot(li,sin(gamma + alpha[i] / 2))
        y = y + np.dot(li,cos(gamma + alpha[i] / 2))
        gamma = gamma + alpha[i]
    
    return [x, y]    