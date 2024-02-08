#!/usr/bin/python
# -*- coding: utf-8 -*-
from enumurations import *

class GameMaster():
    field = [[], []]
    WhosTurn = LeaderEnum.Me
    LastWordQueue = []

    def Print(self):
        for i in range(2):
            for j in range(len(self.field[i])):
                print(self.field[0][j].CardName, end=" ")
            print()
    
    def RearrangeLocation(self):
        for i in range(len(self.field)):
            for j in range(len(self.field[i])):
                self.field[i][j].FieldLocation = j
    
