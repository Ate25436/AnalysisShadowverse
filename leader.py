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
        self.HandNum -= 1
        GameMaster.field[LeaderEnum.Me].append(PlayCard)
        self.PP -= PlayCard.cost
        GameMaster.RearrangeLocation()
        if "fanfare" in PlayCard.ability:
            PlayCard.ability["fanfare"](GameMaster, LeaderEnum.Me)
        
    def Attack(self, AttackingIndex, AttackedIndex, GameMaster, Opponent):
        AttackedObject = "Follower"
        if AttackedIndex == 6:
            AttackedObject = "Leader"
        if AttackingIndex < 0 or AttackingIndex >= len(GameMaster.field[LeaderEnum.Me]):
            print("There is not card at that place")
            exit()
        AttackingCard = GameMaster.field[LeaderEnum.Me][AttackingIndex]
        if AttackingCard.CardType == CardType.Amulet or "unattackable" in AttackingCard.ability:
            print("That card is not able to attack")
            exit()
        if AttackedObject == "Follower":
            if AttackingCard.AttackAuthority == AttackAuthority.CantAttack:
                print("There is not sufficient authority")
                exit()
            if AttackedIndex < 0 or AttackedIndex >= len(GameMaster.field[LeaderEnum.Opponent]):
                print("There is not card at that place")
                exit()
            AttackedCard = GameMaster.field[LeaderEnum.Opponent][AttackedIndex]
            if "untouchable" in AttackedCard.ability:
                print("That card is untouchable")
                exit()
            if "attack" in AttackingCard.ability:
                AttackingCard.ability["attack"](GameMaster, LeaderEnum.Me)
            if "engagement" in AttackingCard.ability:
                AttackingCard.ability["engagement"](GameMaster, LeaderEnum.Me)
            
            if "engagement" in AttackedCard.ability:
                AttackedCard.ability["engagement"](GameMaster, LeaderEnum.Opponent)

            if AttackingCard.health < 0:
                AttackingCard.Destroyed(GameMaster, LeaderEnum.Me)
            if AttackedCard.health < 0:
                AttackedCard.Destroyed(GameMaster, LeaderEnum.Opponent)
            
            AttackingCard.health -= AttackedCard.power
            AttackedCard.health -= AttackingCard.power
            if AttackingCard.health < 0:
                AttackingCard.Destroyed(GameMaster, LeaderEnum.Me)
            if AttackedCard.health < 0:
                AttackedCard.Destroyed(GameMaster, LeaderEnum.Opponent)

        if AttackedObject == "Leader":
            if AttackingCard.AttackAuthority == AttackAuthority.CantAttack or AttackingCard.AttackAuthority == AttackAuthority.OnlyFollower:
                print("There is not sufficient authority")
                exit()
            if AttackedIndex < 0 or AttackedIndex >= len(GameMaster.field[LeaderEnum.Opponent]):
                print("There is not card at that place")
                exit()
            if "attack" in AttackingCard.ability:
                AttackingCard.ability["attack"](GameMaster, LeaderEnum.Me)

            Opponent.health -= AttackingCard.power
            
            

        

    def DrawCard(self, Card:Card):
        self.Hand.append(Card)
        self.HandNum += 1
        self.DeckNum -= 1
    
    def Print(self):
        print(f"LeaderType: {self.LeaderType}, MaxHealth: {self.MaxHealth}, Health: {self.Health}, MaxPP: {self.MaxPP}, PP: {self.PP}, cemetery: {self.cemetery}, DeckNum: {self.DeckNum}, HandNum: {self.HandNum}, advance: {self.advance}, EP: {self.EP}")
        for i in range(len(self.Hand)):
            print(self.Hand[i], end=" ")
        print()

class Opponent(Leader):
    def __init__(self, LeaderType: ClassName, advance) -> None:
        super().__init__(LeaderType, advance)
        if self.advance == 1:
            GameMaster.WhosTurn = LeaderEnum.Opponent
        self.ConfirmedHand = []
        
    
    def Print(self):
        print(f"LeaderType: {self.LeaderType}, MaxHealth: {self.MaxHealth}, Health: {self.Health}, MaxPP: {self.MaxPP}, PP: {self.PP}, cemetery: {self.cemetery}, DeckNum: {self.DeckNum}, HandNum: {self.HandNum}, advance: {self.advance}, EP: {self.EP}")


