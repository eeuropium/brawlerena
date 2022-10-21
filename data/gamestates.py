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
        final_screen = pygame.display.set_mode(self.WINDOW_SIZE, pygame.FULLSCREEN)

        self.full_screen = True

        SCALE_RATIO = 40
        self.screen = pygame.Surface((16 * SCALE_RATIO, 9 * SCALE_RATIO)) # (640, 360)

        pygame.display.set_caption("brawlerena")

    def test(): # with scaled self.screen
        run = True
        final_screen = pygame.display.set_mode(self.WINDOW_SIZE, pygame.FULLSCREEN)


        while run:
            # ------------- usual commands -------------
            self.screen.fill((255, 255, 255))
            events = pygame.event.get()
            key = pygame.key.get_pressed()

            # ------------- main code start -------------


            # ------------- usual commands -------------
            if key[pygame.K_ESCAPE]:
                final_screen = pygame.display.set_mode(self.WINDOW_SIZE)
                pygame.quit()
                sys.exit()

            if key[pygame.K_EQUALS]:
                if self.full_screen:
                    final_screen = pygame.display.set_mode(self.WINDOW_SIZE)
                    self.full_screen = False
                else:
                    final_screen = pygame.display.set_mode(self.WINDOW_SIZE, pygame.FULLSCREEN)
                    self.full_screen = True

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            final_screen.blit(pygame.transform.scale(self.screen, self.WINDOW_SIZE), (0, 0))

            pygame.display.update()
            self.clock.tick(FPS)


    def character_selection(self):
        if self.full_screen:
            final_screen = pygame.display.set_mode(self.WINDOW_SIZE, pygame.FULLSCREEN)
        else:
            final_screen = pygame.display.set_mode(self.WINDOW_SIZE)

        run = True

        character_names = ["GroundHog", "B79", "Jian", "Volta", "Metor"]
        character_images = [image("playing/characters/" + i + "/character.png") for i in character_names]
        character_powerup_images = [image("playing/characters/" + i + "/icon.png") for i in character_names]
        num_characters = len(character_names)

        character_ready = {
            "GroundHog" : True,
            "B79": False,
            "Jian": True,
            "Volta": False,
            "Metor": False
        }

        green_box_image = image("selection/other/green_box.png")
        # card_image = image("playing/other/card.png")

        x_offset = 10 # x value offset from the middle

        spacing_x = 300 # spacing between characters

        left_mid_x = MID_X // 2 - x_offset # midline for left player self.screen
        right_mid_x = MID_X * 1.5 + x_offset


        # selection_surface rendering---------------------------
        selection_surface = pygame.Surface((spacing_x * (num_characters - 1) + MID_X, HEIGHT))

        intermediate_colorkey = (255, 0, 242)
        selection_surface.fill(intermediate_colorkey)

        position_x = MID_X // 2
        position_y = MID_Y


        for i in range(num_characters):
            card_image = image("selection/cards/card_" + character_names[i] + ".png")
            # character_name_surf = Text(character_names[i], "font_10", SILVER, (position_x, position_y - 115))
            character_name_surf = Text(selection_surface, "font_10", SILVER, (position_x, position_y - 115), character_names[i])

            display_center(selection_surface, card_image, (position_x, position_y)) # card background
            display_center(selection_surface, character_images[i], (position_x, position_y - 69)) # character image
            display_center(selection_surface, character_powerup_images[i], (position_x - 48, position_y + 14)) # powerup icon

            character_name_surf.display()

            if OS == "Windows":
                if not character_ready[character_names[i]]:
                    # grey mask
                    card_mask = pygame.mask.from_surface(card_image)
                    card_mask = card_mask.to_surface(unsetcolor = (0, 0, 0, 0), setcolor = (82, 81, 89, 190))
                    display_center(selection_surface, card_mask, (position_x, position_y))

                    # text
                    coming_soon_text = Text(selection_surface, "font_10", WHITE, (position_x, position_y - 28), "COMING SOON")
                    coming_soon_text.display()

            position_x += spacing_x


        selection_surface.set_colorkey(intermediate_colorkey)
        #-------------------------------------------------------


        # circle_surface rendering---------------------------
        circle_spacing = 20
        circle_radius = 5

        circle_surface = pygame.Surface((circle_spacing * (num_characters - 1) + circle_radius * 2, circle_radius * 2))
        circle_surface.set_colorkey(BLACK)

        position_x = circle_radius
        position_y = circle_radius

        for i in range(num_characters):
            pygame.draw.circle(circle_surface, (148, 148, 148), (position_x, position_y), circle_radius)
            position_x += circle_spacing
        #-------------------------------------------------------

        subsurf_x1 = 0
        subsurf_target_x1 = 0

        subsurf_x2 = 0
        subsurf_target_x2 = 0

        scroll_speed = 15

        key_E = PressKey(pygame.K_e)
        key_D = PressKey(pygame.K_d)
        key_A = PressKey(pygame.K_a)

        key_slash = PressKey(pygame.K_SLASH)
        key_right = PressKey(pygame.K_RIGHT)
        key_left = PressKey(pygame.K_LEFT)

        character_index1 = 0 # character index for player 1
        character_index2 = 0 # character index for player 2

        character_chosen_1 = False
        character_chosen_2 = False

        end_timer_started = False

        while run:
            # ------------- usual commands -------------
            self.screen.fill(BACKGROUND_COLOUR)
            events = pygame.event.get()
            key = pygame.key.get_pressed()

            # ------------- main code start -------------

            # key handling for both players

            if not character_chosen_1:
                if key_D.use_function(key):
                    character_index1 += 1

                if key_A.use_function(key):
                    character_index1 -= 1

            if key_E.use_function(key):
                character_chosen_1 = not character_chosen_1

            if not character_chosen_2:
                if key_right.use_function(key):
                    character_index2 += 1

                if key_left.use_function(key):
                    character_index2 -= 1

            if key_slash.use_function(key):
                character_chosen_2 = not character_chosen_2

            character_index1 %= num_characters
            character_index2 %= num_characters

            if character_chosen_1 and character_chosen_2:
                # go to next gamestate if both players chose characters
                if not end_timer_started:
                    end_timer = Timer()
                    end_timer_started = True

            # for waiting one second after both players chose character
            if end_timer_started and end_timer.time_elapsed() > 1:
                run = False

            # updating target x positions for both players
            subsurf_target_x1 = spacing_x * character_index1
            subsurf_target_x2 = spacing_x * character_index2

            # player 1 scrolling
            if subsurf_x1 < subsurf_target_x1:
                subsurf_x1 += scroll_speed
                subsurf_x1 = min(subsurf_x1, subsurf_target_x1)

            if subsurf_x1 > subsurf_target_x1:
                subsurf_x1 -= scroll_speed
                subsurf_x1 = max(subsurf_x1, subsurf_target_x1)

            # player 2 scrolling
            if subsurf_x2 < subsurf_target_x2:
                subsurf_x2 += scroll_speed
                subsurf_x2 = min(subsurf_x2, subsurf_target_x2)

            if subsurf_x2 > subsurf_target_x2:
                subsurf_x2 -= scroll_speed
                subsurf_x2 = max(subsurf_x2, subsurf_target_x2)


            # display section  -----------------------

            # player 1 ------------------

            if character_chosen_1:
                pygame.draw.rect(self.screen, GREEN_SELECTED, (0, 0, MID_X, HEIGHT)) # green background

            screen_subsurf_1 = selection_surface.subsurface(subsurf_x1, 0, 320, 360) # subsurface for player 1
            display_center(self.screen, screen_subsurf_1, (left_mid_x, MID_Y))

            if character_chosen_1:
                display_center(self.screen, green_box_image, (left_mid_x, MID_Y - 69)) # green box

            # player 2 ------------------

            if character_chosen_2:
                pygame.draw.rect(self.screen, GREEN_SELECTED, (MID_X, 0, MID_X, HEIGHT))
                display_center(self.screen, green_box_image, (right_mid_x, MID_Y - 69))

            screen_subsurf_2 = selection_surface.subsurface(subsurf_x2, 0, 320, 360) # subsurface for player 2
            display_center(self.screen, screen_subsurf_2, (right_mid_x, MID_Y))

            if character_chosen_2:
                display_center(self.screen, green_box_image, (right_mid_x, MID_Y - 69))
            # copy of surface is made because it's hard to calculate position of yellow circle due to variable number of characters

            # circle for player 1 ----------------------
            circle_surface_copy = circle_surface.copy()

            # yellow circle showing which selection the player is on
            pygame.draw.circle(circle_surface_copy, (255, 237, 46), (circle_radius + circle_spacing * character_index1, circle_radius), circle_radius)

            display_center(self.screen, circle_surface_copy, (left_mid_x, MID_Y + 150))

            # circle for player 2 ----------------------
            circle_surface_copy = circle_surface.copy()
            # yellow circle showing which selection the player is on
            pygame.draw.circle(circle_surface_copy, (255, 237, 46), (circle_radius + circle_spacing * character_index2, circle_radius), circle_radius)

            display_center(self.screen, circle_surface_copy, (right_mid_x, MID_Y + 150))

            pygame.draw.rect(self.screen, BLACK, (MID_X - x_offset, 0, 2 * x_offset, HEIGHT))
            # ------------- usual commands -------------
            if key[pygame.K_ESCAPE]:
                final_screen = pygame.display.set_mode(self.WINDOW_SIZE)
                pygame.quit()
                sys.exit()

            if key[pygame.K_EQUALS]:
                if self.full_screen:
                    final_screen = pygame.display.set_mode(self.WINDOW_SIZE)
                    self.full_screen = False
                else:
                    final_screen = pygame.display.set_mode(self.WINDOW_SIZE, pygame.FULLSCREEN)
                    self.full_screen = True

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            final_screen.blit(pygame.transform.scale(self.screen, self.WINDOW_SIZE), (0, 0))

            pygame.display.update()
            self.clock.tick(FPS)

        return character_names[character_index1], character_names[character_index2]


    def fighting(self, character1, character2): # with scaled self.screen
        if self.full_screen:
            final_screen = pygame.display.set_mode(self.WINDOW_SIZE, pygame.FULLSCREEN)
        else:
            final_screen = pygame.display.set_mode(self.WINDOW_SIZE)

        joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

        for joystick in joysticks:
            joystick.init()
            print(joystick.get_name())

        player1 = eval(character1 + "(1, \"keyboard\")")
        player2 = eval(character2 + "(2, \"keyboard\")")


        player_names = ["player 1", "player 2"]

        # player name texts
        player1_name_text = Text(self.screen, "font_10", PLAYER_BLUE, (NAME_X, NAME_Y), player_names[0], display_method = "top_left")
        player2_name_text = Text(self.screen, "font_10", PLAYER_RED, (WIDTH - NAME_X, NAME_Y), player_names[1], display_method = "top_right")

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

        run = True

        while run:
            # ------------- usual commands -------------
            # self.screen.fill((255, 255, 255))
            self.screen.fill(BACKGROUND_COLOUR)
            events = pygame.event.get()
            key = pygame.key.get_pressed()

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

                player1.update(key, events)
                player2.update(key, events)

                player1.powerup_update(key, player2)
                player2.powerup_update(key, player1)

                # lives is changed in class function
                player1_lose = player1.out_of_bounds()
                player2_lose = player2.out_of_bounds()

                # updating game state based on loss
                if player1_lose or player2_lose:

                    # assigning winning player
                    if player1_lose:
                        winning_player = 2
                    elif player2_lose:
                        winning_player = 1

                    # assigning winning player moving texts
                    if player1.lives <= 0 or player2.lives <= 0:
                        game_state = "match_over"
                        match_over_text = MovingText(self.screen, "font_20", BLACK, (MID_X, MID_Y), f"{player_names[winning_player - 1]} VICTORIOUS!!")
                    else:
                        game_state = "round_over"
                        round_over_text = MovingText(self.screen, "font_20", BLACK, (MID_X, MID_Y), f"{player_names[winning_player - 1]} WINS!")
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
            if key[pygame.K_ESCAPE]:
                final_screen = pygame.display.set_mode(self.WINDOW_SIZE)
                pygame.quit()
                sys.exit()

            if key[pygame.K_EQUALS]:
                if self.full_screen:
                    final_screen = pygame.display.set_mode(self.WINDOW_SIZE)
                    self.full_screen = False
                else:
                    final_screen = pygame.display.set_mode(self.WINDOW_SIZE, pygame.FULLSCREEN)
                    self.full_screen = True

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            final_screen.blit(pygame.transform.scale(self.screen, self.WINDOW_SIZE), (0, 0))

            pygame.display.update()
            self.clock.tick(FPS)

def run_game():
    game = Game()

    while True:
        character1, character2 = game.character_selection()
        game.fighting(character1, character2)
