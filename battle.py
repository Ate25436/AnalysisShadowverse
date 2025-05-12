import random

from card import *
from leader import *
from gamemaster import *


card_map = {
    "Goblin": Card(ClassName.Neutral, Rarity.Bronze, cost=1, name="Goblin", CardType=CardType.Follower, power=1, health=2, ability={}),
    "Fighter": Card(ClassName.Neutral, Rarity.Bronze, cost=2, name="Fighter", CardType=CardType.Follower, power=2, health=2, ability={}),
    "Quick_Blader": Card(ClassName.Royal, Rarity.Bronze, cost=1, name="Quick_Blader", CardType=CardType.Follower, power=1, health=1, ability={"sprint":True}),
    "Wise_Merman": Card(ClassName.Neutral, Rarity.Bronze, cost=1, name="Wise_Merman", CardType=CardType.Follower, power=1, health=1, ability={"select_in_fanfare":[Card.if_exist_match_card(Card.if_AnyAnd(Card.if_CardType(CardType.Follower), Card.if_ClassName(ClassName.Neutral))), None]}),
    "Minotaur": Card(ClassName.Neutral, Rarity.Bronze, 2, "Minotaur", CardType.Follower, 2, 1, ability={"shield":True}),
    "Dancer_of_Unicorn_Unico": Card(ClassName.Neutral, Rarity.Silver, 2, "Dancer_of_Unicorn_Unico", CardType=CardType.Follower, power=2, health=2, ability={"EndTurn":Card.LeaderHealNum(2)}),
    "Wander_Mercenary": Card(ClassName.Neutral, Rarity.Bronze, 3, "Wander_Mercenary", CardType=CardType.Follower, power=3, health=2),
    "Healing_Angel": Card(ClassName.Neutral, Rarity.Bronze, 3, "Healing_Angel", CardType=CardType.Follower, power=2, health=3, ability={"fanfare":Card.LeaderHealNum(2)}),
    "Pure_Singer": Card(ClassName.Neutral, Rarity.Silver, 3, "Pure_Singer", CardType=CardType.Follower, power=1, health=2, ability={"fanfare":Card.DrawCardNum(1), "LastWord":Card.DrawCardNum(1)}),
    "Skewers_Trap": Card(ClassName.Neutral, Rarity.Bronze, 3, "Skewers_Trap", CardType=CardType.Spell, ability={"fanfare":Card.FuncSequence(Card.FollowerDestroy, Card.LeaderDamageNum(2))}),
    "Novice_Trooper": Card(ClassName.Royal, Rarity.Bronze, 3, "Novice_Trooper", CardType=CardType.Follower, power=2, health=2, ability={"sprint":True}),
    "Goliath": Card(ClassName.Neutral, Rarity.Bronze, 4, "Goliath", CardType=CardType.Follower, power=3, health=4),
    "Death_Dance": Card(ClassName.Neutral, Rarity.Bronze, 5, "Death_Dance", CardType=CardType.Spell, ability={"fanfare":Card.FuncSequence(Card.FollowerDestroy, Card.LeaderDamageNum(2))}),
}

card_map["Goblin_Leader"] = Card(ClassName.Neutral, Rarity.Bronze, 3, "Goblin_Leader", CardType=CardType.Follower, power=1, health=2, ability={"EndTurn":Card.SummonCardNum(card_map["Goblin"], 1)})


card_map["Wise_Merman"].ability["fanfare"] = card_map["Wise_Merman"].BuffSelectedFollowerNum((1, 0))
card_map["Wise_Merman"].ability["select_in_fanfare"][1] = card_map["Wise_Merman"].SelectCard(Card.if_AnyAnd(Card.if_CardType(CardType.Follower), Card.if_ClassName(ClassName.Neutral)))

def CardCopy(card):
    Copy = Card(card.ClassName, card.Rarity, card.cost, card.CardName, card.CardType, card.power, card.health, card.count, card.ability)
    return Copy

def AppendCard(deck, Card, Num):
    for i in range(Num):
        deck.append(CardCopy(Card))

def make_deck():

    deck1 = []
    Goblin = Card(ClassName.Neutral, Rarity.Bronze, cost=1, name="Goblin", CardType=CardType.Follower, power=1, health=2, ability={})
    AppendCard(deck1, Goblin, 3)

    Fighter = Card(ClassName.Neutral, Rarity.Bronze, cost=2, name="Fighter", CardType=CardType.Follower, power=2, health=2, ability={})
    AppendCard(deck1, Fighter, 3)

    QuickBlader = Card(ClassName.Royal, Rarity.Bronze, cost=1, name="Quick_Blader", CardType=CardType.Follower, power=1, health=1, ability={"sprint":True})
    AppendCard(deck1, QuickBlader, 3)

    WiseMerman = Card(ClassName.Neutral, Rarity.Bronze, cost=1, name="Wise_Merman", CardType=CardType.Follower, power=1, health=1, ability={"select_in_fanfare":[Card.if_exist_match_card(Card.if_AnyAnd(Card.if_CardType(CardType.Follower), Card.if_ClassName(ClassName.Neutral))), None]})
    WiseMerman.ability["fanfare"] = WiseMerman.BuffSelectedFollowerNum((1, 0))
    WiseMerman.ability["select_in_fanfare"][1] = WiseMerman.SelectCard(Card.if_AnyAnd(Card.if_CardType(CardType.Follower), Card.if_ClassName(ClassName.Neutral)))
    AppendCard(deck1, WiseMerman, 3)

    Minotaur = Card(ClassName.Neutral, Rarity.Bronze, 2, "Minotaur", CardType.Follower, 2, 1, ability={"shield":True})
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

    return deck1

