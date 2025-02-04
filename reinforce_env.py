import gymnaisum as gym
from gymnaisum.spaces import Discrete, Box
from pettingzoo import ParallelEnv

class TCGEnv(ParallelEnv):
    metadata = {"render.modes": ["human"]}
    def __init__(self):

        self.action_space = {'agent_0': Discrete(40), 'agent_1': Discrete(40)}
        self.observation_space = {'agent_0': (Box(low=0, high=20, shape=(2, )), #体力
                                              Box(low=0, high=10, shape=(2, )), #PP
                                              Box(low=0, high=8, shape=(36, )), #手札
                                              Box(low=0, high=8, shape=(10, )), #自分の場
                                              Box(low=0, high=8, shape=(10, )), #相手の場
                                              Box(low=0, high=1, shape=(5, )), #攻撃可能か
                                              Box(low=0, high=30, shape=(2, ))), #デッキ枚数
                                              'agent_1': 
                                              (Box(low=0, high=20, shape=(2, )), #体力
                                              Box(low=0, high=10, shape=(2, )), #PP
                                              Box(low=0, high=8, shape=(36, )), #手札
                                              Box(low=0, high=8, shape=(10, )), #自分の場
                                              Box(low=0, high=8, shape=(10, )), #相手の場
                                              Box(low=0, high=1, shape=(5, )), #攻撃可能か
                                              Box(low=0, high=30, shape=(2, ))), #デッキ枚数
                                                }

    def step(self, action):
        agent, action = action
        if 0 <= action <= 8:
            self.play(agent, action)
            return 
        elif action == 39:
            self.end_turn(agent)
            return
        else:
            self.attack(agent, (action - 9) // 6, (action - 9) % 6)
            return

    def reset(self):
        pass

    def render(self, mode='human'):
        pass

    def close(self):
        pass

    def seed(self, seed=None):
        pass

    def configure(self, *args, **kwargs):
        pass

    def play(self, agent, card_index):
        pass
    
    def end_turn(self, agent):
        pass

    def attack(self, agent, attacker_index, attacked_index):
        pass

def base_n(num_10,n):
    str_n = ''
    while num_10:
        if num_10%n>=10:
            return -1
        str_n += str(num_10%n)
        num_10 //= n
    return int(str_n[::-1])