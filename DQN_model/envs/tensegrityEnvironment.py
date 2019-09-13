#from configurationParam import *

# from . import configurationParam
# from configurationParam import *

from .configurationParam import *


import csv
import gym
from gym import spaces

class birdEnv(gym.Env):
  """Custom Environment that follows gym interface"""
  metadata = {'render.modes': ['human']}
  def __init__(self):
      
#      super(birdEnv, self).__init__()
      #high and low limits on the state space


      # high = kinHigh + actHigh + beakPosHigh + beakVelHigh
      # low = kinLow + actLow + beakPosLow + beakVelLow
                       
      # high = np.array(high)      
      # low = np.array(low)
      
      # print(actionSpaceDim)
      # self.action_space = spaces.Discrete(actionSpaceDim)  # defining the size of action set
      self.action_space = spaces.Discrete(actionSpaceDim_v2)  # defining the size of action set      
      self.observation_space = spaces.Box(low, high, dtype=np.float32)  # defining the size of obs set
      
      
  def step(self, action):
      timeElap = self.timeElapsed  # track of time elapsed

      currentState = self.state
      
      kinInfo = currentState[:kinDim]  # [ai,aidot,aiddot.....] for all modules
      actInfo = currentState[kinDim: kinDim + actDim]  # [f1l,f1r,f2l,f2r.....] for all modules
      currentBeakPos = currentState[kinDim + actDim: kinDim + actDim + beakPosDim]  # [x,y] of beak
      currentBeakVel = currentState[kinDim + actDim + beakPosDim: kinDim + actDim + beakPosDim + beakVelDim]  # [xdot, ydot] of beak
      
      currentAlpha = extractAlpha(kinInfo)
      currentAlphadot = extractAlphadot(kinInfo)
      
#      currentForces = extractActForces(actInfo)  # currentForces is a N_mod x 2 np array of actuator forces (l,r) with currentF[i] returning [l, r] for the i+1 th module
      currentForces = np.array(actInfo)
      
      # New possible state
      changeInForces = nextAction(action)
      
      tempForces = np.add(currentForces, changeInForces)  # updated forces

      tempAlphaddot = newAlphaddot(tempForces, currentAlpha)  # possible alphaddot (if valid)
      # print('temp alphaddot is: ', tempAlphaddot)    

      # print('current alphadot is: ', currentAlphadot)    
      tempAlphadot = newAlphadot(tempAlphaddot, currentAlphadot)
      # print('temp alphadot is: ', tempAlphadot)    

      # print('current alpha is: ', currentAlpha)    
      tempAlpha = newAlpha(tempAlphadot, currentAlpha)
      # print('temp alpha is: ', tempAlpha)    

      tempBeakPos = xy_from_alpha(tempAlpha,b,L,gammaInit)
      tempBeakVel = xy_from_alpha(tempAlphadot,b,L,gammaInit)
      
      # Filling the state
      # tempState = [0] * obsSpaceDim
      
      # for i in range(N_mod):
      #     tempState[i] = tempAlpha[i]
      #     tempState[i+1] = tempAlphadot[i]
      #     tempState[i+2] = tempAlphaddot[i]
      
      # tempState[kinDim: kinDim + actDim] = tempForces.tolist()          
      # tempState[kinDim + actDim: kinDim + actDim + beakPosDim] = tempBeakPos
      # tempState[kinDim + actDim + beakPosDim: kinDim + actDim + beakPosDim + beakVelDim] = tempBeakVel
      
      tempState = tempAlpha + tempAlphadot + tempAlphaddot + tempForces.tolist() + tempBeakPos + tempBeakVel

      self.state = tempState
      timeElap = timeElap + dt
      self.timeElapsed = timeElap
      
      isValid = check(np.array(tempState), low, high)
      
      if isValid == False:
          reward = -100  # undesirable
          done = True  # termination of episode during training due to obstacle
      
      else:
          if check(tempBeakPos[0], xPosGoal - chatter, xPosGoal + chatter) == True: # goal reached
              reward = sqrt(pow(tempBeakVel[0],2) + pow(tempBeakVel[1],2))  # maximise this
              done = True  # termination of episode
          else:
              reward = 0  # everything is going fine
              done = False  # continue the episode
              
      return np.array(self.state), reward, done, {}
              
    

  def reset(self):
      self.state = initState
      self.timeElapsed = 0
      return np.array(self.state)
      
  def render(self, mode='human', close=False): # printing the current stats and also writing to a CSV file
      # print('state is:  ',self.state, '  time elapsed: ',self.timeElapsed)
      with open('trajData.csv', 'a', newline='') as csvfile:
          writer = csv.writer(csvfile)
          writer.writerow(self.state + [self.timeElapsed])
          

      
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    