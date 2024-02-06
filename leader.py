from card import ClassName, CardType, Card
from enum import Enum
from gamemaster import GameMaster

def handler(func, *args):
    return func(*args)


class LeaderEnum(Enum):
    Me       = 0
    Opponent = 1

class Leader():

    def __init__(self, LeaderType:ClassName, advance) -> None:
        self.LeaderType = LeaderType
        self.MaxHealth = 20
        self.Health = 20
        self.MaxPP = 0
        self.PP = 0
        self.cemetery = 0
        self.DeckNum = 40
        self.HandNum = 0
        self.advance = advance
        if self.advance == 1:
            self.EP = 2
        else:
            self.EP = 3
    


    
class Me(Leader):

    def __init__(self, LeaderType: ClassName, advance) -> None:
        super().__init__(LeaderType, advance)
        self.Hand = []

    def Play(self, CardName):
        existence = False
        for i in range(len(self.Hand)):
            if self.Hand[i].CardName == CardName:
                PlayCard = self.Hand[i]
                PlayIndex = i
                existence = True
                break
        if not existence:
            print(f"{CardName} is not in Hand")
            exit()
        if PlayCard.Cost > self.PP:
            print("There is not sufficient PP")
            exit()
        if len(GameMaster.field[LeaderEnum.Me]) == 5 and (PlayCard.CardType == CardType.Follower or PlayCard.CardType == CardType.Amulet):
            print("There is not sufficient space")
            exit()
        self.Hand.pop(PlayIndex)
        GameMaster.field[LeaderEnum.Me].append(PlayCard)
        if "fanfare" in PlayCard.ability:
            PlayCard.ability["fanfare"](self, GameMaster)
        


class Opponent(Leader):
    def __init__(self, LeaderType: ClassName, advance) -> None:
        super().__init__(LeaderType, advance)
        if self.advance == 1:
            GameMaster.WhosTurn = LeaderEnum.Opponent
        self.ConfirmedHand = []
        


