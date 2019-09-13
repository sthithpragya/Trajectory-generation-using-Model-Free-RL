import math
import numpy as np
import itertools

from .modules.compute_forces import *
from .modules.compute_alphaddot import *
from .modules.xy_from_alpha import *

# all measurements in radians, metres and seconds

#  MECHANISM DATA (ALTER AS PER NEED)
N_mod = 3  # Number of modules

dt = 0.01  # timestep duation between 2 poses (in seconds)

dF = 0.1  # increase or decrease in actuator force per timestep (in Newton_)

b = [0.1] * N_mod  # List of b values in modules, may be set to non-uniform as well
L = [0.2] * N_mod

#-----------------------------------------------------------

#  RL MODEL DATA (DO NOT ALTER)
kinDim = int(N_mod * 3)  #  info on kinematics -> alpha, alphadot, alphaddot per each module
actDim = int(N_mod * 2)  #  info on actuation -> left, right forces per module 

actDim_v2 = int(N_mod + 1) # left forces are equal, only right forces are all different

beakPosDim = 2  # x, y coordiantes of beak
beakVelDim = 2  # xdot, ydot coordiantes of beak
 
obsSpaceDim= kinDim + actDim + beakPosDim + beakVelDim
#  dimension of the observation vector or 'state' of the robot

actionSpaceDim = int(pow(3, actDim))  # 2 actuators per module and 3 options per actuator (increase, decrease or no-change)
actionSpaceDim_v2 = int(pow(3, actDim_v2))

#NOTE: Overall observation state is: [ai,aidot,aiddot.....,f1l,f1r,f2l,f2r.....,x,y,xdot,ydot]

#--------------------------------------------------------------

#  GOAL DATA (ALTER AS PER NEED)
xPosGoal = 0.3  # Tree position
chatter = 0.05  # Permissible range near goal
#--------------------------------------------------------------

#  LIMITS OF MECHANISM

Fmin = 0  # in Newton
Fmax = 200

alphaMax = math.pi/2
alphaMin = -math.pi/2

# limits on alpha, alphadot, alphaddot
# limits on actuator forces
# limit on beak position 
# limit on beak velocity

# kinHigh = [alphaMax, np.finfo(np.float32).max, np.finfo(np.float32).max] * N_mod
# actHigh = [Fmax] * actDim
# beakPosHigh = [xPosGoal, np.finfo(np.float32).max]
# beakVelHigh = [np.finfo(np.float32).max, np.finfo(np.float32).max]

# kinLow = [alphaMin, -np.finfo(np.float32).max, -np.finfo(np.float32).max] * N_mod
# actLow = [Fmin] * actDim
# beakPosLow = [-np.finfo(np.float32).max, 0]
# beakVelLow = [-np.finfo(np.float32).max, -np.finfo(np.float32).max]

kinHigh = [alphaMax] * N_mod + [np.finfo(np.float32).max] * N_mod + [np.finfo(np.float32).max] * N_mod
actHigh = [Fmax] * actDim
beakPosHigh = [xPosGoal, np.finfo(np.float32).max]
beakVelHigh = [np.finfo(np.float32).max, np.finfo(np.float32).max]

kinLow = [alphaMin] * N_mod + [-np.finfo(np.float32).max] * N_mod + [-np.finfo(np.float32).max] * N_mod
actLow = [Fmin] * actDim
beakPosLow = [-np.finfo(np.float32).max, 0]
beakVelLow = [-np.finfo(np.float32).max, -np.finfo(np.float32).max]

high = kinHigh + actHigh + beakPosHigh + beakVelHigh
low = kinLow + actLow + beakPosLow + beakVelLow
                       
high = np.array(high)      
low = np.array(low)

#---------------------------------------------------------------

# HELPER FUNCTIONS
def extractAlpha(kinInfo): #  extracts the alpha info from kinematic data (of dim kinDim)
    # alpha = [0] * N_mod
    # for i in range(N_mod):
    #     alpha[i] = kinInfo[3*i]

    alpha = kinInfo[0:N_mod]
    return alpha
#--------        
    
def extractAlphadot(kinInfo): #  extracts the alphadot info from kinematic data (of dim kinDim)
    # alphadot = [0] * N_mod
    # for i in range(N_mod):
    #     alphadot[i] = kinInfo[3*i + 1]

    alphadot = kinInfo[N_mod:2*N_mod]
    return alphadot
#--------
    
