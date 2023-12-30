"""This file contains combination-calculating functions."""


def sf_n_f(suit: int, hand: list, table: list, score: float) -> float:
    """Straight Flush and Flush calculating."""
    ttable = [i for i in table]
    win_suit = None
    for i in hand:
        ttable.append(i)
    if len(ttable) >= 5:
        l = []
        for i in ttable:
            if i[1] == suit:  # 1-spades 2-clubs 3-diamonds 4-hearts.
                l.append(i[0])
                l = sorted(l)
        if len(l) == 7:
            if l[0] + 4 == l[1] + 3 == l[2] + 2 == l[3] + 1 == l[4]:
                score = max(9 + l[4]/100 + l[3]/10000 + l[2]/1000000 + l[1]/100000000 + l[0]/10000000000, score)
            if l[1] + 4 == l[2] + 3 == l[3] + 2 == l[4] + 1 == l[5]:
                score = max(9 + l[5]/100 + l[4]/10000 + l[3]/1000000 + l[2]/100000000 + l[1]/10000000000, score)
            if l[2] + 4 == l[3] + 3 == l[4] + 2 == l[5] + 1 == l[6]:
                score = max(9 + l[6]/100 + l[5]/10000 + l[4]/1000000 + l[3]/100000000 + l[2]/10000000000, score)
            else:
                score = max(6 + l[6]/100 + l[5]/10000 + l[4]/1000000 + l[3]/100000000 + l[2]/10000000000, score)
        elif len(l) == 6:
            if l[0] + 4 == l[1] + 3 == l[2] + 2 == l[3] + 1 == l[4]:
                score = max(9 + l[4]/100 + l[3]/10000 + l[2]/1000000 + l[1]/100000000 + l[0]/10000000000, score)
            if l[1] + 4 == l[2] + 3 == l[3] + 2 == l[4] + 1 == l[5]:
                score = max(9 + l[5]/100 + l[4]/10000 + l[3]/1000000 + l[2]/100000000 + l[1]/10000000000, score)
            else:
                score = max(6 + l[5]/100 + l[4]/10000 + l[3]/1000000 + l[2]/100000000 + l[1]/10000000000, score)
        elif len(l) == 5:
            if l[0] + 4 == l[1] + 3 == l[2] + 2 == l[3] + 1 == l[4]:
                score = max(9 + l[4]/100 + l[3]/10000 + l[2]/1000000 + l[1]/100000000 + l[0]/10000000000, score)
            else:
                score = max(6 + l[4]/100 + l[3]/10000 + l[2]/1000000 + l[1]/100000000 + l[0]/10000000000, score)
    if int(score) in [6, 9]:
        for j in range(1, 5):
            if len(list(filter(lambda x: x[1] == j, ttable))) >= 5:
                win_suit = j
                break
    return score, win_suit


def smth_of_kind(hand: list, table: list, score: float) -> float:
    """Calculating Pair, Two Pair, Set, Full House and Carre."""
    ttable = [i for i in table]
    t = -1
    l = []
    k = []
    for i in hand:
        ttable.append(i)
    ttable = sorted(ttable)
    for i in range(0, len(ttable)-1):  # Find repeated cards.
        if ttable[i][0] == ttable[i+1][0]:
            for j in range(i, len(ttable)):
                if ttable[i][0] == ttable[j][0] and ttable[j] not in l:
                    l.append(ttable[j])
                    t += 1
                else:
                    t = 0
                    break
    kk = []
    for i in l:
        kk.append(i[0])
    for i in list(set([int(i[0]) for i in l])):
        k.append(kk.count(i))
    ttable = sorted(ttable)
    if len(k) == 3 and k[0] == k[1] == k[2] == 2:  # Delete trash Pair.
        del l[0]
        del l[0]
        del k[0]  # Trash Pair has been deleted.
    if len(k) == 3 and k[0] == 3:  # Delete trash Pair.
        del l[3]
        del l[3]
        del k[1]  # Trash Pair has been deleted
    elif len(k) == 3 and (k[1] == 3 or k[2] == 3):  # Delete trash Pair.
        del l[0]
        del l[0]
        del k[0]  # Trash Pair has been deleted.
    for i in l:
        del ttable[ttable.index(i)] 
    ln = len(ttable) - 1
    if len(k) == 1:  # Pair, Set and Carre calculating.
        if k[0] == 2:
            score = max(score, 2 + l[0][0] / 100 + l[1][0] / 10000 + ttable[ln][0] / 1000000 + ttable[ln-1][0]/100000000 + ttable[ln-2][0]/10000000000)
        elif k[0] == 3:
            score = max(score, 4 + l[0][0] / 100 + l[1][0] / 10000 + l[2][0] / 1000000 + ttable[ln][0]/100000000 + ttable[ln-1][0]/10000000000)
        elif k[0] == 4:
            score = max(score, 8 + l[0][0] / 100 + l[1][0] / 10000 + l[2][0] / 1000000 + l[3][0]/100000000 + ttable[ln][0]/10000000000)
    elif len(k) == 2:  # Two Pair and Full House calculating.
        if k[0] == k[1] == 2:
            score = max(score, 3 + l[3][0] / 100 + l[2][0] / 10000 + l[1][0] / 1000000 + l[0][0]/100000000 + ttable[ln][0]/10000000000)
        elif k[0] == 3 and k[1] == 2:
            score = max(score, 7 + l[2][0] / 100 + l[1][0] / 10000 + l[0][0] / 1000000 + l[4][0]/100000000 + l[3][0]/10000000000)
        elif k[0] == 2 and k[1] == 3:
            score = max(score, 7 + l[4][0] / 100 + l[3][0] / 10000 + l[2][0] / 1000000 + l[1][0]/100000000 + l[0][0]/10000000000)
    return score


