#!/usr/bin/python
# -*- coding: utf-8 -*-
from enumerations import *
from collections import deque

def handler(func, *args):
    return func(*args)

class GameMaster():

    def __init__(self) -> None:
        self.WhosTurn = LeaderEnum.Me
        self.LastWordQueue = []
        self.EndTurnQueue = []
        self.EngagementQueue = []
        self.StartTurnQueue = []
    
    def SolveEndTurn(self):
        while self.EndTurnQueue != []:
            ability = self.EndTurnQueue.pop(0)
            handler(ability[0], ability[1], ability[2])
    
    def ChangeWhosTurn(self):
        if self.WhosTurn == LeaderEnum.Me:
            self.WhosTurn = LeaderEnum.Opponent
        
        else:
            self.WhosTurn = LeaderEnum.Me

    def SolveStartTurn(self):
        while self.StartTurnQueue != []:
            ability = self.StartTurnQueue.pop(0)
            handler(ability[0], ability[1], ability[2])
    
    def SolveEngagement(self):
        while self.EngagementQueue != []:
            ability = self.EngagementQueue.pop(0)
            handler(ability[0], ability[1], ability[2])

    def SolveLastWord(self):
        while self.LastWordQueue != []:
            ability = self.LastWordQueue.pop(0)
            handler(ability[0], ability[1], ability[2])

    def Print(self):
        print(f"WhosTurn: {self.WhosTurn}")
        print("LastWord: ", end="")
        print(*self.LastWordQueue)
        print("EndTurn: ", end="")
        print(*self.EndTurnQueue)
        print("Engagement: ", end="")
        print(*self.EngagementQueue)
        print("StartTurn: ", end="")
        print(*self.StartTurnQueue)

