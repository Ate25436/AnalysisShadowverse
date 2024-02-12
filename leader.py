#!/usr/bin/python
# -*- coding: utf-8 -*-

from enumurations import *
from gamemaster import GameMaster

import random

def handler(func, *args):
    return func(*args)



class Leader():

    def __init__(self, LeaderType:ClassName, advance, Deck) -> None:
        self.LeaderType = LeaderType
        self.MaxHealth = 20
        self.Health = 20
        self.MaxPP = 0
        self.PP = 0
        self.cemetery = 0
        self.HandNum = 0
        self.Hand = []
        self.advance = advance
        if self.advance == 1:
            self.EP = 2
        else:
            self.EP = 3
        self.field = []
        self.Deck = Deck

    def Relocation(self):
        for i, card in enumerate(self.field):
            card.FieldLocation = i


    def Play(self, CardIndex):
        if CardIndex < 0 or CardIndex >= len(self.Hand):
            print("There is not card at that place")
            exit()
        PlayCard = self.Hand[CardIndex]
        
        if PlayCard.cost > self.PP:
            print("There is not sufficient PP")
            exit()
        if len(self.field) == 5 and (PlayCard.CardType == CardType.Follower or PlayCard.CardType == CardType.Amulet):
            print("There is not sufficient space")
            exit()
        self.Hand.pop(CardIndex)
        self.field.append(PlayCard)
        self.PP -= PlayCard.cost
        self.Relocation()
        if "fanfare" in PlayCard.ability:
            handler(PlayCard.ability["fanfare"], PlayCard, self)

    def Attack(self, AttackingIndex, AttackedIndex, GameMaster, Opponent):
        AttackedObject = "Follower"
        if AttackedIndex == 6:
            AttackedObject = "Leader"
        if AttackingIndex < 0 or AttackingIndex >= len(self.field):
            print("There is not card at that place")
            exit()
        AttackingCard = self.field[AttackingIndex]
        if AttackingCard.CardType == CardType.Amulet or "unattackable" in AttackingCard.ability:
            print("That card is not able to attack")
            exit()
        if AttackedObject == "Follower":
            if AttackingCard.AttackAuthority == AttackAuthority.CantAttack:
                print("There is not sufficient authority")
                exit()
            if AttackedIndex < 0 or AttackedIndex >= len(Opponent.field):
                print("There is not card at that place")
                exit()
            AttackedCard = Opponent.field[AttackedIndex]
            if "untouchable" in AttackedCard.ability:
                print("That card is untouchable")
                exit()
            if "attack" in AttackingCard.ability:
                GameMaster.EngagementQueue.append([AttackingCard.ability["attack"], AttackingCard, self])
            if "engagement" in AttackingCard.ability:
                GameMaster.EngagementQueue.append([AttackingCard.ability["engagement"], AttackingCard, self])

            if "engagement" in AttackedCard.ability:
                GameMaster.EngagementQueue.append([AttackedCard.ability["engagement"], AttackedCard, Opponent])

            GameMaster.SolveEndTurn()
            
            if AttackingCard.health < 0:
                AttackingCard.Destroyed(self)
            if AttackedCard.health < 0:
                AttackedCard.Destroyed(Opponent)
            
            if AttackingCard.FieldLocation == -1 or AttackedCard.FieldLocation == -1:
                AttackingCard.health -= AttackedCard.power
                AttackedCard.health -= AttackingCard.power
                if AttackingCard.health < 0:
                    AttackingCard.Destroyed(self)
                if AttackedCard.health < 0:
                    AttackedCard.Destroyed(Opponent)

        if AttackedObject == "Leader":
            if AttackingCard.AttackAuthority == AttackAuthority.CantAttack or AttackingCard.AttackAuthority == AttackAuthority.OnlyFollower:
                print("There is not sufficient authority")
                exit()

            if "attack" in AttackingCard.ability:
                handler(AttackingCard.ability["attack"], AttackingCard, self)

            Opponent.health -= AttackingCard.power

    def DrawCard(self):
        i = random.randrange(len(self.Deck))
        self.Hand.append(self.Deck[i])

    def Print(self):
        print(f"LeaderType: {self.LeaderType}, MaxHealth: {self.MaxHealth}, Health: {self.Health}, MaxPP: {self.MaxPP}, PP: {self.PP}, cemetery: {self.cemetery}, advance: {self.advance}, EP: {self.EP}")
        for i in range(len(self.Hand)):
            print(self.Hand[i], end=" ")
        print()


        

        

    
    
    




