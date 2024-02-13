#!/usr/bin/python
# -*- coding: utf-8 -*-
from enumurations import *

def handler(func, *args):
    return func(*args)

class GameMaster():
    WhosTurn = LeaderEnum.Me
    LastWordQueue = []
    EndTurnQueue = []
    EngagementQueue = []
    StartTurnQueue = []
    def Print(self):
        for i in range(2):
            for j in range(len(GameMaster.field[i])):
                print(GameMaster.field[0][j].CardName, end=" ")
            print()
    
    def SolveEndTurn(self):
        for ability in GameMaster.EndTurnQueue:
            handler(ability[0], ability[1], ability[2])
        
    def ChangeWhosTurn(self):
        if GameMaster.WhosTurn == LeaderEnum.Me:
            GameMaster.WhosTurn = LeaderEnum.Opponent
        
        else:
            GameMaster.WhosTurn = LeaderEnum.Me

    def SolveStartTurn(self):
        for ability in GameMaster.StartTurnQueue:
            handler(ability[0], ability[1], ability[2])