def straight(hand: list, table: list, score: float) -> float:
    """Calculating Straight."""
    ttable = [i[0] for i in table]
    for i in hand:
        ttable.append(i[0])
    ttable = sorted(ttable)
    ttable = list(set(ttable))
    if 14 in ttable:
        if len(ttable) == 7:
            if ttable[0] + 4 == ttable[1] + 3 == ttable[2] + 2 == ttable[3] + 1 == ttable[4]:
                score = max(5 + ttable[4]/100 + ttable[3]/10000 + ttable[2]/1000000 + ttable[1]/100000000 + ttable[0]/10000000000, score)
            if ttable[1] + 4 == ttable[2] + 3 == ttable[3] + 2 == ttable[4] + 1 == ttable[5]:
                score = max(5 + ttable[5]/100 + ttable[4]/10000 + ttable[3]/1000000 + ttable[2]/100000000 + ttable[1]/10000000000, score)
            if ttable[2] + 4 == ttable[3] + 3 == ttable[4] + 2 == ttable[5] + 1 == ttable[6]:
                score = max(5 + ttable[6]/100 + ttable[5]/10000 + ttable[4]/1000000 + ttable[3]/100000000 + ttable[2]/10000000000, score)
        elif len(ttable) == 6:
            if ttable[0] + 4 == ttable[1] + 3 == ttable[2] + 2 == ttable[3] + 1 == ttable[4]:
                score = max(5 + ttable[4]/100 + ttable[3]/10000 + ttable[2]/1000000 + ttable[1]/100000000 + ttable[0]/10000000000, score)
            if ttable[1] + 4 == ttable[2] + 3 == ttable[3] + 2 == ttable[4] + 1 == ttable[5]:
                score = max(5 + ttable[5]/100 + ttable[4]/10000 + ttable[3]/1000000 + ttable[2]/100000000 + ttable[1]/10000000000, score)
        elif len(ttable) == 5:
            if ttable[0] + 4 == ttable[1] + 3 == ttable[2] + 2 == ttable[3] + 1 == ttable[4]:
                score = max(5 + ttable[4]/100 + ttable[3]/10000 + ttable[2]/1000000 + ttable[1]/100000000 + ttable[0]/10000000000, score)
        
        # Check Straight with Ace = 1.
        for i in range(0, len(ttable)):
            if ttable[i] == 14:
                ttable[i] = 1
        ttable = sorted(ttable)

        if len(ttable) == 7:
            if ttable[0] + 4 == ttable[1] + 3 == ttable[2] + 2 == ttable[3] + 1 == ttable[4]:
                score = max(5 + ttable[4]/100 + ttable[3]/10000 + ttable[2]/1000000 + ttable[1]/100000000 + ttable[0]/10000000000, score)
            if ttable[1] + 4 == ttable[2] + 3 == ttable[3] + 2 == ttable[4] + 1 == ttable[5]:
                score = max(5 + ttable[5]/100 + ttable[4]/10000 + ttable[3]/1000000 + ttable[2]/100000000 + ttable[1]/10000000000, score)
            if ttable[2] + 4 == ttable[3] + 3 == ttable[4] + 2 == ttable[5] + 1 == ttable[6]:
                score = max(5 + ttable[6]/100 + ttable[5]/10000 + ttable[4]/1000000 + ttable[3]/100000000 + ttable[2]/10000000000, score)
        elif len(ttable) == 6:
            if ttable[0] + 4 == ttable[1] + 3 == ttable[2] + 2 == ttable[3] + 1 == ttable[4]:
                score = max(5 + ttable[4]/100 + ttable[3]/10000 + ttable[2]/1000000 + ttable[1]/100000000 + ttable[0]/10000000000, score)
            if ttable[1] + 4 == ttable[2] + 3 == ttable[3] + 2 == ttable[4] + 1 == ttable[5]:
                score = max(5 + ttable[5]/100 + ttable[4]/10000 + ttable[3]/1000000 + ttable[2]/100000000 + ttable[1]/10000000000, score)
        elif len(ttable) == 5:
            if ttable[0] + 4 == ttable[1] + 3 == ttable[2] + 2 == ttable[3] + 1 == ttable[4]:
                score = max(5 + ttable[4]/100 + ttable[3]/10000 + ttable[2]/1000000 + ttable[1]/100000000 + ttable[0]/10000000000, score) 
    return score


