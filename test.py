#!/usr/bin/python
# -*- coding: utf-8 -*-
from card import *
from leader import *
from gamemaster import *

test2 = Test2()

Me = Leader(ClassName.Nemesis, advance=1, Deck=[test2])
Opponent = Leader(ClassName.Dragon, advance=0, Deck=[test2])



Me.DrawCard()
Opponent.DrawCard()

Me.MaxPP += 3
Me.PP += 3
Opponent.MaxPP += 3
Opponent.PP += 3

Me.Play(0)
Opponent.Play(test2)
Me.Print()
GameMaster = GameMaster()
GameMaster.Print()