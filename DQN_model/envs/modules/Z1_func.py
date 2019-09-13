from math import *
import numpy as np

def Z1_func(alpha, b, L):

    b = np.array(b) #converting to np array for ease in subsequent calc
    L = np.array(L)    
    
    if alpha == pi:
        psi = pi

    else:
        if alpha == -pi:
            psi = -pi

        else:

            f1=np.dot(np.dot(np.dot(2,b),L),sin(alpha))

            f2=np.dot(np.dot(np.dot(2,b),L),(cos(alpha) + 1))

            f3=np.dot(np.dot(2,b ** 2),(cos(alpha) + 1))
                        
            psi=np.dot(2,atan((- f1 - sqrt(f1 ** 2 + f2 ** 2 - f3 ** 2)) / (f3 - f2)))    
    
    if alpha == pi:
        phi = pi

    else:
        if alpha == -pi:
            phi = -pi

        else:

            g1=np.dot(np.dot(np.dot(- 2,b),L),sin(alpha))
 
            g2=np.dot(np.dot(np.dot(- 2,b),L),(cos(alpha) + 1))

            g3=np.dot(np.dot(2,b ** 2),(cos(alpha) + 1))

            phi=np.dot(2,atan2(- g1 + sqrt(g1 ** 2 + g2 ** 2 - g3 ** 2),g3 - g2))

    l1=sqrt(b ** 2 + L ** 2 + np.dot(np.dot(np.dot(2,b),L),cos(psi)))

    S3=np.dot(b,sin(phi - alpha)) / (np.dot(L,sin(psi - phi)))
    
    Z1=np.multiply(np.dot(np.dot(b,L),sin(psi)) / l1,S3)

    return Z1
        