def higher_card5(hand: list, table: list, score: float) -> float:
    """Calculating higher card for >= 5 cards."""
    ttable = [i for i in table]
    for i in hand:
        ttable.append(i)
    ttable = sorted(ttable)
    ln = len(ttable) - 1
    score = max(1 + ttable[ln][0]/100 + ttable[ln-1][0]/10000 + ttable[ln-2][0]/1000000 + ttable[ln-3][0]/100000000 + ttable[ln-4][0]/10000000000, score)
    return score


def only_hand(hand: list, score: float) -> float:
    """Calculating best combination with no table."""
    if hand[0][0] == hand[1][0]:
        score = max(score, 2 + hand[0][0]/100 + hand[0][0]/10000)
    else:
        score = max(score, 1 + max(hand[0][0], hand[1][0])/100 + min(hand[0][0], hand[1][0])/10000)
    return score


def translate(data: list) -> dict:
    """Convert backend of the frontend to backend of engine 0_0."""
    encriptor1 = {"s": 1, "c": 2, "d": 3, "h": 4}
    encriptor2 = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}

    if data[1] in "23456789":
        data = [int(data[1]), int(encriptor1[data[0]])]
    else:
        data = [int(encriptor2[data[1]]), int(encriptor1[data[0]])]

    return data


def combination(hand: list, table: list) -> (float, str):
    """Calculating the best player's combination using backend of frontend deck type."""
    cards_symbols = {None: None, 1: "♠", 2: "♣", 3: "♦", 4: "♥"}
    hand = [translate(i) for i in hand] if hand != None else []
    table = [translate(i) for i in table] if table != None else []
    score = 0.0
    suit = None
    if len(hand) + len(table) >= 3:
        for i in range(1, 5):
            yes_or_no = sf_n_f(i, hand, table, score)
            score, suit = max(score, yes_or_no[0]), yes_or_no[1]  # 6,9
        score = max(score, smth_of_kind(hand, table, score))      # 2, 3, 4, 7, 8.
        score = max(score, straight(hand, table, score))          # 5
        score = max(score, higher_card5(hand, table, score))      # 1
    else:
        score = only_hand(hand, score)  # 1, 2 for only hand.
    return round(score, 10), cards_symbols[suit]


def combination_Egor(hand: list, table: list) -> float:
    score = 0.0
    if len(hand) + len(table) >= 5:
        for i in range(1, 5):
            score = max(score, sf_n_f(i, hand, table, score)[0])  # 6,9
        score = max(score, straight(hand, table, score))          # 5
        score = max(score, smth_of_kind(hand, table, score))      # 2, 3, 4, 7, 8
        score = max(score, higher_card5(hand, table, score))      # 1
    else:
        score = only_hand(hand, score)  # 1, 2 for only hand.
    return round(score, 10)
