from gym.envs.registration import register

register(
    id='tensegrity-v0',
    entry_point='DQN_model.envs:birdEnv',
)