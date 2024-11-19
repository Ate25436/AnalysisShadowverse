#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import annotations

from enumerations import *
from gamemaster import GameMaster
from card import *

import random
from typing import List

def handler(func, *args):
    return func(*args)



class Leader():

    def __init__(self, Name: str, LeaderType:ClassName, advance: bool, Deck: List[Card], GameMaster: GameMaster) -> None:
        self.Name = Name
        self.LeaderType = LeaderType
        self.MaxHealth = 20
        self.Health = 20
        self.MaxPP = 0
        self.PP = 0
        self.cemetery = 0
        self.Hand = []
        self.advance = advance
        if self.advance:
            self.EP = 2
        else:
            self.EP = 3
        self.field = []
        self.Deck = Deck
        self.Evolvable = False
        self.Turn = 0
        self.GameMaster = GameMaster

    def Relocation(self):
        for i, card in enumerate(self.field):
            card.FieldLocation = i


    def Play(self, CardIndex, Opponent: Leader):
        #スペルをプレイするときは別途関数が必要だと思われる
        if CardIndex < 0 or CardIndex >= len(self.Hand):
            print("There is not card at that place")
            return
        PlayCard: Card = self.Hand[CardIndex]
        if "select_in_fanfare" in PlayCard.ability:
            if_exist = PlayCard.ability["select_in_fanfare"][0]
            select = PlayCard.ability["select_in_fanfare"][1]

            if if_exist(self, Opponent):
                result = select(self, Opponent)
                if result == False:
                    return
            
            elif PlayCard.CardType == CardType.Spell:
                print("There is no target")
                return
        
        
        if PlayCard.cost > self.PP:
            print("There is not sufficient PP")
            return
        if len(self.field) == 5 and (PlayCard.CardType == CardType.Follower or PlayCard.CardType == CardType.Amulet):
            print("There is not sufficient space")
            return
        self.Hand.pop(CardIndex)
        if PlayCard.CardType == CardType.Amulet or PlayCard.CardType == CardType.Follower:
            self.field.append(PlayCard)
        else:
            self.cemetery += 1
        self.PP -= PlayCard.cost
        self.Relocation()
        if "fanfare" in PlayCard.ability:
            handler(PlayCard.ability["fanfare"], self, Opponent)
        self.GameMaster.SolveLastWord()

    def Attack(self, AttackingIndex: int, AttackedIndex: int, Opponent: Leader):
        AttackedObject = "Follower"
        ExistShield = False
        if AttackedIndex == 6:
            AttackedObject = "Leader"
        if AttackingIndex < 0 or AttackingIndex >= len(self.field):
            print("There is not card at that place")
            return
        AttackingCard: Card = self.field[AttackingIndex]
        for card in Opponent.field:
            if "shield" in card.ability:
                ExistShield = True
                   
        if AttackingCard.CardType == CardType.Amulet or "unattackable" in AttackingCard.ability:
            print("That card is not able to attack")
            return
        if AttackedObject == "Follower":
            if AttackingCard.AttackAuthority == AttackAuthority.CantAttack:
                print("There is not sufficient authority")
                return
            if AttackedIndex < 0 or AttackedIndex >= len(Opponent.field):
                print("There is not card at that place")
                return
            AttackedCard: Card = Opponent.field[AttackedIndex]
            if "untouchable" in AttackedCard.ability or AttackedCard.CardType == CardType.Amulet:
                print("That card is untouchable")
                return
            if ExistShield and not("shield" in AttackedCard.ability):
                print("There is a Follower with shield")
                return

            if "attack" in AttackingCard.ability:
                self.GameMaster.EngagementQueue.append([AttackingCard.ability["attack"], self, Opponent])
            if "engagement" in AttackingCard.ability:
                self.GameMaster.EngagementQueue.append([AttackingCard.ability["engagement"], self, Opponent])

            if "engagement" in AttackedCard.ability:
                self.GameMaster.EngagementQueue.append([AttackedCard.ability["engagement"], Opponent, self])
            self.GameMaster.SolveEngagement()

            if AttackingCard.health <= 0:
                AttackingCard.Destroyed(self, Opponent)
            if AttackedCard.health <= 0:
                AttackedCard.Destroyed(Opponent, self)
            
            if not(AttackingCard.FieldLocation == -1 or AttackedCard.FieldLocation == -1):
                AttackingCard.health -= AttackedCard.power
                AttackedCard.health -= AttackingCard.power
                if AttackingCard.health <= 0:
                    AttackingCard.Destroyed(self, Opponent)
                if AttackedCard.health <= 0:
                    AttackedCard.Destroyed(Opponent, self)

                if "bane" in AttackingCard.ability:
                    AttackedCard.Destroyed()
                if "bane" in AttackedCard.ability:
                    AttackingCard.Destroyed()

        if AttackedObject == "Leader":
            if AttackingCard.AttackAuthority == AttackAuthority.CantAttack or AttackingCard.AttackAuthority == AttackAuthority.OnlyFollower:
                print("There is not sufficient authority")
                return
            if ExistShield :
                print("There is a Follower with shield")
                return
            
            if "attack" in AttackingCard.ability:
                handler(AttackingCard.ability["attack"], AttackingCard, self, Opponent)

            Opponent.Health -= AttackingCard.power
        self.GameMaster.SolveLastWord()
        AttackingCard.AttackAuthority = AttackAuthority.CantAttack

    def DrawCard(self):
        if len(self.Deck) > 0:
            i = random.randrange(len(self.Deck))
            self.Hand.append(self.Deck.pop(i))
        else:
            print("You Defeated")

    def DrawSpecificCard(self, CardName):
        for i, card in enumerate(self.Deck):
            if card.CardName == CardName:
                self.Hand.append(self.Deck.pop(i))
                return None
        print("There is not such a card in Deck")
            

    def TurnChange(self, Opponent: Leader):
        for card in self.field:
            if "EndTurn" in card.ability:
                self.GameMaster.EndTurnQueue.append([card.ability["EndTurn"], self, Opponent])
        
        for card in Opponent.field:
            if "EndOpponentTurn" in card.ability:
                self.GameMaster.EndTurnQueue.append([card.ability["EndOpponentTurn"], Opponent, self])

        self.GameMaster.SolveEndTurn()
        self.GameMaster.ChangeWhosTurn()

        for card in Opponent.field:
            if "StartTurn" in card.ability:
                self.GameMaster.StartQueue.append([card.ability["StartTurn"], card, Opponent])
        
        for card in self.field:
            if "StartOpponentTurn" in card.ability:
                self.GameMaster.StartTurnQueue.append([card.ability["StartOpponentTurn"], card, self])
        
        self.GameMaster.SolveStartTurn()

        Opponent.Turn += 1
        if (Opponent.advance == 0 and Opponent.Turn == 4) or (Opponent.advance == 1 and Opponent.Turn == 5):
            self.Evolvable = True
            
        for card in Opponent.field:
            if not "unattackable" in card.ability:
                card.AttackAuthority = AttackAuthority.Attackable
            if card.count > 0:
                card.count -= 1
                if card.count == 0:
                    card.Destroyed(Opponent, self)
        
        
        Opponent.DrawCard()
        if Opponent.Turn == 1 and Opponent.advance == False:
            Opponent.DrawCard()
        
        Opponent.MaxPP += 1
        Opponent.PP = Opponent.MaxPP


    def InsertToDeck(self, CardIndex: int):
        InsertCard: Card = self.Hand.pop(CardIndex)
        self.Deck.append(InsertCard)

    def Print(self):
        print(self.Name)
        print(f"LeaderType: {self.LeaderType}, MaxHealth: {self.MaxHealth}, Health: {self.Health}, MaxPP: {self.MaxPP}, PP: {self.PP}, cemetery: {self.cemetery}, advance: {self.advance}, EP: {self.EP}, Turn: {self.Turn}")
        print(*self.Hand)
        print(*self.field)
