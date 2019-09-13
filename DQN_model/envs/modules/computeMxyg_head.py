from math import *
import numpy as np

def computeMxyg_head(alpha):
	alpha1 = alpha[0]
	alpha2 = alpha[1]
	alpha3 = alpha[2]
	
	M_head_temp = ([np.multiply(pi,(7.0 / 80.0)),0.0,np.multiply(np.multiply(pi,cos(alpha1 + alpha2 + alpha3)),(- 0.004375)),0.0,np.multiply(pi,(7.0 / 80.0)),np.multiply(np.multiply(pi,sin(alpha1 + alpha2 + alpha3)),(- 0.004375)),np.multiply(np.multiply(pi,cos(alpha1 + alpha2 + alpha3)),(- 0.004375)),np.multiply(np.multiply(pi,sin(alpha1 + alpha2 + alpha3)),(- 0.004375)),0.0009621127501618746])

	M_head = np.array(M_head_temp).reshape(3,3,order='F')

	return M_head

# print(computeMxyg_head([pi/4,pi/5,pi/3]))