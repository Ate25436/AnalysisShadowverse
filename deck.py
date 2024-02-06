import random

class Deck():

    def __init__(self, CardList):
        self.CardList = CardList

    def Draw(self):
        index = random.randrange(len(self.CardList))
        return self.CardList.pop(index)

    def Add(self, CardList):
        for i in range(len(CardList)):
            self.CardList.append(CardList)
    
    def Vanish(self, Num):
        for i in range(Num):
            index = random.randrange(len(self.CardList))
            self.CardList.pop(index)
        