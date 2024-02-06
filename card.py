from enum import Enum

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

class Card():
    
    def __init__(self, classname:ClassName, rarity:int, cost:int, name:str, CardType:CardType, power:int=-1, health:int=-1, count:int=-1, ability={}) -> None:
        self.classname = classname
        self.rarity = rarity
        self.cost = cost
        self.name = name
        self.CardType = CardType
        self.power = power
        self.health = health
        self.count = count
        self.ability = ability
        self.AttackAuthority = AttackAuthority.CantAttack
    def __str__(self) -> str:
        return f"{self.name}"
    

