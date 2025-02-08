import gymnasium as gym
from gymnasium.spaces import Discrete, Box
from pettingzoo import ParallelEnv
import numpy as np
from numpy import random as rnd

class TCGEnv(ParallelEnv):
    metadata = {"render.modes": ["human"]}

    CARD_ATTACK = 0
    CARD_HEALTH = 1
    CARD_PP = 2
    CARD_ABILITY = 3
    def __init__(self):
        self.agents = ['agent_0', 'agent_1']
        self.possible_agents = self.agents[:]
        self.action_space = {'agent_0': Discrete(40), 'agent_1': Discrete(40)}
        self.observation_space = {'agent_0': ((Discrete(21) for _ in range(2)), #体力
                                              (Discrete(9) for _ in range(2)), #PP
                                              ((Discrete(9) for _ in range(4)) for _ in range(9)), #手札
                                              ((Discrete(9) for _ in range(2)) for _ in range(5)), #自分の場
                                              ((Discrete(9) for _ in range(2)) for _ in range(5)), #相手の場
                                              (Discrete(2) for _ in range(5)), #攻撃可能か
                                              (Discrete(31) for _ in range(2))), #デッキ枚数
                                              'agent_1': 
                                              ((Discrete(21) for _ in range(2)), #体力
                                              (Discrete(9) for _ in range(2)), #PP
                                              ((Discrete(9) for _ in range(4)) for _ in range(9)), #手札
                                              ((Discrete(9) for _ in range(2)) for _ in range(5)), #自分の場
                                              ((Discrete(9) for _ in range(2)) for _ in range(5)), #相手の場
                                              (Discrete(2) for _ in range(5)), #攻撃可能か
                                              (Discrete(31) for _ in range(2))), #デッキ枚数
                                                }
        self.TurnPlayer = 'agent_0'
        self.turn = {'agent_0': 1, 'agent_1': 0}
        self.health = {'agent_0': 20, 'agent_1': 20}
        self.PP = {'agent_0': 1, 'agent_1': 0}
        self.hands = {'agent_0': [[0 for _ in range(4)] for _ in range(9)], 'agent_1': [[0 for _ in range(4)] for _ in range(9)]}
        self.fields = {'agent_0': [[0 for _ in range(2)] for _ in range(5)], 'agent_1': [[0 for _ in range(2)] for _ in range(5)]}
        self.attackable = {'agent_0': [0 for _ in range(5)], 'agent_1': [0 for _ in range(5)]}
        self.decks = {'agent_0': [[1, 1, 1, 0] for _ in range(30)], 'agent_1': [[1, 1, 1, 0] for _ in range(30)]} #後で変える
    
    def create_observation(self):
        obs = {agent: ((self.health[agent], self.health[self.switch_agent(agent)]), 
                       (self.PP[agent], self.PP[self.switch_agent(agent)]), 
                       tuple(tuple(hand) for hand in self.hands[agent]), 
                       tuple(tuple(card) for card in self.fields[agent]), 
                       tuple(tuple(card) for card in self.fields[self.switch_agent(agent)]), 
                       tuple(self.attackable[agent]), 
                       (len(self.decks[agent]), len(self.decks[self.switch_agent(agent)]))) for agent in self.agents}
        return obs

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
        if self.hands[agent][card_index][self.CARD_HEALTH] == 0:
            observation = self.create_observation()
            return observation, {agent: -0.01, switch_agent:0.0}, {agent: False, switch_agent: False}, {agent: {}, switch_agent: {}}
        card_info = self.hands[agent][card_index]
        if card_info[self.CARD_PP] > self.PP[agent]:
            observation = self.create_observation()
            return observation, {agent: -0.01, switch_agent:0.0}, {agent: False, switch_agent: False}, {agent: {}, switch_agent: {}}
        field_index = self.find_empty_field(agent)
        if field_index == -1:
            observation = self.create_observation()
            return observation, {agent: -0.01, switch_agent:0.0}, {agent: False, switch_agent: False}, {agent: {}, switch_agent: {}}
        done = False
        #---要修正---
        self.PP[agent] -= card_info[self.CARD_PP]
        self.fields[agent][field_index] = [card_info[self.CARD_ATTACK], card_info[self.CARD_HEALTH]]
        done = self.activate_ability(agent, card_info[3], field_index=field_index)
        self.hands[agent][card_index] = [0, 0, 0, 0]
        if done == False:
            observation = self.create_observation()
            return observation, {agent: -0.01, switch_agent:0.0}, {agent: done, switch_agent: done},  {agent: {}, switch_agent: {}}
        else:
            observation = self.create_observation()
            if self.health[switch_agent] <= 0:
                return observation, {agent: 100.0, switch_agent:-100.0}, {agent: done, switch_agent: done}, {agent: {}, switch_agent: {}}
            elif self.len(self.decks[agent]) <= 0:
                return observation, {agent: -100.0, switch_agent:100.0}, {agent: done, switch_agent: done}, {agent: {}, switch_agent: {}}
        #------------
        
    def end_turn(self, agent):
        #---要修正---
        switch_agent = 'agent_0' if agent == 'agent_1' else 'agent_1'
        self.TurnPlayer = switch_agent
        self.turn[switch_agent] += 1
        self.PP[switch_agent] = min(self.turn[switch_agent], 8)
        self.draw_n(switch_agent, 1)
        for i in range(5):
            if self.fields[switch_agent][i][self.CARD_HEALTH] != 0:
                self.attackable[switch_agent][i] = 1
        observation = self.create_observation()
        return observation, {agent: -0.01, switch_agent:0.0}, {agent: False, switch_agent: False}, {agent: {}, switch_agent: {}}

    def attack(self, agent, attacker_index, attacked_index):
        switch_agent = 'agent_0' if agent == 'agent_1' else 'agent_1'
        if self.fields[agent][attacker_index][self.CARD_HEALTH] == 0:
            observation = self.create_observation()
            return observation, {agent: -0.01, switch_agent:0.0}, {agent: False, switch_agent: False}, {agent: {}, switch_agent: {}}
        #-------------

    def activate_ability(self, agent, ability, field_index=None):
        #---要修正---
        switch_agent = 'agent_0' if agent == 'agent_1' else 'agent_1'
        match ability:
            case 0:   #能力なし
                return False
            case 1:   #召喚
                try:
                    i = self.fields[agent].index([0, 0])
                except ValueError:
                    return False
                self.fields[agent][i] = [1, 1]
                return False
            case 2:   #治癒
                self.health[agent] = min(self.health[agent] + 2, 20)
                return False
            case 3:   #攻撃
                done = False
                self.health[switch_agent] -= 2
                if self.health[switch_agent] <= 0:
                    done = True
                return done
            case 4:   #取得
                done = self.draw_n(agent, 1)
                return done
            case 5:   #速攻
                self.attackable[agent][field_index] = 1
                return False
        #-------------
    def find_empty_field(self, agent):
        try:
            i = self.fields[agent].index([0, 0])
        except ValueError:
            return -1
        return i
    
    def find_empty_hand(self, agent):
        try:
            i = self.hands[agent].index([0, 0, 0, 0])
        except ValueError:
            return -1
        return i

    def switch_agent(self, agent):
        return 'agent_0' if agent == 'agent_1' else 'agent_1'
    
    def draw_n(self, agent, n):
        for _ in range(n):
            deck = self.decks[agent]
            if len(deck) == 0:
                return True
            else:
                rnd.shuffle(deck)
                card = deck.pop()
                card_index = self.find_empty_hand(agent)
                if card_index != -1:
                    self.hands[agent][card_index] = card
        return False
            
def base_n(num_10,n):
    str_n = ''
    while num_10:
        if num_10%n>=10:
            return -1
        str_n += str(num_10%n)
        num_10 //= n
    return int(str_n[::-1])

def test():
    env = TCGEnv()
    env.reset()
    print(env.create_observation())

if __name__ == '__main__':
    test()