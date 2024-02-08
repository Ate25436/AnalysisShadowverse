#!/usr/bin/python
# -*- coding: utf-8 -*-
from card import *
from leader import *
from gamemaster import *

Me = Me(ClassName.Nemesis, advance=1)
Opponent = Opponent(ClassName.Dragon, advance=0)
test2 = Test2()
Me.DrawCard(test2)
Me.MaxPP += 3
Me.PP += 3
Me.Play("test2")
Me.Print()
GameMaster = GameMaster()
GameMaster.Print()