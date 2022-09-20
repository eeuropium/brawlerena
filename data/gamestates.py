from data.constants import *
from data.managers import *
from data.character_classes import *
# cd Desktop/Programming/pygame/brawlerena/

pygame.init()
fps = 30
fpsclock = pygame.time.Clock()

info = pygame.display.Info()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

#scaled screen set up
info = pygame.display.Info()

# WINDOW_SIZE = (pygame.display.Info().current_w, pygame.display.Info().current_h)
WINDOW_SIZE = (1280, 720)

final_screen = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)

SCALE_RATIO = 40
screen = pygame.Surface((16 * SCALE_RATIO, 9 * SCALE_RATIO))
# (640, 360)

pygame.display.set_caption("brawlerena")

def test(): # with scaled screen
    global fullscreen
    run = True
    final_screen = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)


    while run:
        # ------------- usual commands -------------
        screen.fill((255, 255, 255))
        events = pygame.event.get()
        key = pygame.key.get_pressed()

        # ------------- main code start -------------


        # ------------- usual commands -------------
        if key[pygame.K_ESCAPE]:
            final_screen = pygame.display.set_mode(WINDOW_SIZE)
            pygame.quit()
            sys.exit()

        if key[pygame.K_EQUALS]:
            if fullscreen:
                final_screen = pygame.display.set_mode(WINDOW_SIZE)
                fullscreen = False
            else:
                final_screen = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
                fullscreen = True

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        final_screen.blit(pygame.transform.scale(screen, WINDOW_SIZE), (0, 0))

        pygame.display.update()
        fpsclock.tick(fps)