def one_Nth_part(n):
    return random.randrange(n)

def GameStart(Me: Leader, Opponent: Leader):
    for i in range(3):
        Me.DrawCard()
        Opponent.DrawCard()
    
    #マリガン
    Me.Print()
    switch_list = list(map(int, input('Input Switch Number(Space Separated): ').split()))
    switch_list = sorted(switch_list, reverse=True)
    print(switch_list)
    if len(switch_list) != 0:
        for index in switch_list:
            Me.InsertToDeck(index)
        for i in switch_list:
            Me.DrawCard()
        Me.Print()
    Opponent.Print()
    switch_list = list(map(int, input('Input Switch Number(Space Separated): ').split()))
    switch_list = sorted(switch_list, reverse=True)
    print(switch_list)
    if len(switch_list) != 0:
        for index in switch_list:
            Opponent.InsertToDeck(index)
        for i in switch_list:
            Opponent.DrawCard()
        Opponent.Print()
    if Me.advance == True:
        Me.MaxPP += 1
        Me.PP = Me.MaxPP
        Me.DrawCard()
        Me.Turn += 1
    else:
        Opponent.MaxPP += 1
        Opponent.PP = Opponent.MaxPP
        Opponent.DrawCard()
        Opponent.Turn += 1
    
    
def InputInt(message):
    input_str = input(message)
    while not input_str.isdecimal():
        print("Invalid String")
        input_str = input(message)
    return int(input_str)

def main():
    deck1 = make_deck()
    deck2 = make_deck()
    GameMaster1 = GameMaster()
    if one_Nth_part(2) == 1:
        advance = True
        GameMaster1.WhosTurn = LeaderEnum.Me
    else:
        advance = False
        GameMaster1.WhosTurn = LeaderEnum.Opponent
    
    Me = Leader("Me", ClassName.Royal, advance, deck1, GameMaster1)
    Opponent = Leader("Opponent", ClassName.Royal, not advance, deck2, GameMaster1)
    #GameStart
    GameStart(Me, Opponent)
    debug = False
    while True:
        PlayerEnum = GameMaster1.WhosTurn
        if PlayerEnum == LeaderEnum.Me:
            Me.Print()
            TurnPlayer = Me
            OtherPlayer = Opponent
        else:
            Opponent.Print()
            TurnPlayer = Opponent
            OtherPlayer = Me
        if debug == False:
            command = input("Input \'p\', \'a\', \'end\', \'evolve\', \'q\', \'debug\' or \'help\'(\'help\' display what commands mean).: ")
        else:
            command = input("Input \'add_hand\', \'add_field\', \'damage_leader\', \'set_PP\', \'exit\', \'demonstrate_fanfare_heal\', \'demonstrate_fanfare_select\': ")
        if debug == False and command == 'help':
            print("-\'p\'...Play Card\n-\'a\'...Attack Card\n-\'e\'...End Turn\n-\'q\'...Quit Game\n-\'help\'...Print This Message")
        elif command == 'debug':
            debug = True
            continue
        elif debug == False and command == 'q':
            break
        elif debug == False and command == 'p':
            CardIndex = InputInt(f"Input card index(0-{max(len(TurnPlayer.Hand) - 1, 0)}): ")
            TurnPlayer.Play(CardIndex, OtherPlayer)

        elif debug == False and command == 'a':
            AttackIndex = InputInt(f"Input card index(0-{max(len(TurnPlayer.field) - 1, 0)}): ")
            AttackedIndex = InputInt(f"Input card index(0-{max(len(OtherPlayer.field) - 1, 0)} or 6): ")
            TurnPlayer.Attack(AttackIndex, AttackedIndex, OtherPlayer)
        
        elif debug == False and command == 'end':
            TurnPlayer.TurnChange(OtherPlayer)
        
        elif debug == False and command == 'evolve':
            CardIndex = InputInt(f"Input card index(0-{max(len(TurnPlayer.field) - 1, 0)}): ")
            TurnPlayer.Evolve(CardIndex, OtherPlayer)
        
        elif debug == True and command == 'add_hand':
            card_name = input("Input card name: ")
            player_name = input("Input player name: ")
            if player_name == "Me":
                Player = Me
            else:
                Player = Opponent
            Player.Hand.append(card_map[card_name])
        
        elif debug == True and command == 'add_field':
            card_name = input("Input card name: ")
            player_name = input("Input player name: ")
            if player_name == "Me":
                Player = Me
            else:
                Player = Opponent
            Player.field.append(card_map[card_name])
        
        elif debug == True and command == 'damage_leader':
            damage = InputInt("Input damage: ")
            player_name = input("Input player name: ")
            if player_name == "Me":
                Player = Me
            else:
                Player = Opponent
            Player.Health -= damage
        
        elif debug == True and command == 'set_PP':
            PP = InputInt("Input PP: ")
            player_name = input("Input player name: ")
            if player_name == "Me":
                Player = Me
            else:
                Player = Opponent
            Player.PP = PP

        elif debug == True and command == 'demonstrate_fanfare_heal':
            TurnPlayer.Hand.append(card_map["Healing_Angel"])
            TurnPlayer.PP = 3
            TurnPlayer.Health = 18

        elif debug == True and command == 'demonstrate_fanfare_select':
            TurnPlayer.Hand.append(card_map["Wise_Merman"])
            TurnPlayer.PP = 3
            TurnPlayer.field.append(card_map["Goblin"])
        
        elif debug == True and command == 'exit':
            debug = False
            continue


if __name__ == '__main__':
    main()
