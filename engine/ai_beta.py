from engine.objects import GameObjects, GamblerInfo
from engine.engine import combination, combination_Egor, translate
from random import randint


def win_chance(hand: list, table: list, players: int) -> float:
    """Calculates chance of win or tie with current hand and table"""
    hhand = []
    ttable = []
    for i in hand:
        hhand.append(translate(i))
    for i in table:
        ttable.append(translate(i))
    t = count = 0
    deck = [
            [2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [7, 1], [8, 1], [9, 1], [10, 1], [11, 1], [12, 1], [13, 1], [14, 1], 
            [2, 2], [3, 2], [4, 2], [5, 2], [6, 2], [7, 2], [8, 2], [9, 2], [10, 2], [11, 2], [12, 2], [13, 2], [14, 2], 
            [2, 3], [3, 3], [4, 3], [5, 3], [6, 3], [7, 3], [8, 3], [9, 3], [10, 3], [11, 3], [12, 3], [13, 3], [14, 3], 
            [2, 4], [3, 4], [4, 4], [5, 4], [6, 4], [7, 4], [8, 4], [9, 4], [10, 4], [11, 4], [12, 4], [13, 4], [14, 4]
            ]
    
    for i in hhand:
        del deck[deck.index(i)]
    for i in ttable:
        del deck[deck.index(i)]
    for i1 in range(0, len(deck)-1):
        for i2 in range(i1+1, len(deck)):
            v1_hand = [deck[i1], deck[i2]]
            v1_score = combination_Egor(v1_hand, ttable)
            score = combination(hand, table)[0]
            if score >= v1_score:
                t += 1
            count += 1
    return round(t/count, 3)


def bluff_turn(ai: GamblerInfo, table: list, bet: (int, float), blind: (int, float)) -> str:
    """Calculates the relevance of bluff and returns bet/raise"""
    score = 0
    ttable = []
    for i in table:
        ttable.append(translate(i))
    deck = [
            [2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [7, 1], [8, 1], [9, 1], [10, 1], [11, 1], [12, 1], [13, 1], [14, 1], 
            [2, 2], [3, 2], [4, 2], [5, 2], [6, 2], [7, 2], [8, 2], [9, 2], [10, 2], [11, 2], [12, 2], [13, 2], [14, 2], 
            [2, 3], [3, 3], [4, 3], [5, 3], [6, 3], [7, 3], [8, 3], [9, 3], [10, 3], [11, 3], [12, 3], [13, 3], [14, 3], 
            [2, 4], [3, 4], [4, 4], [5, 4], [6, 4], [7, 4], [8, 4], [9, 4], [10, 4], [11, 4], [12, 4], [13, 4], [14, 4]
            ]
    ai_bet = {
        1 : 0.05,
        2 : randint(5, 15)/100 ,
        3 : randint(10, 20)/100,
        4 : randint(25, 35)/100,
        5 : randint(40, 60)/100,
        6 : randint(40, 60)/100,
        7 : randint(75, 85)/100,
        8 : randint(90, 100)/100,
        9 : 1,
    }
    for i in ttable:
        del deck[deck.index(i)]
    for i1 in range(0, len(deck)-1):
        for i2 in range(i1, len(deck)):
            v_hand = [deck[i1], deck[i2]]
            score = max(score, combination_Egor(v_hand, ttable))
    if bet == 0:
        if ai.bal >= ai_bet[int(score)]:
            return f"Bet={((ai.bal * ai_bet[int(score)])//(0.5 * blind))*(blind * 0.5)}"
        else:
            return f"Bet={ai.bal}"
    else:
        if ai.bal * ai_bet[int(score)] >= blind and ai.bal >= (bet - ai.bet) + ai.bal * ai_bet[int(score)]:
            return f"Raise={((ai.bal * ai_bet[int(score)])//(0.5 * blind))*(0.5*blind)}"
        if ai.bal >= blind + (bet - ai.bet):
            return f"Raise={blind}"
        return f"Raise={ai.bal - (bet - ai.bet)}"


def make_decision(ai: GamblerInfo, hand: list, table: list, bet: (int, float), blind: (int, float), agr: list, players: int, turn: int, bots: list) -> str:
    """Make decision: call, raise and fold if bet and bet or check if nothing."""
    if GameObjects.DEBUG_MODE:
        print(win_chance(hand, table, players))
    chance = win_chance(hand, table, players)
    first_chance = round(win_chance(hand, table, players)**0.4, 2)
    ai_bet = {
        1 : 0.05,
        2 : randint(5, 15)/100 ,
        3 : randint(10, 20)/100,
        4 : randint(25, 35)/100,
        5 : randint(40, 60)/100,
        6 : randint(40, 60)/100,
        7 : randint(75, 85)/100,
        8 : randint(90, 100)/100,
        9 : 1,
    }
    if turn == 0 and randint(0, 1000) <= 150:
        if any(bool(i.bluff) == True for i in bots):
            pass
        else:
            ai.bluff = True
            if GameObjects.DEBUG_MODE:
                print(f"{ai.name} wanna bluff")

    if ai.bluff and turn >= 1:
        if GameObjects.DEBUG_MODE:
            print(f"{ai.name} is bluffing")
        return bluff_turn(ai, table, bet, blind)

    ch = randint(0, 1000)
    if ai.previous_bet == bet:
        return "Call"
    if ch <= first_chance*1000:
        if bet != 0:
            ch = randint(0, 1000)
            if ch <= chance*1000:
                if ai.bal * ai_bet[int(combination(hand, table)[0])] >= bet:
                    return "Call"
                ch = randint(0, 1000)
            elif ch <= chance*1000:
                return 'Call'
            else:          
                ch = randint(0, 1000)
                if ch <= chance*1000:
                    if ai.bal * ai_bet[int(combination(hand, table)[0])] >= blind and ai.bal >= (bet - ai.bet) + ai.bal * ai_bet[int(combination(hand, table)[0])]:
                        return f"Raise={((ai.bal * ai_bet[int(combination(hand, table)[0])])//(0.5 * blind))*(0.5*blind)}" 
                    if ai.bal >= blind + (bet - ai.bet):
                        return f"Raise={blind}"
                    return f"Raise={ai.bal - (bet - ai.bet)}"
                return "Call"
            return "Call"
        else:
            ch = randint(0, 1000)
            if ch <= chance*1000:
                if ai.bal * ai_bet[int(combination(hand, table)[0])] >= blind:
                    return f"Bet={((ai.bal * ai_bet[int(combination(hand, table)[0])])//(0.5 * blind))*(blind * 0.5)}"
                elif ai.bal * 0.25 >= blind:
                    return f"Bet={blind}"
                return f"Bet={ai.bal}"
            else:
                return "Check"
    elif bet != 0:
        if ai.bluff:
            return "Call"
        return "Fold"
    else:
        return "Check"
