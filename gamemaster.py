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
    def Print(self):
        for i in range(2):
            for j in range(len(self.field[i])):
                print(self.field[0][j].CardName, end=" ")
            print()
    
    def RearrangeLocation(self):
        for i in range(len(self.field)):
            for j in range(len(self.field[i])):
                self.field[i][j].FieldLocation = j
    
    def SolveEndTurn(self):
        for ability in self.EndTurnQueue:
            handler(ability[0], ability[1], ability[2])
