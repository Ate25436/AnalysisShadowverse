#!/usr/bin/python
# -*- coding: utf-8 -*-
from card import *
from leader import *
from gamemaster import *

Me = Me(ClassName.Nemesis, advance=1)
Opponent = Opponent(ClassName.Dragon, advance=0)
test1 = test1()
Me.DrawCard(test1)
Me.MaxPP += 2
Me.PP += 2
Me.Play("test1")
Me.Print()
GameMaster = GameMaster()
GameMaster.Print()