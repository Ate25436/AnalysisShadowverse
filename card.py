#!/usr/bin/python
# -*- coding: utf-8 -*-
from enumurations import *


class Card():
    
    def __init__(self, classname:ClassName, rarity:Rarity, cost:int, name:str, CardType:CardType, power:int=-1, health:int=-1, count:int=-1, ability={}) -> None:
        self.classname = classname
        self.rarity = rarity
        self.cost = cost
        self.CardName = name
        self.CardType = CardType
        self.power = power
        self.health = health
        self.count = count
        self.ability = ability
        self.AttackAuthority = AttackAuthority.CantAttack
    def __str__(self) -> str:
        return f"{self.CardName}"
    
class Knight(Card):
    def __init__(self) -> None:
        super().__init__(ClassName.Neutral, Rarity.Bronze, 1, "Knight", CardType.Follower, 1, 1)

class test1(Card):
    def Test1Fanfare(self, GameMaster, Leader:LeaderEnum):
        knight = Knight()
        GameMaster.field[Leader].append(knight)
    
    def __init__(self) -> None:
        super().__init__(ClassName.Neutral, Rarity.Bronze, 2, "test1", CardType.Follower, 2, 2, ability={"fanfare":self.Test1Fanfare})
    
    