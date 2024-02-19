#!/usr/bin/python
# -*- coding: utf-8 -*-
from enumerations import *
from collections import deque

def handler(func, *args):
    return func(*args)

class GameMaster():
    WhosTurn = LeaderEnum.Me
    LastWordQueue = []
    EndTurnQueue = []
    EngagementQueue = []
    StartTurnQueue = []
    
    def SolveEndTurn(self):
        while GameMaster.EndTurnQueue != []:
            ability = GameMaster.EndTurnQueue.pop(0)
            handler(ability[0], ability[1], ability[2])
        
    def ChangeWhosTurn(self):
        if GameMaster.WhosTurn == LeaderEnum.Me:
            GameMaster.WhosTurn = LeaderEnum.Opponent
        
        else:
            GameMaster.WhosTurn = LeaderEnum.Me

    def SolveStartTurn(self):
        while GameMaster.StartTurnQueue != []:
            ability = GameMaster.StartTurnQueue.pop(0)
            handler(ability[0], ability[1], ability[2])
    
    def SolveEngagement(self):
        while GameMaster.EngagementQueue != []:
            ability = GameMaster.EngagementQueue.pop(0)
            handler(ability[0], ability[1], ability[2])
    
    def SolveLastWord(self):
        while GameMaster.LastWordQueue != []:
            ability = GameMaster.LastWordQueue.pop(0)
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

