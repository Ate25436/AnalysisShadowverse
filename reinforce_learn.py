import supersuit as ss
from pettingzoo.utils.conversions import parallel_to_aec
from stable_baselines3 import DQN, PPO
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.vec_env import VecMonitor

from reinforce_env import TCGEnv




timesteps = 25000

env = TCGEnv()
env = ss.flatten_v0(env)
gym_env = ss.pettingzoo_env_to_vec_env_v1(env)

vec_env = VecMonitor(gym_env)

# 5. SB3 で学習
model = DQN("MlpPolicy", vec_env, verbose=1, device="cuda")
model.learn(total_timesteps=timesteps)
model.save("dqn_tcg")
