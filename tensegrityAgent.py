import gym
import DQN_model

#from tensegrityEnvironment import *

from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.deepq.policies import LnMlpPolicy, MlpPolicy
from stable_baselines import DQN

# Instantiate and wrap the env
#env = DummyVecEnv([lambda: tensegrityEnvironment])

env = gym.make('tensegrity-v0')
env = DummyVecEnv([lambda: env])

# Define and Train the agent
model = DQN('LnMlpPolicy', env, verbose=1)  # , prioritized_replay=True
model.learn(total_timesteps=100000)  # 25000
model.save("agentTraj_2")

del model # remove to demonstrate saving and loading

model = DQN.load("agentTraj_2")

obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()