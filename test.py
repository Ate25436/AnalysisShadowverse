#!/usr/bin/python
# -*- coding: utf-8 -*-
from card import *
from leader import *
from gamemaster import *

test2_1 = Test2()
test2_2 = Test2()
knight1 = Knight()
knight2 = Knight()
knight3 = Knight()
knight4 = Knight()

Player1 = Leader(ClassName.Nemesis, advance=1, Deck=[test2_1, knight1, knight3])
Player2 = Leader(ClassName.Dragon, advance=0, Deck=[test2_2, knight2, knight4])
GameMaster = GameMaster()


Player1.DrawSpecificCard("test2")
Player2.DrawSpecificCard("test2")

Player1.MaxPP += 3
Player1.PP += 3
Player2.MaxPP += 3
Player2.PP += 3

Player1.Play(0)
Player1.TurnChange(GameMaster, Opponent=Player2)
Player2.Play(0)
Player2.TurnChange(GameMaster, Opponent=Player1)
Player1.Attack(1, 0, GameMaster, Opponent=Player2)
Player1.Print()
Player2.Print()
print(Player2.field[0].health)