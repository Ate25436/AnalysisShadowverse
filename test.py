#!/usr/bin/python
# -*- coding: utf-8 -*-
from card import *
from leader import *
from gamemaster import *



test1 = Test1()
test3 = Test3()
knight1 = Knight()
knight2 = Knight()
knight3 = Knight()
knight4 = Knight()

GameMaster = GameMaster()
Player1 = Leader(ClassName.Nemesis, advance=1, Deck=[test3, knight1, knight3])
Player2 = Leader(ClassName.Dragon, advance=0, Deck=[test1, knight2, knight4])



Player1.DrawSpecificCard("test3")
Player2.DrawSpecificCard("test1")

Player1.MaxPP += 3
Player1.PP += 3
Player2.MaxPP += 3
Player2.PP += 3

Player1.Play(0, Opponent=Player2)
Player1.TurnChange(Opponent=Player2)
Player2.Play(0, Opponent=Player1)
Player2.TurnChange(Opponent=Player1)
Player1.Attack(0, 0, Opponent=Player2)
Player1.TurnChange(Opponent=Player2)
Player1.Print()
Player2.Print()

GameMaster.Print()