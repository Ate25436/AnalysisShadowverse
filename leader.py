#!/usr/bin/python
# -*- coding: utf-8 -*-
from card import ClassName, CardType, Card, AttackAuthority
from enumurations import *
from gamemaster import GameMaster

def handler(func, *args):
    return func(*args)



class Leader():

    def __init__(self, LeaderType:ClassName, advance) -> None:
        self.LeaderType = LeaderType
        self.MaxHealth = 20
        self.Health = 20
        self.MaxPP = 0
        self.PP = 0
        self.cemetery = 0
        self.DeckNum = 40
        self.HandNum = 0
        self.advance = advance
        if self.advance == 1:
            self.EP = 2
        else:
            self.EP = 3
        self.Information = [self.LeaderType, self.MaxHealth, self.Health, self.MaxPP, self.PP, self.cemetery, self.DeckNum, self.HandNum, self.advance, self.EP]


    
class Me(Leader):

    def __init__(self, LeaderType: ClassName, advance) -> None:
        super().__init__(LeaderType, advance)
        self.Hand = []

    def Play(self, CardName):
        existence = False
        for i in range(len(self.Hand)):
            if self.Hand[i].CardName == CardName:
                PlayCard = self.Hand[i]
                PlayIndex = i
                existence = True
                break
        if not existence:
            print(f"{CardName} is not in Hand")
            exit()
        if PlayCard.cost > self.PP:
            print("There is not sufficient PP")
            exit()
        if len(GameMaster.field[LeaderEnum.Me]) == 5 and (PlayCard.CardType == CardType.Follower or PlayCard.CardType == CardType.Amulet):
            print("There is not sufficient space")
            exit()
        self.Hand.pop(PlayIndex)
        GameMaster.field[LeaderEnum.Me].append(PlayCard)
        if "fanfare" in PlayCard.ability:
            PlayCard.ability["fanfare"](GameMaster, LeaderEnum.Me)
        
    def Attack(self, AttackingName, AttackedName, GameMaster):
        existence = False
        for i in range(len(GameMaster.field[LeaderEnum.Me])):
            if GameMaster.field[LeaderEnum.Me][i].CardName == AttackingName:
                AttackingCard = GameMaster.field[LeaderEnum.Me][i]
                AttackingIndex = i
                existence = True
                break
        if not existence:
            print("Selected object is not exist in your field")
            exit()
        
        existence = False
        for i in range(len(GameMaster.field[LeaderEnum.Opponent])):
            if GameMaster.field[LeaderEnum.Opponent][i].CardName == AttackedName:
                AttackedCard = GameMaster.field[LeaderEnum.Me][i]
                AttackedIndex = i
                existence = True
                break
        if AttackedName == "leader":
            existence = True

        if not existence:
            print("Selected object is not exist in your opponent field")
            exit()

        if AttackedName == "leader" and (AttackingCard.AttackAuthority == AttackAuthority.CantAttack or AttackingCard.AttackAuthority == AttackAuthority.OnlyFollower):
            print(f"{AttackingCard.CardName} does not have sufficient authority")
            exit()
        elif AttackedName != "leader" and (AttackingCard.AttackAuthority == AttackAuthority.CantAttack):
            print(f"{AttackingCard.CardName} does not have sufficient authority")
            exit()

        if AttackedName == "leader":
            if "Attack" in AttackingCard.ability:
                AttackingCard.ability["Attack"](GameMaster)
        else:
            if "Attack" in AttackingCard.ability:
                AttackingCard.ability["Attack"](GameMaster)

            if "engagement" in AttackingCard.ability:
                AttackingCard.ability["engagement"](GameMaster)
            
            if "engagement" in AttackedCard.ability:
                AttackedCard.ability["engagement"](GameMaster)
        AttackingCard.health -= AttackedCard.power
        AttackedCard.health -= AttackingCard.power
        if AttackingCard.health < 0:
            AttackingCard.Destroyed()
        if AttackedCard.health < 0:
            AttackedCard.Destroyed()


    def DrawCard(self, Card:Card):
        self.Hand.append(Card)
        self.HandNum += 1
    
    def Print(self):
        print(*self.Information)

class Opponent(Leader):
    def __init__(self, LeaderType: ClassName, advance) -> None:
        super().__init__(LeaderType, advance)
        if self.advance == 1:
            GameMaster.WhosTurn = LeaderEnum.Opponent
        self.ConfirmedHand = []
        


