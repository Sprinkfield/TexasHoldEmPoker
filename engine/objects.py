from engine.engine import combination
import platform
import ctypes  # Is needed to get screen resolution (Windows)
import subprocess  # Is needed to get screen resolution (Linux)
import pygame
import random
import time


pygame.mixer.init()


class GameObjects:
    """This is one of the main classes where all useful information is stored."""
    if platform.system().lower().startswith("windows"):
        # For Windows
        user32 = ctypes.windll.user32
        SCREENSIZE = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    else:
        # For Linux
        output = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4',shell=True, stdout=subprocess.PIPE).communicate()[0]
        SCREENSIZE = tuple(map(int, output.split()[0].split(b'x')))
    
    # Constants
    DEBUG_MODE = False
    SCAN_MODE = False
    BORDER_SIZE = int(SCREENSIZE[1] / 20)
    B_HEIGHT = int(SCREENSIZE[1]*0.7)
    B_WIDTH = int(B_HEIGHT * 16 / 10) 
    MAXIMUM_FRAMES_PER_SECOND_VALUE = 60
    TOP_IN_MAIN_MENU = int(SCREENSIZE[1] / 2.8)
    FONT_SIZE = int(SCREENSIZE[1] / 18)
    FONT_DELTA = int(FONT_SIZE / 3)
    FOREGROUND_FONT_COLOUR = [200, 40, 40]
    BACKGROUND_FONT_COLOUR = [40, 40, 200]
    SQUARE_SIZE = int((B_HEIGHT - 2*BORDER_SIZE) / 8)
    BUTTON_SIZE = int(SQUARE_SIZE * 0.9)
    GAP_IN_MAIN_MENU = int(FONT_SIZE * 2)
    CARD_SIZE = (BORDER_SIZE, BORDER_SIZE*1.54)
    USER_BTN_X = int(B_WIDTH / 6)
    USER_BTN_Y = int(B_HEIGHT / 10)
    CHIPSOUND = pygame.mixer.Sound("sounds/chipsound.wav")
    FOLDSOUND = pygame.mixer.Sound("sounds/foldsound.wav")
    deck = [
        "h2", "d2", "c2", "s2", "h3", "d3", "c3", "s3", "h4", "d4", "c4", "s4", "h5", "d5", "c5", "s5", "h6", "d6", "c6", "s6", "h7", "d7", "c7", "s7", "h8", "d8", 
        "c8", "s8", "h9", "d9", "c9", "s9", "hT", "dT", "cT", "sT", "hJ", "dJ", "cJ", "sJ", "hQ", "dQ", "cQ", "sQ", "hK", "dK", "cK", "sK", "hA", "dA", "cA", "sA"
    ]
    cards_png = dict()
    for i in deck:
        cards_png[i] = pygame.transform.scale(pygame.image.load(f"images/cards/{i}.png"), (CARD_SIZE[0], CARD_SIZE[1]))
    combinations = {
        1: "High Card",
        2: "Pair",
        3: "Two Pair",
        4: "Three of a Kind",
        5: "Straight",
        6: "Flush",
        7: "Full House",
        8: "Four of a Kind",
        9: "Straight Flush",
        10: "Royal Flush"
    }


class AiObjects:
    B_WIDTH = GameObjects.B_WIDTH
    B_HEIGHT = GameObjects.B_HEIGHT
    try:
        PLAYER_ICON = pygame.image.load("images/avatars/player.png")
    except:
        PLAYER_ICON = pygame.image.load("images/avatars/player.jpg")
    HARRYK_ICON = pygame.image.load("images/avatars/harry.png")
    FREDDY_ICON = pygame.image.load("images/avatars/freddy.png")
    NEWTON_ICON = pygame.image.load("images/avatars/newton.png")
    FYODOR_ICON = pygame.image.load("images/avatars/fyodor.png")
    YEEGOR_ICON = pygame.image.load("images/avatars/egor.png")
    ais_pos = {
        0: (B_WIDTH*0.5, B_HEIGHT*0.72),
        1: (B_WIDTH*0.12, B_HEIGHT*0.5),
        2: (B_WIDTH*0.25, B_HEIGHT*0.15),
        3: (B_WIDTH*0.75, B_HEIGHT*0.15),
        4: (B_WIDTH*0.88, B_HEIGHT*0.5),
    }
    ais_data = [
        (HARRYK_ICON, "Harry"),
        (FREDDY_ICON, "Freddy"), 
        (NEWTON_ICON, "Isaac"),
        (FYODOR_ICON, "Fyodor"), 
        (YEEGOR_ICON, "Egor"),
    ]
    random.shuffle(ais_data)


