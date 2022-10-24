from data.constants import *
from data.managers import *
from data.character_classes import *
# cd Desktop/Programming/pygame/brawlerena/

class Game():
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        info = pygame.display.Info()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) # render width and height

        self.WINDOW_SIZE = (1280, 720) # scaled up window size
        self.final_screen = pygame.display.set_mode(self.WINDOW_SIZE, pygame.FULLSCREEN)

        self.full_screen = True

        SCALE_RATIO = 40
        self.screen = pygame.Surface((16 * SCALE_RATIO, 9 * SCALE_RATIO)) # (640, 360)

        pygame.display.set_caption("brawlerena")

        icon_image = get_image("playing/characters/B79/character.png")
        pygame.display.set_icon(icon_image)

    def toggle_screen(self):
        if self.full_screen:
            self.final_screen = pygame.display.set_mode(self.WINDOW_SIZE)
            self.full_screen = False
        else:
            self.final_screen = pygame.display.set_mode(self.WINDOW_SIZE, pygame.FULLSCREEN)
            self.full_screen = True

    def settings_before(self, background_colour, last_time): # get dt, events and keys + updates last_time so dt can work
        self.screen.fill(background_colour)

        dt = time.time() - last_time
        dt *= 30
        last_time = time.time()

        # inputs
        events = pygame.event.get()
        keys = pygame.key.get_pressed()

        # mouse input
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pos = (mouse_x // 2, mouse_y // 2) # divide by 2 because 640 screen is scaled to 1280 which is twice the size

        return dt, events, keys, last_time, mouse_pos

    def settings_after(self, events, keys, screen_key): # checks for usual commands eg escape and screen settings
        if screen_key.is_pressed(keys):
            self.toggle_screen()

        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.final_screen.blit(pygame.transform.scale(self.screen, self.WINDOW_SIZE), (0, 0))

        pygame.display.update()
        self.clock.tick(FPS)

    def test():
        # common settings
        last_time = time.time()
        screen_key = AdvancedKey(pygame.K_EQUALS)

        while True:
            # ------------- usual commands -------------
            dt, events, keys, last_time, mouse_pos = self.settings_before(BACKGROUND_COLOUR, last_time)

            # ------------- main code start -------------


            # ------------- usual commands -------------
            self.settings_after(events, keys, screen_key)

    def single_player_selection(self, key_left, key_right, key_up, key_select):
        if not character_chosen_1:
            if key_D.is_pressed(keys):
                character_index1 += 1

            if key_A.is_pressed(keys):
                character_index1 -= 1

        if key_E.is_pressed(keys):
            character_chosen_1 = not character_chosen_1

    def character_selection(self):
        # common settings
        last_time = time.time()
        screen_key = AdvancedKey(pygame.K_EQUALS)

        character_names = ["GroundHog", "Jian", "Farohar", "B79", "Volta", "Metor"]

        character_ready = {
            "GroundHog" : True,
            "B79": False,
            "Jian": True,
            "Volta": False,
            "Metor": False,
            "Farohar": True,
        }

        with open('data/player_data.json', 'r') as f:
            player_data = json.load(f)

        player1 = PlayerSelection(1, self.screen, character_names, player_data)
        player2 = PlayerSelection(2, self.screen, character_names, player_data)

        end_timer_started = False

        while True:
            # ------------- usual commands -------------
            dt, events, keys, last_time, mouse_pos = self.settings_before(BACKGROUND_COLOUR, last_time)

            # ------------- main code start -------------

            # prevent taking inputs when other player is inputing username / password
            if player2.navigation != "input":
                player1.input_update(keys, events, mouse_pos)
            if player1.navigation != "input":
                player2.input_update(keys, events, mouse_pos)

            if player1.character_chosen and player2.character_chosen:
                # go to next gamestate if both players chose characters
                if not end_timer_started:
                    end_timer = Timer()
                    end_timer_started = True

            # for waiting one second after both players chose character
            if end_timer_started and end_timer.time_elapsed() > 1:
                break

            player1.scroll()
            player2.scroll()

            # display section  -----------------------
            player1.cards_display()
            player2.cards_display()

            player1.selection_circle_display()
            player2.selection_circle_display()

            player1.button_display(mouse_pos)
            player2.button_display(mouse_pos)

            player1.authentication_display()
            player2.authentication_display()

            if player1.navigation == "input":
                player2.waiting_display()
            elif player2.navigation == "input":
                player1.waiting_display()

            # black separator
            pygame.draw.rect(self.screen, BLACK, (MID_X - X_OFFSET, 0, 2 * X_OFFSET, HEIGHT))

            # ------------- usual commands -------------
            self.settings_after(events, keys, screen_key)

        return character_names[player1.character_index], character_names[player2.character_index], player1.username, player2.username

    def fighting(self, character1, character2, username1, username2):
        # common settings
        last_time = time.time()
        screen_key = AdvancedKey(pygame.K_EQUALS)

        joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

        for joystick in joysticks:
            joystick.init()
            print(joystick.get_name())

        player1 = eval(character1 + "(1, \"keyboard\")")
        player2 = eval(character2 + "(2, \"keyboard\")")

        # player name texts
        player1_name_text = Text(self.screen, "FONT_10", PLAYER_BLUE, (NAME_X, NAME_Y), username1, display_method = "top_left")
        player2_name_text = Text(self.screen, "FONT_10", PLAYER_RED, (WIDTH - NAME_X, NAME_Y), username2, display_method = "top_right")

        consecutive_collisions = 0
        # variable to keep track of consecutive_collisions
        # so if there is (2 or more) consecutive_collisions clipping can be prevented

        game_state = "playing"

        '''
        All game states:
        playing - players are battling in a game
        round_over - one players wins and game is over
        '''

        # generating glow surface
        # red_glow = glow_surf(10, 100, 4, (143, 0, 11), (38, 0, 3))
        # blue_glow = glow_surf(10, 100, 4, (69, 0, 62), (129, 3, 135))
        # glow_surf = pygame.Surface((120, 120))
        # display_center(glow_surf, circle_surf(60, (20, 20, 20)), (60, 60))
        # display_center(glow_surf, circle_surf(50, (40, 40, 40)), (60, 60))
        # display_center(glow_surf, circle_surf(40, (60, 60, 60)), (60, 60))
        # display_center(glow_surf, circle_surf(30, (80, 80, 80)), (60, 60))
        # display_center(glow_surf, circle_surf(20, (100, 100, 100)), (60, 60))
        # display_center(glow_surf, circle_surf(10, (120, 120, 120)), (60, 60))

        while True:
            # ------------- usual commands -------------
            dt, events, keys, last_time, mouse_pos = self.settings_before(BACKGROUND_COLOUR, last_time)

            # ------------- main code start -------------

            pygame.draw.circle(self.screen, (50, 90, 168), (MID_X, MID_Y), HEIGHT // 2 + 10) # inner circle
            pygame.draw.circle(self.screen, (142, 241, 250), (MID_X, MID_Y), HEIGHT // 2) # outer circle


            if game_state == "playing":

                # collision check first will prevent characters "bumping in mid air"
                if circle_collision((player1.x, player1.y, player1.radius),
                                    (player2.x, player2.y, player2.radius)):

                    '''
                    # x and y positions go back one frame to before the collission
                    player1.x -= player1.dx
                    player1.y -= player1.dy

                    player2.x -= player2.dx
                    player2.y -= player2.dy
                    '''

                    player1.x -= player1.dx
                    player1.y -= player1.dy

                    player2.x -= player2.dx
                    player2.y -= player2.dy

                    player1.dx, player2.dx = collision_physics(player1.dx, player1.mass, player2.dx, player2.mass)
                    player1.dy, player2.dy = collision_physics(player1.dy, player1.mass, player2.dy, player2.mass)

                    consecutive_collisions += 1

                    if consecutive_collisions >= 2:
                        # calculating intersection of line and circle
                        gradient = (player1.y - player2.y) / (player1.x - player2.x)

                        # calculating first intersection coordinates, using player 1 coordinates as origin
                        diff_x1 = math.sqrt((player1.radius ** 2) / (1 + (gradient ** 2)))

                        if player1.x < player2.x:
                            intersection_x1 = player1.x + diff_x1
                        else:
                            intersection_x1 = player1.x - diff_x1

                        intersection_y1 = gradient * intersection_x1

                        # calculating second intersection coordinates, using player 2 coordinates as origin
                        diff_x2 = math.sqrt((player2.radius ** 2) / (1 + (gradient ** 2)))

                        if player2.x < player1.x:
                            intersection_x2 = player2.x + diff_x2
                        else:
                            intersection_x2 = player2.x - diff_x2

                        intersection_y2 = gradient * intersection_x2

                        # calculating midpoint of intersections
                        mid_point_x = (intersection_x1 + intersection_x2) / 2
                        mid_point_y = (intersection_y1 + intersection_y2) / 2

                        # updating the player coordinates
                        player1.x += mid_point_x - intersection_x1
                        player1.y += mid_point_y - intersection_y1

                        player2.x += mid_point_x - intersection_x2
                        player2.y += mid_point_y - intersection_y2
                else:
                    consecutive_collisions = 0

                player1.update(keys, events)
                player2.update(keys, events)

                player1.powerup_update(keys, player2)
                player2.powerup_update(keys, player1)

                # lives is changed in class function
                player1_lose = player1.out_of_bounds()
                player2_lose = player2.out_of_bounds()

                # updating game state based on loss
                if player1_lose or player2_lose:

                    # assigning winning player
                    if player1_lose:
                        winning_username = username2
                    elif player2_lose:
                        winning_username = username1

                    # assigning winning player moving texts
                    if player1.lives <= 0 or player2.lives <= 0:
                        game_state = "match_over"
                        match_over_text = MovingText(self.screen, "FONT_20", BLACK, (MID_X, MID_Y), f"{winning_username} VICTORIOUS!!")
                    else:
                        game_state = "round_over"
                        round_over_text = MovingText(self.screen, "FONT_20", BLACK, (MID_X, MID_Y), f"{winning_username} WINS!")
                    # -1 to account for 0 index


            player1_name_text.display()
            player2_name_text.display()

            player1.powerup_display(self.screen)
            player2.powerup_display(self.screen)


            player1.display(self.screen)
            player2.display(self.screen)

            #display_center(self.screen, red_glow, (player1.x, player1.y), special_flags = BLEND_RGB_ADD)
            #display_center(self.screen, blue_glow, (player2.x, player2.y), special_flags = BLEND_RGB_ADD)

            player1.display_lives(self.screen)
            player2.display_lives(self.screen)


            # pygame.draw.circle(self.screen, (255, 74, 213), (MID_X, MID_Y), 50, special_flags = BLEND_RGB_ADD)


            if game_state == "round_over":
                round_over_text.display()

                if round_over_text.is_finished():
                    game_state = "playing"

                    player1.reset()
                    player2.reset()

            elif game_state == "match_over":
                match_over_text.display()

                if match_over_text.is_finished():
                    break

            # ------------- usual commands -------------
            self.settings_after(events, keys, screen_key)

def run_game():
    game = Game()

    while True:
        character1, character2, username1, username2 = game.character_selection()
        game.fighting(character1, character2, username1, username2)
