from stable_baselines3 import PPO
from reinforce_env import TCGEnv

from pettingzoo.utils.conversions import parallel_to_aec

import supersuit as ss

from stable_baselines3.common.vec_env import VecMonitor

env = TCGEnv()
env = ss.multiagent_wrappers.pad_observations_v0(env)
gym_env = ss.pettingzoo_env_to_vec_env_v1(env)

vec_env = VecMonitor(gym_env)

# 5. SB3 で学習
model = PPO("MlpPolicy", vec_env, verbose=1, device="cpu")
model.learn(total_timesteps=10000)