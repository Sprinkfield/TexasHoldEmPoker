from engine.objects import GamblerInfo
from engine.engine import combination
from random import randint
import numpy as np


def sigmoid(x):
    # Activation function sigmoid: f(x) = 1 / (1 + e^(-x))
    return 1 / (1 + np.exp(-x))


def deriv_sigmoid(x):
    # Derivative of sigmoid: f'(x) = f(x) * (1 - f(x))
    fx = sigmoid(x)
    return fx * (1 - fx)


def mse_loss(y_true, y_pred):
    # y_true and y_pred are empty arrays of the same length
    return ((y_true - y_pred) ** 2).mean()


class NeuralNetwork:
    def __init__(self): # 0.9330787273868613 -0.6808345302048712 1.3400511200580396 -1.0773637854465972 3.6307840902860473 2.0300002771139045 1.7989613097388633 -3.7777878890656615 -2.1525974905342657
        self.w1 = 0.9330787273868613
        self.w2 = -0.6808345302048712
        self.w3 = 1.3400511200580396
        self.w4 = -1.0773637854465972
        self.w5 = 3.6307840902860473
        self.w6 = 2.0300002771139045

        # Offsets
        self.b1 = 1.7989613097388633
        self.b2 = -3.7777878890656615
        self.b3 = -2.1525974905342657

    def feedforward(self, x):
        # x is a numpy array with two elements
        h1 = sigmoid(self.w1 * x[0] + self.w2 * x[1] + self.b1)
        h2 = sigmoid(self.w3 * x[0] + self.w4 * x[1] + self.b2)
        o1 = sigmoid(self.w5 * h1 + self.w6 * h2 + self.b3)
        return o1


def hand_quality(hand, table, agr, randomness):
    """Calculating quality of combination with neural network."""
    data = np.array([
    [1.1009080604, 7],
    [3.1010080811, 7],
    [4.0909091208, 7],
    [1.1009080604, 2],
    [9.1413121110, 7],
    [9.1413121110, 5],
    [7.1010100909, 7],
    [5.1211100908, 5],
    [4.1010100906, 6]
    ])
    all_y_trues = np.array([
        0.15**(1/agr), 
        0.40**(1/agr), 
        0.6**(1/agr), 
        0.70**(1/agr),
        0.95**(1/agr),
        1.0**(1/agr),
        0.85**(1/agr),
        0.8**(1/agr),
        0.7**(1/agr)
    ])
    score = combination(hand, table)[0]
    cards = len(table) + len(hand)
    x = np.array([score, cards])
    x = network.feedforward(x)
    x = (x / (randomness**(0.5/x)))
    return round(x, 3)


def make_decision(ai: GamblerInfo, hand, table, bet, blind, agr, empty1=None, empty2=None, empty3=None) -> str:
    """Make decision: call, raise and fold if bet and bet or check if nothing."""
    randomness = 1
    agr_ai = agr[ai.num - 1]
    Raise_chance = hand_quality(hand, table, agr_ai, randomness)
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

    if bet != 0:
        ch = randint(0, 1000)

        if ch <= Raise_chance*1000:
            if ai.bal * ai_bet[int(combination(hand, table)[0])] >= bet:
                return "Call"
            ch = randint(0, 1000)

            if ch <= Raise_chance*1000:
                return "Call"
            return "Fold"
        ch = randint(0, 1000)

        if ch <= Raise_chance*1000:
            if ai.bal * ai_bet[int(combination(hand, table)[0])] >= blind and ai.bal >= bet + ai.bal * ai_bet[int(combination(hand, table)[0])]:
                return f"Raise={ai.bal * ai_bet[int(combination(hand, table)[0])]}"
            
            if ai.bal >= blind + bet:
                return f"Raise={blind}"
            ch = randint(0, 1000)

            if ch <= Raise_chance*1000 and ai.bal > bet:
                return f"Raise={ai.bal - bet}"
        return "Call"
    else:
        ch = randint(0, 1000)
        if ch <= Raise_chance*1000:
            if ai.bal * ai_bet[int(combination(hand, table)[0])] >= blind:
                return f"Bet={ai.bal * ai_bet[int(combination(hand, table)[0])]}"
            return f"Bet={ai.bal}"
        else:
            return "Check"


network = NeuralNetwork()
