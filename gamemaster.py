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
    
    @classmethod
    def SolveEndTurn(cls):
        while GameMaster.EndTurnQueue != []:
            ability = GameMaster.EndTurnQueue.pop(0)
            handler(ability[0], ability[1], ability[2])
    
    @classmethod
    def ChangeWhosTurn(cls):
        if GameMaster.WhosTurn == LeaderEnum.Me:
            GameMaster.WhosTurn = LeaderEnum.Opponent
        
        else:
            GameMaster.WhosTurn = LeaderEnum.Me

    @classmethod
    def SolveStartTurn(cls):
        while GameMaster.StartTurnQueue != []:
            ability = GameMaster.StartTurnQueue.pop(0)
            handler(ability[0], ability[1], ability[2])
    
    @classmethod
    def SolveEngagement(cls):
        while GameMaster.EngagementQueue != []:
            ability = GameMaster.EngagementQueue.pop(0)
            handler(ability[0], ability[1], ability[2])
    
    @classmethod
    def SolveLastWord(cls):
        while GameMaster.LastWordQueue != []:
            ability = GameMaster.LastWordQueue.pop(0)
            handler(ability[0], ability[1], ability[2])

    @classmethod
    def Print(cls):
        print(f"WhosTurn: {GameMaster.WhosTurn}")
        print("LastWord: ", end="")
        print(*GameMaster.LastWordQueue)
        print("EndTurn: ", end="")
        print(*GameMaster.EndTurnQueue)
        print("Engagement: ", end="")
        print(*GameMaster.EngagementQueue)
        print("StartTurn: ", end="")
        print(*GameMaster.StartTurnQueue)

