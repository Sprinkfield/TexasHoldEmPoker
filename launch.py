"""Execute this file to run the program."""
from engine.objects import GameObjects, AiObjects, GamblerInfo, get_config, write_config
from engine.gui import GUI
from engine.ai_alpha import make_decision
from engine.engine import combination
import pygame
import random
import time


TOP_IN_MAIN_MENU = GameObjects.TOP_IN_MAIN_MENU
DEBUG_MODE = GameObjects.DEBUG_MODE
FONT_SIZE = GameObjects.FONT_SIZE
FONT_DELTA = GameObjects.FONT_DELTA
GAP_IN_MAIN_MENU = GameObjects.GAP_IN_MAIN_MENU
LETTER_BORDER_SIZE = int(GameObjects.SCREENSIZE[1] / 36)
B_WIDTH = GameObjects.B_WIDTH
B_HEIGHT = GameObjects.B_HEIGHT
USER_BTN_X = GameObjects.USER_BTN_X
USER_BTN_Y = GameObjects.USER_BTN_Y
BORDER_SIZE = GameObjects.BORDER_SIZE
BACKGROUND_FONT_COLOUR = GameObjects.BACKGROUND_FONT_COLOUR
FOREGROUND_FONT_COLOUR = GameObjects.FOREGROUND_FONT_COLOUR
MAXIMUM_FRAMES_PER_SECOND_VALUE = GameObjects.MAXIMUM_FRAMES_PER_SECOND_VALUE
B_B_WIDTH = GameObjects.SCREENSIZE[1] * 2
SQUARE_SIZE = GameObjects.SQUARE_SIZE
GAME_ICON = pygame.image.load("images/icon.ico")
blinds_dict = {0: 20, 1: 40, 2: 60, 3: 100, 4: 200, 5: 400, 6: 800, 7: 1600}
agr = [1, 1, 1, 1]
random.shuffle(agr)
[print("============== DEBUG MODE IS ACTIVE! ==============") if DEBUG_MODE else None]


def ai_move(gam, table, max_bet, blind, players, phase, start_players) -> (bool, int):
    result = make_decision(gam, gam.hand, table, max_bet, blind, agr, len(players), phase, start_players)

    if DEBUG_MODE:
        print(result)

    round_bet = lambda x: (x - (x % blind)) if (gam.bal > blind) else (gam.bal)

    if result == "Fold":
        gam.do_fold()
        gam.curr_state = "Fold"
        return (False, 0)
    elif result in ["Check", "Call"] or max_bet >= gam.bal:
        gam.curr_state = "Call"
        return (False, min(max_bet, gam.bal))
    elif result.startswith("Bet="):
        gam.curr_state = "Bet"
        move = round_bet(int(round(float(result[4:]))))
        move = min(move, gam.bal)
        if any([move <= b.start_bal for b in players if b != gam]):
            return (True, move)
        else:
            return (True, min([b.start_bal for b in players]))
    elif result.startswith("Raise="):
        gam.curr_state = "Raise"
        move = round_bet(int(round(float(result[6:]))))
        move = min(move, gam.bal)
        if all([(max_bet + move) <= (b.bal + b.bet) for b in players]):
            return (True, min(gam.bal, max_bet + move))
        else:
            return (True, min(gam.bal, max([(b.bal + b.bet) for b in players if b != gam])))
    else:
        print("Help! I don't know what to do! :((((")
        return (False, gam.bal)