def character_selection():
    global fullscreen

    if fullscreen:
        final_screen = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
    else:
        final_screen = pygame.display.set_mode(WINDOW_SIZE)

    run = True

    character_names = ["GroundHog", "B79", "Jian", "Volta", "Metor"]
    character_images = [image("playing/characters/" + i + "/character.png") for i in character_names]
    character_powerup_images = [image("playing/characters/" + i + "/icon.png") for i in character_names]
    num_characters = len(character_names)

    green_box_image = image("selection/other/green_box.png")
    # card_image = image("playing/other/card.png")

    x_offset = 10 # x value offset from the middle

    spacing_x = 300 # spacing between characters

    left_mid_x = MID_X // 2 - x_offset # midline for left player screen
    right_mid_x = MID_X * 1.5 + x_offset


    # selection_surface rendering---------------------------
    selection_surface = pygame.Surface((spacing_x * (num_characters - 1) + MID_X, HEIGHT))

    intermediate_colorkey = (255, 0, 242)
    selection_surface.fill(intermediate_colorkey)

    position_x = MID_X // 2
    position_y = MID_Y


    for i in range(num_characters):
        card_image = image("selection/cards/card_" + character_names[i] + ".png")
        character_name_surf = Text(character_names[i], "font_10", SILVER, (position_x, position_y - 115))

        display_center(selection_surface, card_image, (position_x, position_y)) # card background
        display_center(selection_surface, character_images[i], (position_x, position_y - 69)) # character image
        display_center(selection_surface, character_powerup_images[i], (position_x - 48, position_y + 14)) # powerup icon
        character_name_surf.display_text(selection_surface)

        position_x += spacing_x


    selection_surface.set_colorkey(intermediate_colorkey)
    #-------------------------------------------------------


    # circle_surface rendering---------------------------
    circle_spacing = 20
    circle_radius = 5

    circle_surface = pygame.Surface((circle_spacing * (num_characters - 1) + circle_radius * 2, circle_radius * 2))
    circle_surface.fill(WHITE)

    position_x = circle_radius
    position_y = circle_radius

    for i in range(num_characters):
        pygame.draw.circle(circle_surface, (148, 148, 148), (position_x, position_y), circle_radius)
        position_x += circle_spacing

    circle_surface.set_colorkey(WHITE)
    #-------------------------------------------------------

    subsurf_x_1 = 0
    subsurf_target_x_1 = 0

    subsurf_x_2 = 0
    subsurf_target_x_2 = 0

    scroll_speed = 15

    key_E = PressKey(pygame.K_e)
    key_D = PressKey(pygame.K_d)
    key_A = PressKey(pygame.K_a)

    key_slash = PressKey(pygame.K_SLASH)
    key_right = PressKey(pygame.K_RIGHT)
    key_left = PressKey(pygame.K_LEFT)

    character_index_1 = 0 # character index for player 1
    character_index_2 = 0 # character index for player 2

    character_chosen_1 = False
    character_chosen_2 = False

    end_timer_started = False

    while run:
        # ------------- usual commands -------------
        # screen.fill((255, 255, 255))
        screen.fill(BACKGROUND_COLOUR)
        events = pygame.event.get()
        key = pygame.key.get_pressed()

        # ------------- main code start -------------

        # key handling for both players

        if not character_chosen_1:
            if key_D.use_function(key):
                character_index_1 += 1

            if key_A.use_function(key):
                character_index_1 -= 1

        if key_E.use_function(key):
            character_chosen_1 = not character_chosen_1

        if not character_chosen_2:
            if key_right.use_function(key):
                character_index_2 += 1

            if key_left.use_function(key):
                character_index_2 -= 1

        if key_slash.use_function(key):
            character_chosen_2 = not character_chosen_2

        character_index_1 %= num_characters
        character_index_2 %= num_characters

        if character_chosen_1 and character_chosen_2:
            # go to next gamestate if both players chose characters
            if not end_timer_started:
                end_timer = Timer()
                end_timer_started = True
        # for waiting one second after both players chose character
        if end_timer_started and end_timer.time_elapsed() > 1:
            run = False

        # updating target x positions for both players
        subsurf_target_x_1 = spacing_x * character_index_1
        subsurf_target_x_2 = spacing_x * character_index_2

        # player 1 scrolling
        if subsurf_x_1 < subsurf_target_x_1:
            subsurf_x_1 += scroll_speed
            subsurf_x_1 = min(subsurf_x_1, subsurf_target_x_1)

        if subsurf_x_1 > subsurf_target_x_1:
            subsurf_x_1 -= scroll_speed
            subsurf_x_1 = max(subsurf_x_1, subsurf_target_x_1)

        # player 2 scrolling
        if subsurf_x_2 < subsurf_target_x_2:
            subsurf_x_2 += scroll_speed
            subsurf_x_2 = min(subsurf_x_2, subsurf_target_x_2)

        if subsurf_x_2 > subsurf_target_x_2:
            subsurf_x_2 -= scroll_speed
            subsurf_x_2 = max(subsurf_x_2, subsurf_target_x_2)


        # display section  -----------------------

        # player 1 ------------------

        if character_chosen_1:
            pygame.draw.rect(screen, GREEN_SELECTED, (0, 0, MID_X, HEIGHT)) # green background

        screen_subsurf_1 = selection_surface.subsurface(subsurf_x_1, 0, 320, 360) # subsurface for player 1
        display_center(screen, screen_subsurf_1, (left_mid_x, MID_Y))

        if character_chosen_1:
            display_center(screen, green_box_image, (left_mid_x, MID_Y - 69)) # green box

        # player 2 ------------------

        if character_chosen_2:
            pygame.draw.rect(screen, GREEN_SELECTED, (MID_X, 0, MID_X, HEIGHT))
            display_center(screen, green_box_image, (right_mid_x, MID_Y - 69))

        screen_subsurf_2 = selection_surface.subsurface(subsurf_x_2, 0, 320, 360) # subsurface for player 2
        display_center(screen, screen_subsurf_2, (right_mid_x, MID_Y))

        if character_chosen_2:
            display_center(screen, green_box_image, (right_mid_x, MID_Y - 69))
        # copy of surface is made because it's hard to calculate position of yellow circle due to variable number of characters

        # circle for player 1 ----------------------
        circle_surface_copy = circle_surface.copy()
        # yellow circle showing which selection the player is on
        pygame.draw.circle(circle_surface_copy, (255, 237, 46), (circle_radius + circle_spacing * character_index_1, circle_radius), circle_radius)

        display_center(screen, circle_surface_copy, (left_mid_x, MID_Y + 150))

        # circle for player 2 ----------------------
        circle_surface_copy = circle_surface.copy()
        # yellow circle showing which selection the player is on
        pygame.draw.circle(circle_surface_copy, (255, 237, 46), (circle_radius + circle_spacing * character_index_2, circle_radius), circle_radius)

        display_center(screen, circle_surface_copy, (right_mid_x, MID_Y + 150))

        pygame.draw.rect(screen, BLACK, (MID_X - x_offset, 0, 2 * x_offset, HEIGHT))
        # ------------- usual commands -------------
        if key[pygame.K_ESCAPE]:
            final_screen = pygame.display.set_mode(WINDOW_SIZE)
            pygame.quit()
            sys.exit()

        if key[pygame.K_EQUALS]:
            if fullscreen:
                final_screen = pygame.display.set_mode(WINDOW_SIZE)
                fullscreen = False
            else:
                final_screen = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
                fullscreen = True

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        final_screen.blit(pygame.transform.scale(screen, WINDOW_SIZE), (0, 0))

        pygame.display.update()
        fpsclock.tick(fps)

    return character_names[character_index_1], character_names[character_index_2]

