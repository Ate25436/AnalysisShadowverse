import gymnasium as gym
from gymnasium.spaces import Discrete, Box
from pettingzoo import ParallelEnv
import numpy as np
from numpy import random as rnd

class TCGEnv(ParallelEnv):
    metadata = {"render.modes": ["human"]}
    HEALTH = 0
    PP = 1
    HAND = 2
    MY_FIELD = 3
    ENEMY_FIELD = 4
    ATTACKABLE = 5
    DECK = 6

    CARD_ATTACK = 0
    CARD_HEALTH = 1
    CARD_PP = 2
    CARD_ABILITY = 3
    def __init__(self):

        self.action_space = {'agent_0': Discrete(40), 'agent_1': Discrete(40)}
        self.observation_space = {'agent_0': (Box(low=0, high=20, shape=(2, )), #体力
                                              Box(low=0, high=10, shape=(2, )), #PP
                                              Box(low=0, high=8, shape=(9, 4)), #手札
                                              Box(low=0, high=8, shape=(5, 2)), #自分の場
                                              Box(low=0, high=8, shape=(5, 2)), #相手の場
                                              Box(low=0, high=1, shape=(5, )), #攻撃可能か
                                              Box(low=0, high=30, shape=(2, ))), #デッキ枚数
                                              'agent_1': 
                                              (Box(low=0, high=20, shape=(2, )), #体力
                                              Box(low=0, high=10, shape=(2, )), #PP
                                              Box(low=0, high=8, shape=(9, 4)), #手札
                                              Box(low=0, high=8, shape=(5, 2)), #自分の場
                                              Box(low=0, high=8, shape=(5, 2)), #相手の場
                                              Box(low=0, high=1, shape=(5, )), #攻撃可能か
                                              Box(low=0, high=30, shape=(2, ))), #デッキ枚数
                                                }
        self.decks = {'agent_0': np.array([base_n(i, 8) for i in range(30)]).astype(np.float32), 'agent_1': np.array([base_n(i, 8) for i in range(30)]).astype(np.float32)} #後で変える
        self.TurnPlayer = 'agent_0'
        self.turn = {'agent_0': 1, 'agent_1': 0}
    def step(self, actions):
        action = actions[self.TurnPlayer]
        agent = self.TurnPlayer
        if 0 <= action <= 8:
            obs, reward, done, info = self.play(agent, action)
            return obs, reward, done, info
        elif action == 39:
            obs, reward, done, info = self.end_turn(agent)
            return obs, reward, done, info
        else:
            obs, reward, done, info = self.attack(agent, (action - 9) // 6, (action - 9) % 6)
            return obs, reward, done, info

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
        switch_agent = 'agent_0' if agent == 'agent_1' else 'agent_1'
        if self.observation_space[agent][self.HAND][card_index][self.CARD_HEALTH] == 0:
            return self.observation_space, {agent: -0.01, switch_agent:0.0}, {agent: False, switch_agent: False}, {agent: {}, switch_agent: {}}
        card_info = self.observation_space[agent][self.HAND][card_index]
        if card_info[self.CARD_PP] > self.observation_space[agent][self.PP][0]:
            return self.observation_space, {agent: -0.01, switch_agent:0.0}, {agent: False, switch_agent: False}, {agent: {}, switch_agent: {}}
        if self.observation_space[agent][self.MY_FIELD][-1][self.CARD_HEALTH] != 0:
            return self.observation_space, {agent: -0.01, switch_agent:0.0}, {agent: False, switch_agent: False}, {agent: {}, switch_agent: {}}
        done = False
        self.observation_space[agent][self.PP][0] -= card_info[self.CARD_PP]
        self.observation_space[switch_agent][self.PP][1] -= card_info[self.CARD_PP]
        done = self.activate_ability(agent, card_info[3])
        try:
            i = self.observation_space[agent][self.MY_FIELD].index(np.array([0, 0]).astype(np.float32))
        except ValueError:
            self.observation_space[agent][self.PP][0] += card_info[self.CARD_PP]
            self.observation_space[switch_agent][self.PP][1] += card_info[self.CARD_PP]
            return self.observation_space, {agent: -0.01, switch_agent:0.0}, {agent: False, switch_agent: False}, {agent: {}, switch_agent: {}}
        self.observation_space[agent][self.MY_FIELD][i] = np.array([card_info[self.CARD_ATTACK], card_info[self.CARD_HEALTH]]).astype(np.float32)
        self.observation_space[switch_agent][self.ENEMY_FIELD][i] = np.array([card_info[self.CARD_ATTACK], card_info[self.CARD_HEALTH]]).astype(np.float32)
        self.observation_space[agent][self.HAND][card_index] = np.array([0, 0, 0, 0]).astype(np.float32)
        if done == False:
            return self.observation_space, {agent: -0.01, switch_agent:0.0}, {agent: done, switch_agent: done},  {agent: {}, switch_agent: {}}
        else:
            return self.observation_space, {agent: 10.0, switch_agent:-10.0}, {agent: done, switch_agent: done}, {agent: {}, switch_agent: {}}

        
    def end_turn(self, agent):
        switch_agent = 'agent_0' if agent == 'agent_1' else 'agent_1'
        self.TurnPlayer = switch_agent
        self.turn[switch_agent] += 1
        self.observation_space[switch_agent][self.PP][0] = min(self.turn[switch_agent], 8).astype(np.float32)
        self.observation_space[agent][self.PP][1] = min(self.turn[switch_agent], 8).astype(np.float32)
        self.draw_n(switch_agent, 1)
        for i in range(5):
            if self.observation_space[switch_agent][self.MY_FIELD][i][self.CARD_HEALTH] != 0:
                self.observation_space[switch_agent][self.ATTACKABLE][i] = 1
        return self.observation_space, {agent: -0.01, switch_agent:0.0}, {agent: False, switch_agent: False}, {agent: {}, switch_agent: {}}

    def attack(self, agent, attacker_index, attacked_index):
        pass

    def activate_ability(self, agent, ability):
        match ability:
            case 0:   #能力なし
                return False
            case 1:   #召喚
                try:
                    i = self.observation_space[agent][self.MY_FIELD].index(np.array([0, 0]).astype(np.float32))
                except ValueError:
                    return False
                self.observation_space[agent][self.MY_FIELD][i] = np.array([1, 1]).astype(np.float32)
                switch_agent = 'agent_0' if agent == 'agent_1' else 'agent_1'
                self.observation_space[switch_agent][self.ENEMY_FIELD][i] = np.array([1, 1]).astype(np.float32)
            case 2:   #治癒
                self.observation_space[self.HEALTH][0] = min(self.observation_space[self.HEALTH][0] + 2, 20).astype(np.float32)
                switch_agent = 'agent_0' if agent == 'agent_1' else 'agent_1'
                self.observation_space[switch_agent][self.HEALTH][1] = min(self.observation_space[switch_agent][self.HEALTH][1] + 2, 20).astype(np.float32)
                return False
            case 3:   #攻撃
                done = False
                self.observation_space[agent][self.HEALTH][1] -= 2.0
                switch_agent = 'agent_0' if agent == 'agent_1' else 'agent_1'
                self.observation_space[switch_agent][self.HEALTH][0] -= 2.0
                if self.observation_space[agent][self.HEALTH][1] <= 0.0:
                    done = True
                return done
            case 4:   #取得
                done = self.draw_n(agent, 1)
                return done
            case 5:   #速攻
                i = self.observation_space[agent][self.MY_FIELD].index(np.array([0, 0]).astype(np.float32))
                self.observation_space[agent][self.ATTACKABLE][i] = 1
                return False

    
    def draw_n(self, agent, n):
        for _ in range(n):
            deck = self.decks[agent]
            if len(deck) == 0:
                return False
            else:
                rnd.shuffle(deck)
                card = deck.pop()
                self.observation_space[agent][self.HAND][self.observation_space[agent][self.HAND].index(np.array([0, 0, 0, 0]).astype(np.float32))] = card
                self.observation_space[agent][self.DECK][0] -= 1
                switch_agent = 'agent_0' if agent == 'agent_1' else 'agent_1'
                self.observation_space[switch_agent][self.DECK][1] -= 1
        return True
            
def base_n(num_10,n):
    str_n = ''
    while num_10:
        if num_10%n>=10:
            return -1
        str_n += str(num_10%n)
        num_10 //= n
    return int(str_n[::-1])