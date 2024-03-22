#!/usr/bin/python
# -*- coding: utf-8 -*-

from enumerations import *
from enumerations import CardType, ClassName, Rarity
from gamemaster import GameMaster


def IndexError(Leader):
    SubjectIndex = int(input("Subject Index"))
    if SubjectIndex < 0 or len(Leader.field) <= SubjectIndex:
        print("There is not follower at that place")
        return
    if Leader.field[SubjectIndex].CardType == CardType.Amulet:
        print("That is not follower")
        return
    return SubjectIndex

class abilities():
    @classmethod
    def RepeatNum(cls, func, Num):
        def Repeat(Leader, Opponent):
            for i in range(Num):
                func(Leader, Opponent)
        return Repeat
    
    @classmethod
    def FuncSequence(cls, *funcs):
        def Sequence(Leader, Opponent):
            for func in funcs:
                func(Leader, Opponent)
        return Sequence
    '''条件を含む選択
    @classmethod
    def '''

    @classmethod
    def DrawCardNum(cls, Num):
        def DrawCard(Leader, Opponent):
            for i in range(Num):
                Leader.DrawCard()
        return DrawCard
    
    @classmethod
    def LeaderHealNum(cls, Num):
        def LeaderHeal(Leader, Opponent):
            Leader.Health = min(Leader.MaxHealth, Leader.Health + Num)
        return LeaderHeal #Numに指定した分だけの回復を行う関数のポインタを返す
    
    @classmethod
    def LeaderDamageNum(cls, Num):
        def LeaderDamage(Leader, Opponent):
            Opponent.Health -= Num
        return LeaderDamage #Numに指定した分だけの回復を行う関数のポインタを返す
    
    @classmethod
    def FollowerHealNum(cls, Num):
        def FollowerHeal(Leader, Opponent):
            SubjectIndex = IndexError(Leader)
            Leader.field[SubjectIndex].health = min(Leader.field[SubjectIndex].MaxHealth, Leader.field[SubjectIndex].health + Num)
        return FollowerHeal
    
    @classmethod
    def FollowerDamageNum(cls, Num):
        def FollowerDamage(Leader, Opponent):
            SubjectIndex = IndexError(Opponent)
            Opponent.field[SubjectIndex].health -= Num
        return FollowerDamage
    
    @classmethod
    def FollowerDestroy(cls, Leader, Opponent):
        SubjectIndex = IndexError(Opponent)
        Opponent.field[SubjectIndex].Destroyed()
    
    @classmethod
    def SummonCardNum(cls, Card, Num):
        def SummonCard(Leader, Opponent):
            for i in range(Num):
                if len(Leader.field) == 5:
                    break
                Leader.field.append(Card)
                Leader.Relocation
        return SummonCard

class Card():
    
    def __init__(self, classname:ClassName, rarity:Rarity, cost:int, name:str, CardType:CardType, power:int=-1, health:int=-1, count:int=-1, ability={}) -> None:
        self.ClassName = classname
        self.Rarity = rarity
        self.cost = cost
        self.CardName = name
        self.CardType = CardType
        self.power = power
        self.health = health
        self.MaxHealth = health
        self.count = count
        self.ability = ability
        self.AttackAuthority = AttackAuthority.CantAttack
        self.FieldLocation = -1
        if "rush" in self.ability:
            self.AttackAuthority = AttackAuthority.OnlyFollower
        if "sprint" in self.ability:
            self.AttackAuthority = AttackAuthority.Attackable
    
    def __str__(self) -> str:
        if self.CardType == CardType.Amulet or self.CardType == CardType.Spell:
            return f"{self.CardName}"
        else:
            return f"{self.CardName}(power:{self.power} health:{self.health})"

    def Destroyed(self, Leader, Opponent):
        if self.FieldLocation == -1:
            return
        Leader.field.pop(self.FieldLocation)
        self.FieldLocation = -1
        if "LastWord" in self.ability:
            GameMaster.LastWordQueue.append([self.ability["LastWord"], Leader, Opponent])
        Leader.cemetery += 1
        Leader.Relocation()
    

    

    
class Knight(Card):
    def __init__(self) -> None:
        super().__init__(ClassName.Neutral, Rarity.Bronze, 1, "Knight", CardType.Follower, 1, 1)

class Test1(Card):
    def Test1Fanfare(self, Leader, Opponent):
        knight = Knight()
        Leader.field.append(knight)
        Leader.Relocation()
    
    def __init__(self) -> None:
        super().__init__(ClassName.Neutral, Rarity.Bronze, 2, "test1", CardType.Follower, 2, 2, ability={"fanfare":abilities.SummonCardNum(Card(ClassName.Neutral, Rarity.Bronze, 1, "Knight", CardType.Follower, 1, 1), 1)})
    
class Test2(Card):
    def Test2Fanfare(self, Leader, Opponent):
        test1 = Test1()
        Leader.field.append(test1)
        Leader.Relocation()
    
    def Test2EndOpponentTurnEnd(self, Leader, Opponent):
        Opponent.Health -= 1

    def Test2Engagement(self, Leader, Opponent):
        Leader.Health += 1

    def __init__(self) -> None:
        super().__init__(ClassName.Neutral, Rarity.Bronze, 3, "test2", CardType.Follower, 3, 3, ability={"fanfare":self.Test2Fanfare, "EndOpponentTurn":self.Test2EndOpponentTurnEnd, "engagement":self.Test2Engagement})

class Test3(Card):

    def Test3Attack(self, Leader, Opponent):
        Leader.DrawCard()

    def Test3Engagement(self, Leader, Opponent):
        Opponent.Health -= 1

    def Test3LastWord(self, Leader, Opponent):
        Leader.Health += 1

    def __init__(self) -> None:
        super().__init__(ClassName.Neutral, Rarity.Bronze, 2, "test3", CardType.Follower, 1, 2, ability={"attack":self.Test3Attack, "rush":True, "engagement":self.Test3Engagement, "LastWord":self.Test3LastWord})