class GamblerInfo:
    def __init__(self, is_player: bool, num: int, image=None, name=None,
                 hand=None, card_shown=False, is_dealer=False, bet=0, 
                 current_move=False, move_made=False, fold=False, score=None, 
                 bal=1000, previous_bet=0, bankrupt=False, start_bal=1000, 
                 hglght_win=False, potential_take=0, win_gain=0, comb_suit=None, 
                 bluff=False, high_card=None, small_blind=False, big_blind=False,
                 curr_state=None) -> None:
        if is_player:
            pass
        elif random.randint(1, 100) == 1:
            image = AiObjects.JAAMES_ICON
            name = "James"
            bal = 10000
        else:
            new_person = AiObjects.ais_data.pop()
            AiObjects.ais_data.insert(0, new_person)
            image = new_person[0]
            name = new_person[1]
        self.x_size = int(GameObjects.B_WIDTH / 4.2)
        self.y_size = int(GameObjects.B_HEIGHT / 6.2)
        self.is_player = is_player
        self.num = num
        self.x_pos = AiObjects.ais_pos[num][0]
        self.y_pos = AiObjects.ais_pos[num][1]
        self.image = pygame.transform.scale(image, (self.y_size*0.75, self.y_size*0.75))
        self.bal = bal
        self.name = name
        self.hand = hand
        self.card_shown = card_shown
        self.is_dealer = is_dealer
        self.bet = bet
        self.current_move = current_move
        self.move_made = move_made
        self.fold = fold
        self.score = score
        self.previous_bet = previous_bet
        self.bankrupt = bankrupt
        self.start_bal = start_bal
        self.hglght_win = hglght_win
        self.potential_take = potential_take
        self.win_gain = win_gain
        self.comb_suit = comb_suit
        self.bluff = bluff
        self.high_card = high_card
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.curr_state = curr_state
        self.box = pygame.Rect(self.x_pos - self.x_size//2, self.y_pos, self.x_size, self.y_size)

    def do_fold(self) -> None:
        GameObjects.FOLDSOUND.play()
        if GameObjects.DEBUG_MODE:
            print(f"{self.name} has Folded!\n---------------------------------------------------")
        time.sleep(0.3)
        self.fold = True
        self.move_made = True

    def add_bet(self, cash: int, bank: int, max_bet: int, turn: int, phase: int, players: list, table: list, smbd_raised: bool) -> (int, int):
        GameObjects.CHIPSOUND.play()
        self.bet = cash
        if GameObjects.DEBUG_MODE:
            self.print_debug_info(turn, phase, players, table, smbd_raised)
            time.sleep(0.2)
        else:
            time.sleep(0.3)
        if self.curr_state != "All in":
            self.bal -= self.bet - self.previous_bet
            bank += self.bet - self.previous_bet
            self.previous_bet = self.bet
            max_bet = max(max_bet, self.bet)
        else:
            self.bal -= self.bet
            bank += self.bet
            self.previous_bet = self.bet
            max_bet = max(max_bet, self.bet)
        self.move_made = True

        return bank, max_bet
    
    def set_blind(self, blind: int) -> None:
        cash = min(blind, self.bal)
        self.bet = cash
        self.previous_bet = cash
        self.bal -= cash

    def new_round_setup(self) -> None:
        self.high_card = None
        self.bluff = False
        self.win_gain = 0
        self.hglght_win = False
        self.bankrupt = False
        self.potential_take = 0
        self.start_bal = self.bal
        self.fold = False
        self.move_made = False
        self.card_shown = True if self.is_player or (GameObjects.DEBUG_MODE and GameObjects.SCAN_MODE) else False

    def execute_folded(self) -> None:
        self.current_move = False
        self.move_made = True
        self.potential_take = 0
        self.bet = 0
        self.previous_bet = 0

    def print_debug_info(self, turn, phase, players, table, smbd_raised) -> None:
        print(f"Turn: {turn}, Phase: {phase};")
        if self.is_player:
            if self.fold:
                print(f"{self.name} has Folded!")
            elif self.bet == max([k.bet for k in players]) != 0:
                print(f"{self.name} has Called {self.bet}!")
            elif smbd_raised:
                print(f"{self.name} has Raised {self.bet}!")
            else:
                print(f"{self.name} has Checked!")
        print(f"{self.name} has made move! curr_bet: {self.bet}; prev_bet: {self.previous_bet};")
        print(f"{self.name}'s cards are: {self.hand[0]} {self.hand[1]}")
        print(f"{self.name}'s combination: {combination(self.hand, table)[0]} ({GameObjects.combinations[int(combination(self.hand, table)[0])]})")
        print("---------------------------------------------------")


def get_config() -> dict:
    data_dict = dict()
    with open("user_config.txt", "r") as file:
        data = file.read().split()
        data = [line.split("=") for line in data]

    for key, value in data:
        try:
            value = int(value)
        except:
            value = str(value)
        data_dict[key] = value

    return data_dict


def write_config(new_data: dict) -> None:
    data = []
    for key, value in new_data.items():
        data.append(f"{key}={value}")

    with open("user_config.txt", "w") as file:
        file.write("\n".join(data) + "\n")
