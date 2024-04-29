import pandas as pd
import copy

from card import *

def CardCopy(card):
    Copy = Card(card.ClassName, card.Rarity, card.cost, card.CardName, card.CardType, card.power, card.health, card.count, card.ability)
    return Copy

def AppendCard(deck, Card, Num):
    for i in range(Num):
        deck.append(CardCopy(Card))

deck1 = []
Goblin = Card(ClassName.Neutral, Rarity.Bronze, cost=1, name="Goblin", CardType=CardType.Follower, power=1, health=2, ability={})
AppendCard(deck1, Goblin, 3)
Fighter = Card(ClassName.Neutral, Rarity.Bronze, cost=1, name="Fighter", CardType=CardType.Follower, power=2, health=2, ability={})
AppendCard(deck1, Fighter, 3)
QuickBlader = Card(ClassName.Royal, Rarity.Bronze, cost=1, name="QuickBlader", CardType=CardType.Follower, power=1, health=1, ability={"sprint":True})
AppendCard(deck1, QuickBlader, 3)
WiseMerman = Card(ClassName.Neutral, Rarity.Bronze, cost=1, name="WiseMerman", CardType=CardType.Follower, power=1, health=1, ability={})
WiseMerman.ability["fanfare"] = WiseMerman.BuffSelectedFollowerNum((1, 0))
WiseMerman.ability["Select_in_Fanfare"] = [WiseMerman.if_exist_NeutralFollower, WiseMerman.SelectNeutralFollower]
AppendCard(deck1, WiseMerman, 3)