def extractAlphaddot(kinInfo): #  extracts the alphadot info from kinematic data (of dim kinDim)
    # alphaddot = [0] * N_mod
    # for i in range(N_mod):
    #     alphaddot[i] = kinInfo[3*i + 2]
    alphaddot = kinInfo[2*N_mod:3*N_mod]
    return alphaddot
#--------

def extractActForces(actInfo): #  extracts force info as N_mod x 2 np array
    # currently not used
    forces = np.zeros((N_mod,2))
    for i in range(N_mod):
        forces[i] = actInfo[2*i: 2*(i + 1)]
        
    return forces

#forces[i] = [fL, fR] for the (i+1)th module if we start numbering from 1
#--------
    
comb = itertools.product(range(-1,2), repeat=actDim) #  3^actDim possible combinations per action step
#  comb can only be iterated upon
nextdF = np.zeros((int(pow(3,actDim)),actDim)) #  3^actDim all possible combinations; actDim = length of each combinations (total actuation forces)
iterator = 0

for tempComb in comb:
    nextdF[iterator] = np.array(tempComb)
    iterator = iterator + 1

# print(dF)
nextdF = np.dot(nextdF,dF)  # step of dF

comb_v2 = itertools.product(range(-1,2), repeat=actDim_v2) #  3^actDim_v2 possible combinations per action step
nextdF_v2 = np.zeros((int(pow(3,actDim_v2)),actDim)) #  3^actDim_v2 all possible combinations; actDim = length of each combinations (total actuation forces)
iterator_v2 = 0
for tempComb_v2 in comb_v2:
    tempList = list(tempComb_v2)
    nextdF_v2[iterator_v2] = np.array([tempList[0]]*(N_mod - 1) + tempList)
    iterator_v2 = iterator_v2 + 1

nextdF_v2 = np.dot(nextdF_v2,dF)  # step of dF

def nextAction(actSeq): #  actSeq -> int from 0 to actionSpaceDim-1
    tempdF = nextdF[actSeq]
    tempdF_v2 = nextdF_v2[actSeq]

    return tempdF_v2
#--------

def newAlphaddot(Forces, alpha):  # Forces - array, alpha  list
    # FL = [0]*N_mod
    # FR = [0]*N_mod
    # for i in range(N_mod):
    #     FL[i] = Forces[2*i]
    #     FR[i] = Forces[2*i + 1]

    FL = Forces[0:N_mod]
    FR = Forces[N_mod:2*N_mod]

    temp =  compute_alphaddot(N_mod,alpha,FL,FR,b,L)
    return temp # return list
    # NOTE THESE RETURN ARRAYS

def newAlphadot(alphaddot, oldalphadot):  # alphaddot - list, oldalphadot - list
    change = np.dot(alphaddot,dt)
    temp = np.add(change, oldalphadot)
    return temp.tolist()

def newAlpha(alphadot, oldalpha):  # alphadot - list, oldalpha - list
    change = np.dot(alphadot,dt)
    temp = np.add(change, oldalpha)
    return temp.tolist()
#--------
    
def check(elemArray, lower, upper):  # to check if forces (array) are within limits (lists)
    upper = np.array(upper)
    lower = np.array(lower)
    return ((lower <= elemArray).all() and (elemArray <= upper).all())

#-----------------------------------------------------------------

#  START DATA (ALTER AS PER NEED)
kinInit = [0] * kinDim  # [alpha_1_init, alpha_2_init,... alpha_1_init_dot, alpha_2_init_dot,.... alpha_1_init_ddot, alpha_2_init_ddot ....]
actInit = [0] * actDim  # [f1L, f2L, f3L,...f1R, f2R, f3R....] at init

gammaInit = 0  # mechanism placed on horizontal ground

alphaInit = extractAlpha(kinInit)
alphadotInit = extractAlphadot(kinInit)

beakPosInit = xy_from_alpha(alphaInit,b,L,gammaInit)
beakVelInit = xy_from_alpha(alphadotInit,b,L,gammaInit)

initState = kinInit + actInit + beakPosInit + beakVelInit

#timeElap = 0

#--------------------------------------------------------------

# TESTING
#print(extractAlphadot([1,2,3,1,2,3]))

#print(extractActForces([1,2,3,4]))        
#
#print(nextAction(55))
#print(nextdF[55])
#
#print(nextAction(79))
#print(nextdF[79])


#print(check(5, 1, 10))


