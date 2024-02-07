#!/usr/bin/python
# -*- coding: utf-8 -*-
from enumurations import *

class GameMaster():
    field = [[], []]
    WhosTurn = LeaderEnum.Me

    def Print(self):
        for i in range(2):
            for j in range(len(self.field[i])):
                print(self.field[0][j].CardName, end=" ")
            print()