def game(character1, character2): # with scaled screen
    global fullscreen

    if fullscreen:
        final_screen = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
    else:
        final_screen = pygame.display.set_mode(WINDOW_SIZE)

    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

    for joystick in joysticks:
        joystick.init()
        print(joystick.get_name())

    player1 = eval(character1 + "(1, \"keyboard\")")
    player2 = eval(character2 + "(2, \"keyboard\")")


    player_names = ["testing_player_1", "europium_god"]

    player1_name_text = Text(player_names[0], "font_10", BLACK, (NAME_X, NAME_Y))
    player2_name_text = Text(player_names[1], "font_10", BLACK, (WIDTH - NAME_X, NAME_Y))

    consecutive_collisions = 0
    # variable to keep track of consecutive_collisions
    # so if there is (2 or more) consecutive_collisions clipping can be prevented

    game_state = "playing"

    '''
    All game states:
    playing - players are battling in a game
    game_over - one players wins and game is over
    '''

    run = True


    while run:
        # ------------- usual commands -------------
        # screen.fill((255, 255, 255))
        screen.fill(BACKGROUND_COLOUR)
        events = pygame.event.get()
        key = pygame.key.get_pressed()

        # ------------- main code start -------------

        pygame.draw.circle(screen, (50, 90, 168), (MID_X, MID_Y), HEIGHT // 2 + 10)
        pygame.draw.circle(screen, (142, 241, 250), (MID_X, MID_Y), HEIGHT // 2)

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

                # swap player dx and dy
                player1.dx, player2.dx = player2.dx, player1.dx
                player1.dy, player2.dy = player2.dy, player1.dy
                '''

                player1.x -= player1.dx
                player1.y -= player1.dy

                player2.x -= player2.dx
                player2.y -= player2.dy

                player1.dx, player2.dx = collision_physics(player1.dx, player1.mass, player2.dx, player2.mass)
                player1.dy, player2.dy = collision_physics(player1.dy, player1.mass, player2.dy, player2.mass)


                consecutive_collisions += 1
            else:
                consecutive_collisions = 0

            player1.update(key, events)
            player2.update(key, events)

            player1.powerup_update(key, player2)
            player2.powerup_update(key, player1)

            # lives is changed in class function
            player1_lose = player1.out_of_bounds()
            player2_lose = player2.out_of_bounds()

            if player1_lose or player2_lose:
                game_state = "game_over"

                if player1_lose:
                    winning_player = 2
                elif player2_lose:
                    winning_player = 1

                game_over_text = MovingText(f"{player_names[winning_player - 1]} WINS!", "font_20", BLACK, (MID_X, MID_Y))
                # -1 to account for 0 index
                # game_over_text = MovingText("LONG LONG LONG LONG TEXT TEST", "font_20", BLACK, (MID_X, MID_Y))
                # game_over_text = MovingText("SHORT", "font_20", BLACK, (MID_X, MID_Y))



        player1_name_text.display_top_left(screen)
        player2_name_text.display_top_right(screen)

        player1.powerup_display(screen)
        player2.powerup_display(screen)

        player1.display(screen)
        player2.display(screen)

        player1.display_lives(screen)
        player2.display_lives(screen)

        if game_state == "game_over":
            game_over_text.display_text(screen)

            if game_over_text.is_finished():
                game_state = "playing"

                player1.reset()
                player2.reset()

        # ------------- usual commands -------------
        if key[pygame.K_ESCAPE]:
            final_screen = pygame.display.set_mode(WINDOW_SIZE)
            pygame.quit()
            sys.exit()

        if key[pygame.K_EQUALS]:
            if fullscreen:
                final_screen = pygame.display.set_mode(WINDOW_SIZE)
                fullscreen = False
            else:
                final_screen = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
                fullscreen = True

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        final_screen.blit(pygame.transform.scale(screen, WINDOW_SIZE), (0, 0))

        pygame.display.update()
        fpsclock.tick(fps)
