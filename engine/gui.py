from engine.objects import GameObjects
import pygame


B_WIDTH = GameObjects.B_WIDTH
B_HEIGHT = GameObjects.B_HEIGHT
BUTTON_SIZE = GameObjects.BUTTON_SIZE
TOP_IN_MAIN_MENU = GameObjects.TOP_IN_MAIN_MENU
FONT_SIZE = GameObjects.FONT_SIZE
CARD_SIZE = GameObjects.CARD_SIZE
USER_BTN_X = GameObjects.USER_BTN_X
USER_BTN_Y = GameObjects.USER_BTN_Y
GAP_IN_MAIN_MENU = GameObjects.GAP_IN_MAIN_MENU
COMBINATIONS = GameObjects.combinations
FOREGROUND_FONT_COLOUR = GameObjects.FOREGROUND_FONT_COLOUR
BACKGROUND_FONT_COLOUR = GameObjects.BACKGROUND_FONT_COLOUR
BUTTON_TRANSPARENCY_VALUE = 100
MAIN_MENU_BACKGROUND = pygame.image.load("images/backgrounds/main_menu_background.png")
CARD_SHIRT = pygame.transform.scale(pygame.image.load("images/cards/card_shirt.png"), (CARD_SIZE[0], CARD_SIZE[1]))
CHIPS_PNG = pygame.transform.scale(pygame.image.load("images/chips.png"), (CARD_SIZE[0]//2, CARD_SIZE[0]//2))
BANK_CHIPS_PNG = pygame.transform.scale(pygame.image.load("images/chips.png"), (CARD_SIZE[0]//1.5, CARD_SIZE[0]//1.5))
DEALER_CHIP = pygame.transform.scale(pygame.image.load("images/dealer_chip.png"), (CARD_SIZE[0]//1.2, CARD_SIZE[0]//1.2))
FOLD_BTN = pygame.transform.scale(pygame.image.load("images/buttons/fold_btn.png"), (USER_BTN_X, USER_BTN_Y))
CALL_BTN = pygame.transform.scale(pygame.image.load("images/buttons/call_btn.png"), (USER_BTN_X, USER_BTN_Y))
RAISE_BTN = pygame.transform.scale(pygame.image.load("images/buttons/raise_btn.png"), (USER_BTN_X*1.2, USER_BTN_Y))
U_STAKE_BTN = pygame.transform.scale(pygame.image.load("images/buttons/upper_stake.png"), (USER_BTN_Y, USER_BTN_Y))
L_STAKE_BTN = pygame.transform.scale(pygame.image.load("images/buttons/lower_stake.png"), (USER_BTN_Y, USER_BTN_Y))
ALLIN_BTN = pygame.transform.scale(pygame.image.load("images/buttons/allin_btn.png"), (USER_BTN_Y*1.75, USER_BTN_Y))
CARDS_PNG = GameObjects.cards_png
cards_let_num = {"10": "T", "11": "J", "12": "Q", "13": "K", "14": "A"}


class GUI:
    ### /* Main Menu stuff ###
    def draw_mm_button(self, font_type, text, selected_button, curr_btn, position, game_screen) -> None:
        text_object = font_type.render(text, False, pygame.Color(BACKGROUND_FONT_COLOUR))
        text_location = pygame.Rect(0, position, B_WIDTH, 100).move(B_WIDTH / 2 - text_object.get_width() / 2, 0)
        game_screen.blit(text_object, text_location)
        text_object = font_type.render(text, False, pygame.Color(list(map(lambda x: x + 55, FOREGROUND_FONT_COLOUR)) if selected_button == curr_btn else FOREGROUND_FONT_COLOUR))
        game_screen.blit(text_object, text_location.move(2, 2))

    def draw_main_menu(self, game_screen, selected_button, player_bal) -> None:
        game_screen.blit(pygame.transform.scale(pygame.image.load("images/backgrounds/main_menu_background.png"), (B_WIDTH, B_HEIGHT)), (0, 0))
        self.dim_bg(game_screen)

        font_type = pygame.font.SysFont("Arial", FONT_SIZE, True, False)
        font_type_main = pygame.font.SysFont("Arial", FONT_SIZE * 2, True, False)

        self.draw_mm_button(font_type_main, "Main Menu", False, True, int(GameObjects.SCREENSIZE[1] / 14), game_screen)
        self.draw_mm_button(font_type, "Play", selected_button, 0, TOP_IN_MAIN_MENU - GAP_IN_MAIN_MENU, game_screen)
        self.draw_mm_button(font_type, "Setting", selected_button, 1, TOP_IN_MAIN_MENU, game_screen)
        self.draw_mm_button(font_type, "Exit", selected_button, 2, TOP_IN_MAIN_MENU + GAP_IN_MAIN_MENU, game_screen)

        # self.draw_player_info(game_screen, player_bal)

    def draw_player_info(self, game_screen, player_bal):
        font_type = pygame.font.SysFont("Arial", FONT_SIZE//2, True, False)
        text_object = font_type.render(f"Player balance: {player_bal}", False, pygame.Color((230, 230, 250)))
        text_location = pygame.Rect(0, B_HEIGHT - FONT_SIZE//1.6, 0, 0)
        game_screen.blit(text_object, text_location)

    def hightlighting_the_button(self, screen, chosen_button) -> None:
        if chosen_button:
            button = pygame.Surface((chosen_button.width, chosen_button.height))
            button.set_alpha(BUTTON_TRANSPARENCY_VALUE)
            button.fill(pygame.Color(100, 100, 100))
            screen.blit(button, (chosen_button.x, chosen_button.y))

    def dim_bg(self, game_screen, alpha=60) -> None:
        bg_dimmed = pygame.Surface((B_WIDTH, B_HEIGHT))
        bg_dimmed.set_alpha(alpha)
        bg_dimmed.fill(pygame.Color(10, 10, 10))
        game_screen.blit(bg_dimmed, (0, 0))
    
    def draw_settings_menu(self, game_screen, selected_button, gam_amount) -> None:
        game_screen.blit(pygame.transform.scale(MAIN_MENU_BACKGROUND, (B_WIDTH, B_HEIGHT)), (0, 0))
        self.dim_bg(game_screen)

        font_type = pygame.font.SysFont("Arial", FONT_SIZE, True, False)
        font_type_main = pygame.font.SysFont("Arial", FONT_SIZE * 2, True, False)

        text_object = font_type_main.render("Settings", False, pygame.Color(BACKGROUND_FONT_COLOUR))
        text_location = pygame.Rect(0, 80, B_WIDTH, 100).move(B_WIDTH / 2 - text_object.get_width() / 2, 0)
        game_screen.blit(text_object, text_location)
        text_object = font_type_main.render("Settings", False, pygame.Color(FOREGROUND_FONT_COLOUR))
        game_screen.blit(text_object, text_location.move(2, 2))

        # Amount of players.
        text_object = font_type.render(f"Amount of players: {gam_amount}", False, pygame.Color(BACKGROUND_FONT_COLOUR))
        text_location = pygame.Rect(0, TOP_IN_MAIN_MENU - GAP_IN_MAIN_MENU, B_WIDTH, 100).move(B_WIDTH / 2 - text_object.get_width() / 1.8, 0)
        game_screen.blit(text_object, text_location)
        text_object = font_type.render(f"Amount of players: {gam_amount}", False, pygame.Color(list(map(lambda x: x + 55, FOREGROUND_FONT_COLOUR)) if selected_button == 0 else FOREGROUND_FONT_COLOUR))
        game_screen.blit(text_object, text_location.move(2, 2))

        # Username.
        text_object = font_type.render(f"Username:         ", False, pygame.Color(BACKGROUND_FONT_COLOUR))
        text_location = pygame.Rect(0, TOP_IN_MAIN_MENU, B_WIDTH, 100).move(B_WIDTH / 2 - text_object.get_width() / 1.8, 0)
        game_screen.blit(text_object, text_location)
        text_object = font_type.render(f"Username:         ", False, pygame.Color(list(map(lambda x: x + 55, FOREGROUND_FONT_COLOUR)) if selected_button == 1 else FOREGROUND_FONT_COLOUR))
        game_screen.blit(text_object, text_location.move(2, 2))

        # Return to Main Menu.
        text_object = font_type.render("Return to Main Menu", False, pygame.Color(BACKGROUND_FONT_COLOUR))
        text_location = pygame.Rect(0, TOP_IN_MAIN_MENU + GAP_IN_MAIN_MENU, B_WIDTH, 100).move(B_WIDTH / 2 - text_object.get_width() / 1.8, 0)
        game_screen.blit(text_object, text_location)
        text_object = font_type.render("Return to Main Menu", False, pygame.Color(list(map(lambda x: x + 55, FOREGROUND_FONT_COLOUR)) if selected_button == 2 else FOREGROUND_FONT_COLOUR))
        game_screen.blit(text_object, text_location.move(2, 2))

    ### Main Menu stuff */ ###

    ### /* Game stuff ###

    def show_bet(self, screen, gambler, pos) -> None:
        x, y = pos
        font_type = pygame.font.SysFont("Arial", int(FONT_SIZE//2.5), True, False)
        text_object = font_type.render(f"{gambler.curr_state}: {str(gambler.bet)}", False, pygame.Color(0, 0, 0))
        text_location = pygame.Rect(x, y, B_WIDTH, 100)
        screen.blit(text_object, text_location)

    def show_check_or_fold(self, screen, pos, text="Check") -> None:
        x, y = pos

        if text == "Fold":
            clr = pygame.Color(255, 50, 50)
        else:
            clr = pygame.Color(0, 0, 0)

        font_type = pygame.font.SysFont("Arial", int(FONT_SIZE//2.5), True, False)
        text_object = font_type.render(text, False, clr)
        text_location = pygame.Rect(x, y, B_WIDTH, 100)
        screen.blit(text_object, text_location)
    
    def show_end_combinaton(self, screen, pos, gambler) -> None:
        x, y = pos
        
        if int(gambler.score) == 9 and int(str(gambler.score)[2:4]) == 14:
            gambler.score = 10
            shown_card = ''
        elif gambler.high_card and 2 <= int(gambler.high_card) <= 9:
            try:
                shown_card = int(gambler.high_card)
            except:
                shown_card = ''
        else:
            try:
                shown_card = cards_let_num[gambler.high_card]
            except:
                shown_card = ''

        font_type = pygame.font.SysFont("Arial", int(FONT_SIZE//2.5), True, False)
        text_object = font_type.render(f"{COMBINATIONS[int(gambler.score)]} {gambler.comb_suit if gambler.comb_suit else ''} {'High card:' if gambler.high_card and shown_card else ''} {shown_card}", False, pygame.Color(255, 255, 255))
        text_location = pygame.Rect(x, y, B_WIDTH, 100)
        screen.blit(text_object, text_location)

    def print_win_gain(self, screen, pos, text) -> None:
        x, y = pos
        screen.blit(CHIPS_PNG, pygame.Rect(x, y, CARD_SIZE[0], CARD_SIZE[0]).move(FONT_SIZE//3.5, 0))
        font_type = pygame.font.SysFont("Arial", int(FONT_SIZE//2.5), True, False)
        text_object = font_type.render(f"+     {text}", False, pygame.Color(120, 255, 100))
        text_location = pygame.Rect(x, y, B_WIDTH, 100)
        screen.blit(text_object, text_location)

    def draw_gambler(self, screen, gambler, last_stand, show_up, blind) -> None:
        # Background and avatar.
        screen.blit(pygame.transform.scale(pygame.image.load("images/backgrounds/gambler_background.png"), (gambler.x_size, gambler.y_size)), gambler.box)
        if gambler.fold:
            screen.blit(pygame.transform.scale(pygame.image.load("images/backgrounds/fold_background.png"), (gambler.x_size, gambler.y_size)), gambler.box)
        screen.blit(gambler.image, pygame.Rect(gambler.x_pos - gambler.x_size//2.2, gambler.y_pos + gambler.y_size//8, gambler.y_pos - 2, gambler.y_pos - 2))

        # Nickname.
        font_type = pygame.font.SysFont("Arial", FONT_SIZE//2, True, False)
        text_object = font_type.render(gambler.name, False, pygame.Color(0, 0, 0))
        text_location = pygame.Rect(gambler.x_pos + 0, gambler.y_pos + gambler.y_size//2.2, B_WIDTH, 100)
        screen.blit(text_object, text_location)

        # Hand.
        screen.blit(CARDS_PNG[gambler.hand[0]] if gambler.card_shown else CARD_SHIRT, \
            pygame.Rect(gambler.x_pos - gambler.x_size//40, gambler.y_pos - gambler.y_size//4.25, CARD_SIZE[0], CARD_SIZE[1]))
        screen.blit(CARDS_PNG[gambler.hand[1]] if gambler.card_shown else CARD_SHIRT, \
            pygame.Rect(gambler.x_pos + gambler.x_size//4.9, gambler.y_pos - gambler.y_size//4.25, CARD_SIZE[0], CARD_SIZE[1]))

        # Balance.
        font_type = pygame.font.SysFont("Arial", int(FONT_SIZE//2.5), False, False)
        if gambler.hglght_win:
            text_object = font_type.render(str(gambler.bal), False, pygame.Color(120, 255, 100))
        else:
            text_object = font_type.render(str(gambler.bal), False, pygame.Color(0, 0, 0))
        text_location = pygame.Rect(gambler.x_pos + gambler.x_size//7, gambler.y_pos + gambler.y_size//1.4, B_WIDTH, 100)
        screen.blit(text_object, text_location)
        screen.blit(CHIPS_PNG, pygame.Rect(gambler.x_pos + gambler.x_size//40, gambler.y_pos + gambler.y_size//1.4, CARD_SIZE[0], CARD_SIZE[0]))

        # Dealer chip.
        if gambler.is_dealer: 
            screen.blit(DEALER_CHIP, pygame.Rect(gambler.x_pos - gambler.x_size//2, gambler.y_pos + gambler.y_size//1.6, CARD_SIZE[0], CARD_SIZE[0]))
        
        # Bet.
        gam_pos = {
            0: (gambler.x_pos - gambler.x_size//7.5, gambler.y_pos - gambler.y_size//2),
            1: (gambler.x_pos + gambler.x_size//1.95, gambler.y_pos + gambler.y_size//2.5),
            2: (gambler.x_pos + gambler.x_size//100, gambler.y_pos + gambler.y_size*1.1),
            3: (gambler.x_pos - gambler.x_size//2.8, gambler.y_pos + gambler.y_size*1.1),
            4: (gambler.x_pos - gambler.x_size//1.1, gambler.y_pos + gambler.y_size//2.5),
        }

        gam_win_pos = {
            0: (gambler.x_pos - gambler.x_size//7.5, gambler.y_pos - gambler.y_size//2 - FONT_SIZE//2.2),
            1: (gambler.x_pos + gambler.x_size//1.95, gambler.y_pos + gambler.y_size//2.5 - FONT_SIZE//2.2),
            2: (gambler.x_pos + gambler.x_size//100 + FONT_SIZE//2.2, gambler.y_pos + gambler.y_size*1.1 + FONT_SIZE//2.2),
            3: (gambler.x_pos - gambler.x_size//2.8 - FONT_SIZE//2.2, gambler.y_pos + gambler.y_size*1.1 + FONT_SIZE//2.2),
            4: (gambler.x_pos - gambler.x_size//1.2, gambler.y_pos + gambler.y_size//2.5 - FONT_SIZE//2.2),
        }

        # Combination.
        if gambler.is_player and gambler.score >= 2:
            clr_num = int(gambler.score)
            if clr_num <= 9:
                clr = pygame.Color(int(2**(clr_num-1) - 1), 255, int(2**(clr_num-2) - 1))
            if int(gambler.score) == 9 and int(str(gambler.score)[2:4]) == 10:
                clr = pygame.Color(255, 0, 0)
                gambler.score = 10
                shown_card = ''
            elif int(str(gambler.score)[2:4]) <= 9:
                shown_card = int(str(gambler.score)[2:4])
            else:
                shown_card = cards_let_num[str(gambler.score)[2:4]]
            if int(gambler.score) in [3, 5, 6, 7, 9, 10]:
                shown_card = ''
            font_type = pygame.font.SysFont("Arial", int(FONT_SIZE//2), True, False)
            text_object = font_type.render(f"{COMBINATIONS[int(gambler.score)]} {gambler.comb_suit if gambler.comb_suit else ''}{'' if int(gambler.score) in [3, 5, 6, 7, 9, 10] else ':'} {shown_card}", False, clr)
            text_location = pygame.Rect(gambler.x_pos + gambler.x_size//1.8, gambler.y_pos + gambler.y_size//2.2, 100, 100)
            screen.blit(text_object, text_location)
            
        if GameObjects.DEBUG_MODE and GameObjects.SCAN_MODE:
            self.show_end_combinaton(screen, gam_pos[gambler.num], gambler)

        # Show fold, check, call & bet.
        if show_up and not gambler.fold:
            self.show_end_combinaton(screen, gam_pos[gambler.num], gambler)
        elif not last_stand:
            if gambler.bet > 0 and gambler.bal > 0:
                self.show_bet(screen, gambler, gam_pos[gambler.num])
            elif gambler.move_made and gambler.bet == 0 and not gambler.fold and not gambler.bal <= 0:
                self.show_check_or_fold(screen, gam_pos[gambler.num])
            elif gambler.fold:
                self.show_check_or_fold(screen, gam_pos[gambler.num], "Fold")
            elif gambler.bal <= 0:
                self.show_check_or_fold(screen, gam_pos[gambler.num], "All in!")

        if gambler.win_gain != 0:
            self.print_win_gain(screen, gam_win_pos[gambler.num], gambler.win_gain)
    
    def draw_game_manip(self, game_screen, table, player, blind, start_players, max_bet, bank, bet_mulpiplier, last_stand, turn, show_up=False) -> None:
        game_screen.blit(pygame.transform.scale(pygame.image.load("images/backgrounds/table_background.png"), (B_WIDTH, B_HEIGHT)), (0, 0))

        # Table table.
        if table != None:
            C_S = []
            C_S.append(CARD_SIZE[0]*1.2)
            C_S.append(CARD_SIZE[1]*1.2)
            if len(table) == 3:
                game_screen.blit(pygame.transform.scale(CARDS_PNG[table[0]], (C_S[0], C_S[1])), \
                    pygame.Rect(B_WIDTH//2 - CARD_SIZE[0]*3.5, B_HEIGHT//2.3, B_WIDTH, 100))
                game_screen.blit(pygame.transform.scale(CARDS_PNG[table[1]], (C_S[0], C_S[1])), \
                    pygame.Rect(B_WIDTH//2 - CARD_SIZE[0]*2, B_HEIGHT//2.3, B_WIDTH, 100))
                game_screen.blit(pygame.transform.scale(CARDS_PNG[table[2]], (C_S[0], C_S[1])), \
                    pygame.Rect(B_WIDTH//2 - CARD_SIZE[0]//2, B_HEIGHT//2.3, B_WIDTH, 100))
            if len(table) == 4:
                game_screen.blit(pygame.transform.scale(CARDS_PNG[table[0]], (C_S[0], C_S[1])), \
                    pygame.Rect(B_WIDTH//2 - CARD_SIZE[0]*3.5, B_HEIGHT//2.3, B_WIDTH, 100))
                game_screen.blit(pygame.transform.scale(CARDS_PNG[table[1]], (C_S[0], C_S[1])), \
                    pygame.Rect(B_WIDTH//2 - CARD_SIZE[0]*2, B_HEIGHT//2.3, B_WIDTH, 100))
                game_screen.blit(pygame.transform.scale(CARDS_PNG[table[2]], (C_S[0], C_S[1])), \
                    pygame.Rect(B_WIDTH//2 - CARD_SIZE[0]//2, B_HEIGHT//2.3, B_WIDTH, 100))
                game_screen.blit(pygame.transform.scale(CARDS_PNG[table[3]], (C_S[0], C_S[1])), \
                    pygame.Rect(B_WIDTH//2 + CARD_SIZE[0], B_HEIGHT//2.3, B_WIDTH, 100))
            if len(table) == 5:
                game_screen.blit(pygame.transform.scale(CARDS_PNG[table[0]], (C_S[0], C_S[1])), \
                    pygame.Rect(B_WIDTH//2 - CARD_SIZE[0]*3.5, B_HEIGHT//2.3, B_WIDTH, 100))
                game_screen.blit(pygame.transform.scale(CARDS_PNG[table[1]], (C_S[0], C_S[1])), \
                    pygame.Rect(B_WIDTH//2 - CARD_SIZE[0]*2, B_HEIGHT//2.3, B_WIDTH, 100))
                game_screen.blit(pygame.transform.scale(CARDS_PNG[table[2]], (C_S[0], C_S[1])), \
                    pygame.Rect(B_WIDTH//2 - CARD_SIZE[0]//2, B_HEIGHT//2.3, B_WIDTH, 100))
                game_screen.blit(pygame.transform.scale(CARDS_PNG[table[3]], (C_S[0], C_S[1])), \
                    pygame.Rect(B_WIDTH//2 + CARD_SIZE[0], B_HEIGHT//2.3, B_WIDTH, 100))
                game_screen.blit(pygame.transform.scale(CARDS_PNG[table[4]], (C_S[0], C_S[1])), \
                    pygame.Rect(B_WIDTH//2 + CARD_SIZE[0]*2.5, B_HEIGHT//2.3, B_WIDTH, 100))
        
        if bank > 0:
            font_type = pygame.font.SysFont("Arial", FONT_SIZE//2, True, False)
            text_object = font_type.render(f"Bank: {bank}", False, pygame.Color(40, 250, 40))
            text_location = pygame.Rect(B_WIDTH//2, B_HEIGHT*0.35, FONT_SIZE, FONT_SIZE).move(-FONT_SIZE, 0)
            game_screen.blit(BANK_CHIPS_PNG, pygame.Rect(B_WIDTH*0.492, B_HEIGHT*0.345, CARD_SIZE[0], CARD_SIZE[0]).move(-B_WIDTH / 13.1, 0))
            game_screen.blit(text_object, text_location)
        
        for gambler in start_players:
            GUI().draw_gambler(game_screen, gambler, last_stand, show_up, blind)
        
        if player.current_move and not all(b.move_made for b in start_players) and not player.fold and player.is_player and not player.bal == 0:
            self.user_choice(game_screen, player, blind, max_bet, bet_mulpiplier)

        font_type = pygame.font.SysFont("Arial", int(FONT_SIZE*0.5), True, False)
        text_object = font_type.render(str(turn + 1), False, pygame.Color(70, 10, 10))
        text_location = pygame.Rect(3, 0, B_WIDTH, 100)
        game_screen.blit(text_object, text_location)
        pygame.display.flip()

        pygame.display.flip()

    def user_choice(self, game_screen, player, blind, max_bet, bet_mulpiplier) -> None:
        F_SIZE = int(FONT_SIZE*0.8)
        font_type = pygame.font.SysFont("Arial", F_SIZE, True, False)

        # Fold button.
        game_screen.blit(FOLD_BTN, pygame.Rect(B_WIDTH//2 - USER_BTN_X*1.55, B_HEIGHT*0.9, USER_BTN_X, USER_BTN_Y))
        text_object = font_type.render("Fold", False, pygame.Color(255, 255, 255))
        text_location = pygame.Rect(B_WIDTH//2 - USER_BTN_X*1.55, B_HEIGHT*0.9, F_SIZE, F_SIZE).move(F_SIZE, F_SIZE//5)
        game_screen.blit(text_object, text_location)

        # Call button.
        if len(str(max_bet)) < 4:
            font_type = pygame.font.SysFont("Arial", F_SIZE, True, False)
        else:
            font_type = pygame.font.SysFont("Arial", int(F_SIZE*0.9), True, False)
        if max_bet == 0 or player.bet == max_bet:
            game_screen.blit(CALL_BTN, pygame.Rect(B_WIDTH//2 - USER_BTN_X*0.5, B_HEIGHT*0.9, USER_BTN_X, USER_BTN_Y))
            text_object = font_type.render(f"Check", False, pygame.Color(255, 255, 255))
            text_location = pygame.Rect(B_WIDTH//2 - USER_BTN_X*0.45, B_HEIGHT*0.9, F_SIZE, F_SIZE).move(F_SIZE//3, F_SIZE//5)
            game_screen.blit(text_object, text_location)
        else:
            game_screen.blit(CALL_BTN, pygame.Rect(B_WIDTH//2 - USER_BTN_X*0.5, B_HEIGHT*0.9, USER_BTN_X, USER_BTN_Y))
            text_object = font_type.render(f"Call {min(max_bet, player.bal)}", False, pygame.Color(255, 255, 255))
            text_location = pygame.Rect(B_WIDTH//2 - USER_BTN_X*0.5, B_HEIGHT*0.9, F_SIZE, F_SIZE).move(F_SIZE//3, F_SIZE//5)
            game_screen.blit(text_object, text_location)
        
        # Raise button.
        if len(str(max_bet + blind*bet_mulpiplier)) < 4:
            font_type = pygame.font.SysFont("Arial", F_SIZE, True, False)
        else:
            font_type = pygame.font.SysFont("Arial", int(F_SIZE*0.9), True, False)
        game_screen.blit(RAISE_BTN, pygame.Rect(B_WIDTH//2 + USER_BTN_X*0.55, B_HEIGHT*0.9, USER_BTN_X*2, USER_BTN_Y))
        text_object = font_type.render(f"Raise {min(max_bet + blind*bet_mulpiplier, player.bal)}", False, pygame.Color(255, 255, 255))
        text_location = pygame.Rect(B_WIDTH//2 + USER_BTN_X*0.55, B_HEIGHT*0.9, F_SIZE, F_SIZE).move(F_SIZE//3, F_SIZE//5)
        game_screen.blit(text_object, text_location)

        # Upper stake button.
        game_screen.blit(U_STAKE_BTN, pygame.Rect(B_WIDTH//2 + USER_BTN_X*1.8, B_HEIGHT*0.9, USER_BTN_Y, USER_BTN_Y))

        # Lower stake button.
        game_screen.blit(L_STAKE_BTN, pygame.Rect(B_WIDTH//2 + USER_BTN_X*2.2, B_HEIGHT*0.9, USER_BTN_Y, USER_BTN_Y))

        # All-in button.
        font_type = pygame.font.SysFont("Arial", F_SIZE, True, False)
        font_type = pygame.font.SysFont("Arial", int(F_SIZE//1.5), True, False)
        game_screen.blit(ALLIN_BTN, pygame.Rect(0, B_HEIGHT*0.9, USER_BTN_Y*1.5, USER_BTN_Y))
        text_object = font_type.render(f"ALL IN!", False, pygame.Color(255, 0, 0))
        text_location = pygame.Rect(0, B_HEIGHT*0.9, F_SIZE, F_SIZE).move(F_SIZE//5, F_SIZE//2.5)
        game_screen.blit(text_object, text_location)

        pygame.display.flip()

    ### Game stuff */ ###

    def draw_endgame_stuff(self, game_screen) -> None:
        bg_dimmed = pygame.Surface((B_WIDTH, B_HEIGHT))
        bg_dimmed.set_alpha(1)
        bg_dimmed.fill(pygame.Color(10, 10, 10))
        game_screen.blit(bg_dimmed, (0, 0))

        font_type = pygame.font.SysFont("Arial", FONT_SIZE, True, False)
        text_object = font_type.render("End Of The Game", False, pygame.Color(205, 205, 205))
        text_location = pygame.Rect(B_WIDTH / 2 - text_object.get_width() / 2, B_HEIGHT / 2 - text_object.get_height(), B_WIDTH, 100)
        game_screen.blit(text_object, text_location)

        font_type = pygame.font.SysFont("Arial", int(FONT_SIZE//3), True, False)
        text_object = font_type.render("Press any button to return to the Main Menu.", False, pygame.Color(205, 205, 205))
        text_location = pygame.Rect(B_WIDTH / 2 - text_object.get_width() / 2, B_HEIGHT / 2, B_WIDTH, 100)
        game_screen.blit(text_object, text_location)

        pygame.display.flip()
