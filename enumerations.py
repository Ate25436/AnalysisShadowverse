#!/usr/bin/python
# -*- coding: utf-8 -*-
from enum import Enum, IntEnum

class ClassName(Enum):
    Neutral     = 0 #ニュートラル
    Elf         = 1 #エルフ
    Royal       = 2 #ロイヤル
    Witch       = 3 #ウィッチ
    Dragon      = 4 #ドラゴン
    Necromancer = 5 #ネクロマンサー
    Vampire     = 6 #ヴァンパイア
    Bishop      = 7 #ビショップ
    Nemesis     = 8 #ネメシス

class CardType(Enum):
    Follower = 0 #フォロワー
    Spell    = 1 #スペル
    Amulet   = 2 #アミュレット

class AttackAuthority(Enum):
    CantAttack   = 0 #攻撃不可
    OnlyFollower = 1 #フォロワーにのみ攻撃可能
    Attackable   = 2 #フォロワー，リーダーともに攻撃可能

class Rarity(Enum):
    Bronze = 0
    Silver = 1
    Gold   = 2
    Legend = 3

class LeaderEnum(IntEnum):
    Me       = 0
    Opponent = 1