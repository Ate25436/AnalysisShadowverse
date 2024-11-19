#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import annotations

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
        self.SelectedCard = []
    
    def __str__(self) -> str:
        if self.CardType == CardType.Amulet or self.CardType == CardType.Spell:
            return f"{self.CardName}(c: {self.cost})"
        else:
            return f"{self.CardName}(p:{self.power} h:{self.health} c:{self.cost} a:{self.AttackAuthority2str()})"

    def Destroyed(self, Leader, Opponent):
        if self.FieldLocation == -1:
            return
        Leader.field.pop(self.FieldLocation)
        self.FieldLocation = -1
        if "LastWord" in self.ability:
            GameMaster.LastWordQueue.append([self.ability["LastWord"], Leader, Opponent])
        Leader.cemetery += 1
        Leader.Relocation()
    
    def AttackAuthority2str(self):
        if self.AttackAuthority == AttackAuthority.CantAttack:
            return "Can't"
        elif self.AttackAuthority == AttackAuthority.OnlyFollower:
            return "Only Follower"
        elif self.AttackAuthority == AttackAuthority.Attackable:
            return "Attackable"

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
        Opponent.field[SubjectIndex].Destroyed(Leader, Opponent)
    
    @classmethod
    def SummonCardNum(cls, Card, Num):
        def SummonCard(Leader, Opponent):
            for i in range(Num):
                if len(Leader.field) == 5:
                    break
                Leader.field.append(Card)
                Leader.Relocation
        return SummonCard

    @classmethod
    def if_CardType(cls, CardType: CardType):
        def if_Type(Card: Card):
            if Card.CardType == CardType:
                return True
            else:
                return False
        return if_Type
    
    @classmethod
    def if_ClassName(cls, ClassName: ClassName):
        def if_Class(Card: Card):
            if Card.ClassName == ClassName:
                return True
            else:
                return False
        return if_Class
    
    
    @classmethod
    def if_AnyAnd(cls, *funcs):
        def if_And(Card):
            ans = True
            for func in funcs:
                if func(Card) == False:
                    ans = False
            return ans
        return if_And
    
    @classmethod
    def if_exist_match_card(cls, if_func):
        def if_exist(Leader, Opponent):
            ans = False
            for card in Leader.field:
                if if_func(card):
                    ans = True
            return ans
        return if_exist
    


    def SelectCard(self, if_func):
        def Select_if_match_card(Leader, Opponent):
            while True:
                CardIndex = input("")
                if CardIndex == 'q':
                    return False
                CardIndex = int(CardIndex)
                if CardIndex < 0 or CardIndex >= len(Leader.field):
                    print("There is not card")
                    continue
                SelectedCard = Leader.field[CardIndex]
                if if_func(SelectedCard):
                    self.SelectedCard.append(CardIndex)
                    break
                else:
                    print("That card is not Neutral-Follower")
                
        return Select_if_match_card
    

    def BuffSelectedFollowerNum(self, BuffNum):
        def BuffSelectedFollower(Leader, Opponent):
            if len(self.SelectedCard) != 0:
                Buffed_index = self.SelectedCard[0]
                Buffed = Leader.field[Buffed_index]
                Buffed.power += BuffNum[0]
                Buffed.MaxHealth += BuffNum[1]
                Buffed.health += BuffNum[1]
            return
        return BuffSelectedFollower



    

    
class Knight(Card):
    def __init__(self) -> None:
        super().__init__(ClassName.Neutral, Rarity.Bronze, 1, "Knight", CardType.Follower, 1, 1)

class Test1(Card):
    def Test1Fanfare(self, Leader, Opponent):
        knight = Knight()
        Leader.field.append(knight)
        Leader.Relocation()
    
    def __init__(self) -> None:
        super().__init__(ClassName.Neutral, Rarity.Bronze, 2, "test1", CardType.Follower, 2, 2, ability={"fanfare":self.SummonCardNum(Card(ClassName.Neutral, Rarity.Bronze, 1, "Knight", CardType.Follower, 1, 1), 1)})
    
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