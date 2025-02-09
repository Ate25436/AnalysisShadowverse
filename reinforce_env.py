import gymnasium as gym
from gymnasium.spaces import Discrete, Box
from pettingzoo import ParallelEnv
import numpy as np
from numpy import random as rnd
import copy

class TCGEnv(ParallelEnv):
    metadata = {"render.modes": ["human"]}

    CARD_ATTACK = 0
    CARD_HEALTH = 1
    CARD_PP = 2
    CARD_ABILITY = 3
    card_map = {
        'card_0': [4, 4, 1, 0],
        'card_1': [2, 2, 2, 0],
        'card_2': [3, 3, 3, 0],
        'card_3': [4, 3, 4, 0],
        'card_4': [5, 4, 5, 0],
        'card_5': [2, 2, 2, 1],
        'card_6': [2, 3, 3, 1],
        'card_7': [1, 1, 1, 4],
        'card_8': [1, 3, 2, 4],
        'card_9': [2, 1, 2, 5],
        'card_10': [3, 1, 3, 5],
        'card_11': [1, 2, 2, 3],
        'card_12': [2, 3, 3, 3],
        'card_13': [1, 1, 1, 2],
        'card_14': [1, 1, 5, 2],
    }
    def __init__(self):
        self.agents = ['agent_0', 'agent_1']
        self.possible_agents = self.agents[:]
        self.action_spaces = {'agent_0': Discrete(40), 'agent_1': Discrete(40)}
        self.observation_spaces = {'agent_0': Box(low=0, high=30, shape=(67, ), dtype=np.uint16), 'agent_1': Box(low=0, high=30, shape=(67, ), dtype=np.uint16)}
        self.turn = {'agent_0': 1, 'agent_1': 0}
        self.health = {'agent_0': 20, 'agent_1': 20}
        self.PP = {'agent_0': 1, 'agent_1': 0}
        self.hands = {'agent_0': [[0 for _ in range(4)] for _ in range(9)], 'agent_1': [[0 for _ in range(4)] for _ in range(9)]}
        self.fields = {'agent_0': [[0 for _ in range(2)] for _ in range(5)], 'agent_1': [[0 for _ in range(2)] for _ in range(5)]}
        self.attackable = {'agent_0': [0 for _ in range(5)], 'agent_1': [0 for _ in range(5)]}
        deck = []
        for i in range(15):
            deck += [self.card_map[f'card_{i}'] for _ in range(2)]
        self.decks = {'agent_0': copy.deepcopy(deck), 'agent_1': copy.deepcopy(deck)}
        self.render_mode = 'human'
    
    def create_observation(self):

        obs = {}
        for agent in self.agents:
            switch_agent = 'agent_0' if agent == 'agent_1' else 'agent_1'
            concated_obs = []
            concated_obs += [self.health[agent], self.health[switch_agent]]
            concated_obs += [self.PP[agent], self.PP[switch_agent]]
            concated_obs += flatten_list(self.hands[agent])
            concated_obs += flatten_list(self.fields[agent])
            concated_obs += self.attackable[agent]
            concated_obs += [len(self.decks[agent]), len(self.decks[switch_agent])]
            obs[agent] = np.array(concated_obs).astype(np.uint16)
            print(type(obs[agent]))
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

    def reset(self, seed=None, options=None):
        self.TurnPlayer = 'agent_0'
        self.turn = {'agent_0': 1, 'agent_1': 0}
        self.health = {'agent_0': 20, 'agent_1': 20}
        self.PP = {'agent_0': 1, 'agent_1': 0}
        self.fields = {'agent_0': [[0, 0] for _ in range(5)], 'agent_1': [[0, 0] for _ in range(5)]}
        self.attackable = {'agent_0': [0 for _ in range(5)], 'agent_1': [0 for _ in range(5)]}
        deck = []
        for i in range(15):
            deck += [self.card_map[f'card_{i}'] for _ in range(2)]
        self.decks = {'agent_0': copy.deepcopy(deck), 'agent_1': copy.deepcopy(deck)}
        self.draw_n('agent_0', 5)
        self.draw_n('agent_1', 5)
        return self.create_observation(), {agent: {} for agent in self.agents}


    def render(self, mode='human'):
        if mode == 'human':
            observation = self.create_observation()
            for agent in self.agents:
                print(f'{agent}:')
                print(f'health: {observation[agent][0][0]}, PP: {observation[agent][1][0]}')
                print(f'hand: {"; ".join(" ".join(str(item) for item in card) for card in observation[agent][2])}\n')
                print(f'field: {"; ".join(" ".join(str(item) for item in card) for card in observation[agent][3])}')
                print(f'attackable: {observation[agent][5]}')
                print(f'deck_num: {observation[agent][6][0]}')
                print()
    def close(self):
        pass

    def seed(self, seed=None):
        pass

    def configure(self, *args, **kwargs):
        pass
    
    def observation_space(self, agent):
        return self.observation_spaces[agent]
    
    def action_space(self, agent):
        return self.action_spaces[agent]

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
        
    def end_turn(self, agent):
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
        if attacked_index <= 4 and self.fields[switch_agent][attacked_index][self.CARD_HEALTH] == 0:
            observation = self.create_observation()
            return observation, {agent: -0.01, switch_agent:0.0}, {agent: False, switch_agent: False}, {agent: {}, switch_agent: {}}
        if self.attackable[agent][attacker_index] == 0:
            observation = self.create_observation()
            return observation, {agent: -0.01, switch_agent:0.0}, {agent: False, switch_agent: False}, {agent: {}, switch_agent: {}}
        if attacked_index <= 4:
            self.fields[switch_agent][attacked_index][self.CARD_HEALTH] -= self.fields[agent][attacker_index][self.CARD_ATTACK]
        elif attacked_index == 5:
            self.health[switch_agent] -= self.fields[agent][attacker_index][self.CARD_ATTACK]
        if attacked_index <= 4:
            self.fields[agent][attacker_index][self.CARD_HEALTH] -= self.fields[switch_agent][attacked_index][self.CARD_ATTACK]
        elif attacked_index == 5:
            pass

        if attacked_index <= 4 and self.fields[switch_agent][attacked_index][self.CARD_HEALTH] <= 0:
            self.fields[switch_agent][attacked_index] = [0, 0]
        if self.fields[agent][attacker_index][self.CARD_HEALTH] <= 0:
            self.fields[agent][attacker_index] = [0, 0]
        self.attackable[agent][attacker_index] = 0
        observation = self.create_observation()
        return observation, {agent: -0.01, switch_agent:0.0}, {agent: False, switch_agent: False}, {agent: {}, switch_agent: {}}

    def activate_ability(self, agent, ability, field_index=None):
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
            case _:  #その他
                return False
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
    
    def t_save_env(self):
        save_env = {
            'TurnPlayer': self.TurnPlayer,
            'turn': copy.deepcopy(self.turn),
            'health': copy.deepcopy(self.health),
            'PP': copy.deepcopy(self.PP),
            'hands': copy.deepcopy(self.hands),
            'fields': copy.deepcopy(self.fields),
            'attackable': copy.deepcopy(self.attackable),
            'decks': copy.deepcopy(self.decks)
        }
        return save_env
    def t_load_env(self, save_env):
        self.TurnPlayer = save_env['TurnPlayer']
        self.turn = copy.deepcopy(save_env['turn'])
        self.health = copy.deepcopy(save_env['health'])
        self.PP = copy.deepcopy(save_env['PP'])
        self.hands = copy.deepcopy(save_env['hands'])
        self.fields = copy.deepcopy(save_env['fields'])
        self.attackable = copy.deepcopy(save_env['attackable'])
        self.decks = copy.deepcopy(save_env['decks'])

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

def flatten_list(l):
    return [item for sublist in l for item in sublist]

def test():
    test_list = [[0, 0], [1, 1]]
    print(flatten_list(test_list))
if __name__ == '__main__':
    test()