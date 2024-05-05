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

WiseMerman = Card(ClassName.Neutral, Rarity.Bronze, cost=1, name="WiseMerman", CardType=CardType.Follower, power=1, health=1, ability={"select_in_fanfare":[Card.if_exist_match_card(Card.if_AnyAnd(Card.if_CardType(CardType.Follower), Card.if_ClassName(ClassName.Neutral))), None]})
WiseMerman.ability["fanfare"] = WiseMerman.BuffSelectedFollowerNum((1, 0))
WiseMerman.ability["select_in_fanfare"][1] = WiseMerman.SelectCard(Card.if_AnyAnd(Card.if_CardType(CardType.Follower), Card.if_ClassName(ClassName.Neutral)))
AppendCard(deck1, WiseMerman, 3)

Minotaur = Card(ClassName.Neutral, Rarity.Bronze, 1, "Minotaur", CardType.Follower, 2, 1, ability={"shield":True})
AppendCard(deck1, Minotaur, 3)

Dancer_of_Unicorn_Unico = Card(ClassName.Neutral, Rarity.Silver, 2, "Dancer_of_Unicorn_Unico", CardType.Follower, 2, 2, ability={"EndTurn":Card.LeaderHealNum(2)})
AppendCard(deck1, Dancer_of_Unicorn_Unico, 3)

Wander_Mercenary = Card(ClassName.Neutral, Rarity.Bronze, 3, "Wander_Mercenary", CardType.Follower, 3, 2)
AppendCard(deck1, Wander_Mercenary, 3)

Healing_Angel = Card(ClassName.Neutral, Rarity.Bronze, 3, "Healing_Angel", CardType.Follower, 2, 3, ability={"fanfare":Card.LeaderHealNum(2)})
AppendCard(deck1, Healing_Angel, 3)

Goblin_Leader = Card(ClassName.Neutral, Rarity.Bronze, 3, "Goblin_Leader", CardType.Follower, 1, 2, ability={"EndTurn":Card.SummonCardNum(Goblin, 1)})
AppendCard(deck1, Goblin_Leader, 3)

Pure_Singer = Card(ClassName.Neutral, Rarity.Silver, 3, "Pure_Singer", CardType.Follower, 1, 2, ability={"fanfare":Card.DrawCardNum(1), "LastWord":Card.DrawCardNum(1)})
AppendCard(deck1, Pure_Singer, 3)

Skewers_Trap = Card(ClassName.Neutral, Rarity.Bronze, 3, "Skewers_Trap", CardType.Spell, ability={"fanfare":Card.FuncSequence(Card.FollowerDestroy, Card.LeaderDamageNum(2))})
AppendCard(deck1, Skewers_Trap, 3)

Novice_Trooper = Card(ClassName.Royal, Rarity.Bronze, 3, "Novice_Trooper", CardType.Follower, 2, 2, ability={"sprint":True})
AppendCard(deck1, Novice_Trooper, 3)

Goliath = Card(ClassName.Neutral, Rarity.Bronze, 4, "Goliath", CardType.Follower, 3, 4)
AppendCard(deck1, Goliath, 3)

Death_Dance = Card(ClassName.Neutral, Rarity.Bronze, 5, "Death_Dance", CardType.Spell, ability={"fanfare":Card.FuncSequence(Card.FollowerDestroy, Card.LeaderDamageNum(2))})
AppendCard(deck1, Death_Dance, 1)
