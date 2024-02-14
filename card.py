#!/usr/bin/python
# -*- coding: utf-8 -*-
from enumurations import *
from gamemaster import GameMaster

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
        self.FieldLocation = -1
    
    def __str__(self) -> str:
        return f"{self.CardName}"

    def Destroyed(self, Leader):
        print(self.FieldLocation)
        Leader.field.pop(self.FieldLocation)
        self.FieldLocation = -1
        if "LastWord" in self.ability:
            GameMaster.LastWordQueue(self.ability["LastWord"])
        Leader.cemetery += 1
        Leader.Relocation()
    

    
class Knight(Card):
    def __init__(self) -> None:
        super().__init__(ClassName.Neutral, Rarity.Bronze, 1, "Knight", CardType.Follower, 1, 1)

class Test1(Card):
    def Test1Fanfare(self, Leader):
        knight = Knight()
        Leader.field.append(knight)
        Leader.Relocation()
    
    def __init__(self) -> None:
        super().__init__(ClassName.Neutral, Rarity.Bronze, 2, "test1", CardType.Follower, 2, 2, ability={"fanfare":self.Test1Fanfare})
    
class Test2(Card):
    def Test2Fanfare(self,Leader):
        test1 = Test1()
        Leader.field.append(test1)
        Leader.Relocation()
    
    def __init__(self) -> None:
        super().__init__(ClassName.Neutral, Rarity.Bronze, 3, "test2", CardType.Follower, 3, 3, ability={"fanfare":self.Test2Fanfare})