def run_game() -> None:
    pygame.init()
    pygame.font.init()
    pygame.display.set_icon(GAME_ICON)
    pygame.display.set_caption("Poker Offline")

    game_screen = pygame.display.set_mode((B_WIDTH, B_HEIGHT))
    game_timer = pygame.time.Clock()
    input_box = pygame.Rect(B_WIDTH*0.56, TOP_IN_MAIN_MENU, B_WIDTH//3, FONT_SIZE)
    in_main_menu_or_settings = True
    game_running_state = True
    selected_button = None
    in_main_menu = True

    skip_flag = False
    smbd_raised = False
    active = False
    new_round = True

    blind = blinds_dict[0]
    turn = 0
    phase = 0
    bank = 0
    table = []
    max_bet = blind

    new_data = get_config()
    gam_amount = new_data["gam_amount"]
    username = new_data["username"]
    player_bal = new_data["player_bal"]

    while in_main_menu_or_settings:
        if in_main_menu:
            for single_event in pygame.event.get():
                if single_event.type == pygame.QUIT:
                    game_running_state = False
                    in_main_menu_or_settings = False
                # Mouse movement processing.
                elif single_event.type == pygame.MOUSEBUTTONDOWN:
                    location = pygame.mouse.get_pos()
                    if BORDER_SIZE < location[1] < B_HEIGHT and B_WIDTH//3 < location[0] < B_WIDTH//3*2:
                        if TOP_IN_MAIN_MENU - GAP_IN_MAIN_MENU <= location[1] <= TOP_IN_MAIN_MENU - GAP_IN_MAIN_MENU + FONT_SIZE:
                            in_main_menu_or_settings = False
                        elif TOP_IN_MAIN_MENU <= location[1] <= TOP_IN_MAIN_MENU + FONT_SIZE:
                            in_main_menu = False
                        elif TOP_IN_MAIN_MENU + GAP_IN_MAIN_MENU <= location[1] <= TOP_IN_MAIN_MENU + GAP_IN_MAIN_MENU + FONT_SIZE:
                            game_running_state = False
                            in_main_menu_or_settings = False

            GUI().draw_main_menu(game_screen, selected_button, player_bal)
            game_timer.tick(MAXIMUM_FRAMES_PER_SECOND_VALUE)

            # Highlighting the chosen button in main menu.
            location = pygame.mouse.get_pos()

            if TOP_IN_MAIN_MENU - GAP_IN_MAIN_MENU <= location[1] <= TOP_IN_MAIN_MENU + GAP_IN_MAIN_MENU + FONT_SIZE and B_WIDTH//3 < location[0] < B_WIDTH//3*2:
                if TOP_IN_MAIN_MENU - GAP_IN_MAIN_MENU <= location[1] <= TOP_IN_MAIN_MENU - GAP_IN_MAIN_MENU + FONT_SIZE:
                    selected_button = 0
                elif TOP_IN_MAIN_MENU <= location[1] <= TOP_IN_MAIN_MENU + FONT_SIZE:
                    selected_button = 1
                elif TOP_IN_MAIN_MENU + GAP_IN_MAIN_MENU <= location[1] <= TOP_IN_MAIN_MENU + GAP_IN_MAIN_MENU + FONT_SIZE:
                    selected_button = 2
            else:
                selected_button = None

            pygame.display.flip()
        else:  # Settings Menu.
            for single_event in pygame.event.get():
                if single_event.type == pygame.QUIT:
                    game_running_state = False
                    in_main_menu_or_settings = False
                # Mouse movement processing.
                elif single_event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(single_event.pos):
                        active = not active
                    else:
                        active = False
                    location = pygame.mouse.get_pos()
                    if BORDER_SIZE < location[1] < B_HEIGHT:
                        if TOP_IN_MAIN_MENU - GAP_IN_MAIN_MENU <= location[1] <= TOP_IN_MAIN_MENU - GAP_IN_MAIN_MENU + FONT_SIZE:
                            gam_amount = max((gam_amount + 1) % 6, 2)
                        elif TOP_IN_MAIN_MENU <= location[1] <= TOP_IN_MAIN_MENU + FONT_SIZE:
                            pass
                        elif TOP_IN_MAIN_MENU + GAP_IN_MAIN_MENU <= location[1] <= TOP_IN_MAIN_MENU + GAP_IN_MAIN_MENU + FONT_SIZE:
                            in_main_menu = True
                elif single_event.type == pygame.KEYDOWN:
                    if active:
                        if single_event.key == pygame.K_RETURN:
                            active = not active
                        elif single_event.key == pygame.K_BACKSPACE:
                            username = username[:-1]
                        else:
                            username += single_event.unicode

            # Settings menu render.
            GUI().draw_settings_menu(game_screen, selected_button, gam_amount)
            game_timer.tick(MAXIMUM_FRAMES_PER_SECOND_VALUE)

            # Highlighting the chosen button in settings menu.
            location = pygame.mouse.get_pos()

            if TOP_IN_MAIN_MENU - GAP_IN_MAIN_MENU <= location[1] <= TOP_IN_MAIN_MENU - GAP_IN_MAIN_MENU + FONT_SIZE:
                selected_button = 0
            elif TOP_IN_MAIN_MENU <= location[1] <= TOP_IN_MAIN_MENU + FONT_SIZE:
                selected_button = 1
            elif TOP_IN_MAIN_MENU + GAP_IN_MAIN_MENU <= location[1] <= TOP_IN_MAIN_MENU + GAP_IN_MAIN_MENU + FONT_SIZE:
                selected_button = 2
            else:
                selected_button = None

            font = pygame.font.SysFont("Arial", FONT_SIZE, True, False)
            txt_surface = font.render(username, True, BACKGROUND_FONT_COLOUR)
            game_screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
            txt_surface = font.render(username, True, pygame.Color(list(map(lambda x: x + 55, FOREGROUND_FONT_COLOUR)) if active or selected_button == 1 else FOREGROUND_FONT_COLOUR))
            game_screen.blit(txt_surface, (input_box.x+7, input_box.y+7))
            pygame.display.flip()

    new_data["gam_amount"] = gam_amount
    new_data["username"] = username
    new_data["player_bal"] = player_bal
    write_config(new_data)

    user = GamblerInfo(True, 0, AiObjects.PLAYER_ICON, username, AiObjects.ais_pos[0][0], AiObjects.ais_pos[0][1])
    start_players = [user]
    players = [i for i in start_players]
    dealer_num = random.randint(0, len(players) - 1)
    current_num = (dealer_num+3) % len(players)
    for n in range(1, gam_amount):
        start_players.append(GamblerInfo(False, n))

    ### Game Itself ###
    while game_running_state:
        if len(start_players) <= 1:
            # End of the game
            GUI().draw_endgame_stuff(game_screen)
            for single_event in pygame.event.get():
                if single_event.type in [pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN]:
                    game_running_state = False
                    run_game()
            continue

        if new_round:
            if DEBUG_MODE:
                print(f"Turn is {turn + 1}")

            new_round = False
            blind = blinds_dict[min(turn // 5, 7)]
            max_bet = blind
            bet_mulpiplier = 1
            black_list = []
            temp_len_sp = len(start_players)

            for gambler in start_players:
                if gambler.bal <= 0 or gambler.bankrupt:
                    black_list.append(gambler)
                else:
                    gambler.new_round_setup()

            for b_gambl in black_list:
                del start_players[start_players.index(b_gambl)]

            if len(start_players) <= 1:
                continue  # End game.
            else:
                players = [i for i in start_players]  # Copying list.

            for er in players:
                er.fold = False
                er.is_dealer = False
                er.small_blind = False
                er.big_blind = False
                er.curr_state = None

            # Dealer change.
            delta_players = temp_len_sp - len(start_players)
            dealer_num = (dealer_num + 1 - delta_players) % len(players)
            players[dealer_num].is_dealer = True
            current_num = current_num % len(players)

            # Blinds.
            players[(dealer_num+1) % len(players)].set_blind(blind//2)
            players[(dealer_num+1) % len(players)].small_blind = True
            players[(dealer_num+1) % len(players)].curr_state = "Bet"
            
            players[(dealer_num+2) % len(players)].set_blind(blind)
            players[(dealer_num+2) % len(players)].big_blind = True
            players[(dealer_num+2) % len(players)].curr_state = "Bet"

            bank += players[(dealer_num+1) % len(players)].bet + players[(dealer_num+2) % len(players)].bet
            current_num = (dealer_num+3) % len(players)

            # Hands giveaway.
            table = []
            deck = [
                "h2", "d2", "c2", "s2", "h3", "d3", "c3", "s3", "h4", "d4", "c4", "s4", "h5", 
                "d5", "c5", "s5", "h6", "d6", "c6", "s6", "h7", "d7", "c7", "s7", "h8", "d8", 
                "c8", "s8", "h9", "d9", "c9", "s9", "hT", "dT", "cT", "sT", "hJ", "dJ", "cJ", 
                "sJ", "hQ", "dQ", "cQ", "sQ", "hK", "dK", "cK", "sK", "hA", "dA", "cA", "sA"
            ]
            random.shuffle(deck)

            for gambler in players:
                gambler.hand = [deck.pop(), deck.pop()]
                g_result = combination(gambler.hand, table)
                gambler.score = g_result[0]
                gambler.comb_suit = g_result[1]

        for single_event in pygame.event.get():
            if single_event.type == pygame.QUIT:
                game_running_state = False  # Exit the game.
            elif not players[0].fold and players[0].is_player and players[0].current_move and not any(gmb.hglght_win for gmb in start_players):
                if single_event.type == pygame.MOUSEBUTTONDOWN:
                    location = pygame.mouse.get_pos()
                    if B_HEIGHT - USER_BTN_Y <= location[1] <= B_HEIGHT:
                        GUI().draw_game_manip(game_screen, table, players[0], blind, start_players, max_bet, bank, bet_mulpiplier, len(players) <= 1, turn, smbd_raised)
                        if B_WIDTH//2 - USER_BTN_X*1.55 <= location[0] <= B_WIDTH//2 - USER_BTN_X*1.55 + USER_BTN_X:   # Fold.
                            players[0].do_fold()
                            players[0].curr_state = "Fold"
                        elif B_WIDTH//2 - USER_BTN_X*0.5 <= location[0] <= B_WIDTH//2 - USER_BTN_X*0.5 + USER_BTN_X:   # Call.
                            bank, max_bet = players[0].add_bet(min(max_bet, players[0].bal), bank, max_bet, turn, phase, players, table, smbd_raised)
                            players[0].curr_state = "Call"
                            current_num = (current_num + 1) % len(players)
                        elif B_WIDTH//2 + USER_BTN_X*0.55 <= location[0] <= B_WIDTH//2 + USER_BTN_X*0.74 + USER_BTN_X: # Raise.
                            smbd_raised = True
                            if max_bet == 0:
                                players[0].curr_state = "Bet"
                            else:
                                players[0].curr_state = "Raise"
                            bank, max_bet = players[0].add_bet(min(max_bet + blind*bet_mulpiplier, players[0].bal), bank, max_bet, turn, phase, players, table, smbd_raised)
                            current_num = (current_num + 1) % len(players)
                        elif B_WIDTH//2 + USER_BTN_X*1.8 <= location[0] <= B_WIDTH//2 + USER_BTN_X*1.8 + USER_BTN_Y:   # Increase stake.
                            bet_mulpiplier += 1 if players[0].bal >= max_bet + blind*(bet_mulpiplier + 1) else 0
                        elif B_WIDTH//2 + USER_BTN_X*2.2 <= location[0] <= B_WIDTH//2 + USER_BTN_X*2.2 + USER_BTN_Y:   # Lower stake.
                            bet_mulpiplier -= 1 if max_bet <= max_bet + blind*(bet_mulpiplier - 2) else 0
                        elif 0 <= location[0] <= USER_BTN_Y*1.75:                                                      # All-in stake.
                            if max_bet < players[0].bal:
                                smbd_raised = True
                            players[0].curr_state = "All in"
                            bank, max_bet = players[0].add_bet(players[0].bal, bank, max_bet, turn, phase, players, table, smbd_raised)
                            current_num = (current_num + 1) % len(players)

                skip_flag = True

        for gambler in players:
            if gambler.fold:
                del players[players.index(gambler)]
                gambler.execute_folded()
                current_num = current_num % len(players)
            elif gambler.bal <= 0:
                gambler.bankrupt = True
            elif gambler == players[current_num]:
                gambler.current_move = True
            else:
                gambler.current_move = False

        if skip_flag:
            skip_flag = False
            continue

        if smbd_raised:
            smbd_raised = False
            for gambler in players:
                gambler.move_made = False
            players[current_num - 1].move_made = True
            continue

        GUI().draw_game_manip(game_screen, table, players[0], blind, start_players, max_bet, bank, bet_mulpiplier, len(players) <= 1, turn)
        
        if all([g.move_made for g in players]):  # Next phase.
            if DEBUG_MODE:
                print("| Next phase! |\n===============")

            for gambler in players:
                gambler.curr_state = None
                gambler.move_made = False
                gambler.potential_take += gambler.bet
                gambler.bet = 0
                gambler.previous_bet = 0

            phase += 1
            max_bet = 0
            bet_mulpiplier = 1

            for gmblr in start_players:
                g_result = combination(gmblr.hand, table)
                gmblr.move_made = False
                gmblr.curr_state = None
                gmblr.score = g_result[0]
                gmblr.comb_suit = g_result[1]

            if phase == 1:
                table = [deck.pop(), deck.pop(), deck.pop()]
            elif phase == 2:
                table.append(deck.pop())
            elif phase == 3:
                table.append(deck.pop())
            elif phase > 3:
                GUI().draw_game_manip(game_screen, table, players[0], blind, start_players, max_bet, bank, bet_mulpiplier, len(players) <= 1, turn, True)

                max_score = max([gmblr.score for gmblr in players if not gmblr.fold])
                winner_list = []
                winner_name = []
                # special_winners = []

                for gambler in players:
                    gambler.card_shown = True
                    if gambler.score == max_score:
                        # if gambler.potential_take * len(players) <= int(bank / len(players)) and not all([gambler.potential_take >= g.potential_take for g in players]):
                        #     special_winners.append(gambler)
                        # else:
                        winner_list.append(gambler)
                        gambler.hglght_win = True
                        gambler.bankrupt = False
                        winner_name.append(gambler.name)

                bank_temp = bank
                players = sorted(players, key=lambda x: x.score)

                # Finding high card for each one.
                if len(players) >= 2:
                    score_a = str(players[0].score)[2:]
                    score_b = str(players[-1].score)[2:]
                    for j in range(0, len(score_a), 2):
                        if score_a[j:j+2] != score_b[j:j+2]:
                            players[0].high_card = score_a[j:j+2]
                            players[-1].high_card = score_b[j:j+2]
                            break
                for i in range(len(players) - 1):
                    score_a = str(players[i].score)[2:]
                    score_b = str(players[i+1].score)[2:]
                    for j in range(0, len(score_a), 2):
                        if score_a[j:j+2] != score_b[j:j+2]:
                            players[i].high_card = score_a[j:j+2]
                            players[i+1].high_card = score_b[j:j+2]
                            break

                # for man_gam in special_winners:
                #     bank -= man_gam.potential_take * len(players)
                #     man_gam.bal += man_gam.potential_take * len(players)
                #     man_gam.win_gain = man_gam.potential_take * len(players)
                for gam_win in winner_list:
                    if DEBUG_MODE:
                        print(f"= = = = = = = =\n{gam_win.name} wins!\n= = = = = = = =\n")
                    gam_win.bal += int(bank / len(winner_list))
                    gam_win.win_gain = int(bank / len(winner_list))

                bank = bank_temp

                GUI().draw_game_manip(game_screen, table, players[0], blind, start_players, max_bet, bank, bet_mulpiplier, len(players) <= 1, turn, True)

                # * Showing the winners.
                font_type = pygame.font.SysFont("Arial", int(FONT_SIZE*0.7), True, False)
                wintext = f"{', '.join(winner_name)} win!" if len(winner_list) > 1 else f"{winner_name[0]} wins!"
                text_object = font_type.render(wintext, False, pygame.Color(100, 100, 100))
                text_location = pygame.Rect(B_WIDTH//2, B_HEIGHT*0.02, B_WIDTH, 100).move(-text_object.get_width()/2, 0)
                game_screen.blit(text_object, text_location)
                text_object = font_type.render(wintext, False, pygame.Color(255, 255, 255))
                game_screen.blit(text_object, text_location.move(2, 2))
                pygame.display.flip()

                time.sleep(4.5)

                new_round = True
                max_bet = blind
                bank = 0
                phase = 0
                turn += 1

            for gr in players:
                g_result = combination(gr.hand, table)
                gr.score = g_result[0]
                gr.comb_suit = g_result[1]

            time.sleep(0.2)
            continue

        if len(players) <= 1:
            for p in players:
                p.move_made = True
                p.bet = 0
            continue

        GUI().draw_game_manip(game_screen, table, players[0], blind, start_players, max_bet, bank, bet_mulpiplier, len(players) <= 1, turn)

        # AI move.
        if players[current_num].bankrupt:
            players[current_num].move_made = True
            current_num = (current_num + 1) % len(players)
        elif not (current_num == 0 and players[0].is_player) and not all([g.move_made for g in players]):
            if not players[current_num].fold:
                ai_result = ai_move(players[current_num], table, max_bet, blind, players, phase, start_players)

                if players[current_num].fold:
                    continue
                elif players[current_num].bal == ai_result[1]:
                    players[current_num].previous_bet = 0

                smbd_raised = ai_result[0]
                bank, max_bet = players[current_num].add_bet(ai_result[1], bank, max_bet, turn, phase, players, table, smbd_raised)

                current_num = (current_num + 1) % len(players)

        GUI().draw_game_manip(game_screen, table, players[0], blind, start_players, max_bet, bank, bet_mulpiplier, len(players) <= 1, turn)
        pygame.display.flip()


if __name__ == "__main__":
    run_game()
