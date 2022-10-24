'''

    def character_selection(self):
        # common settings
        last_time = time.time()
        screen_key = AdvancedKey(pygame.K_EQUALS)

        # getting character information
        character_names = ["GroundHog", "B79", "Jian", "Volta", "Metor"]
        character_images = [get_image("playing/characters/" + i + "/character.png") for i in character_names]
        character_powerup_images = [get_image("playing/characters/" + i + "/icon.png") for i in character_names]
        num_characters = len(character_names)

        character_ready = {
            "GroundHog" : True,
            "B79": False,
            "Jian": True,
            "Volta": False,
            "Metor": False
        }

        # definining images and constants
        green_box_image = get_image("selection/other/green_box.png")

        X_OFFSET = 10 # x value offset from the middle

        SPACING_X = 300 # spacing between characters

        left_mid_x = MID_X * 0.5 - X_OFFSET # midline for left player self.screen
        right_mid_x = MID_X * 1.5 + X_OFFSET

        # selection_surface rendering ---------------------------
        selection_surface = pygame.Surface((SPACING_X * (num_characters - 1) + MID_X, HEIGHT))

        INTERMEDIATE_COLORKEY = (255, 0, 242)
        selection_surface.fill(INTERMEDIATE_COLORKEY)

        position_x = MID_X // 2
        position_y = MID_Y

        for i in range(num_characters):
            card_image = get_image("selection/cards/card_" + character_names[i] + ".png")
            character_name_surf = Text(selection_surface, "font_10", SILVER, (position_x, position_y - 115), character_names[i])

            display_center(selection_surface, card_image, (position_x, position_y)) # card background
            display_center(selection_surface, character_images[i], (position_x, position_y - 69)) # character image
            display_center(selection_surface, character_powerup_images[i], (position_x - 48, position_y + 14)) # powerup icon

            character_name_surf.display()

            if OS == "Windows":
                if not character_ready[character_names[i]]:
                    # grey mask
                    coming_soon_mask = pygame.mask.from_surface(card_image)
                    coming_soon_mask = coming_soon_mask.to_surface(unsetcolor = (0, 0, 0, 0), setcolor = (82, 81, 89, 190))
                    display_center(selection_surface, coming_soon_mask, (position_x, position_y))

                    # text
                    coming_soon_text = Text(selection_surface, "font_10", WHITE, (position_x, position_y - 28), "COMING SOON")
                    coming_soon_text.display()

            position_x += SPACING_X


        selection_surface.set_colorkey(INTERMEDIATE_COLORKEY)
        #-------------------------------------------------------


        # circle_surface rendering---------------------------
        circle_surface = pygame.Surface((CIRCLE_SPACING * (num_characters - 1) + CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2))
        circle_surface.set_colorkey(BLACK)

        position_x = CIRCLE_RADIUS
        position_y = CIRCLE_RADIUS

        for i in range(num_characters):
            pygame.draw.circle(circle_surface, (148, 148, 148), (position_x, position_y), CIRCLE_RADIUS)
            position_x += CIRCLE_SPACING
        #-------------------------------------------------------

        subsurf_x1 = 0
        subsurf_target_x1 = 0

        subsurf_x2 = 0
        subsurf_target_x2 = 0

        SCROLL_SPEED = 15

        key_E = AdvancedKey(pygame.K_e)
        key_D = AdvancedKey(pygame.K_d)
        key_A = AdvancedKey(pygame.K_a)

        key_slash = AdvancedKey(pygame.K_SLASH)
        key_right = AdvancedKey(pygame.K_RIGHT)
        key_left = AdvancedKey(pygame.K_LEFT)

        character_index1 = 0 # character index for player 1
        character_index2 = 0 # character index for player 2

        character_chosen_1 = False
        character_chosen_2 = False

        end_timer_started = False

        while True:
            # ------------- usual commands -------------
            dt, events, keys, last_time, mouse_pos = self.settings_before(BACKGROUND_COLOUR, last_time)

            # ------------- main code start -------------

            # key handling for both players

            if not character_chosen_1:
                if key_D.is_pressed(keys):
                    character_index1 += 1

                if key_A.is_pressed(keys):
                    character_index1 -= 1

            if key_E.is_pressed(keys):
                character_chosen_1 = not character_chosen_1

            if not character_chosen_2:
                if key_right.is_pressed(keys):
                    character_index2 += 1

                if key_left.is_pressed(keys):
                    character_index2 -= 1

            if key_slash.is_pressed(keys):
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
                break

            # updating target x positions for both players
            subsurf_target_x1 = SPACING_X * character_index1
            subsurf_target_x2 = SPACING_X * character_index2

            # player 1 scrolling
            if subsurf_x1 < subsurf_target_x1:
                subsurf_x1 += SCROLL_SPEED
                subsurf_x1 = min(subsurf_x1, subsurf_target_x1)

            if subsurf_x1 > subsurf_target_x1:
                subsurf_x1 -= SCROLL_SPEED
                subsurf_x1 = max(subsurf_x1, subsurf_target_x1)

            # player 2 scrolling
            if subsurf_x2 < subsurf_target_x2:
                subsurf_x2 += SCROLL_SPEED
                subsurf_x2 = min(subsurf_x2, subsurf_target_x2)

            if subsurf_x2 > subsurf_target_x2:
                subsurf_x2 -= SCROLL_SPEED
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

            screen_subsurf_2 = selection_surface.subsurface(subsurf_x2, 0, 320, 360) # subsurface for player 2
            display_center(self.screen, screen_subsurf_2, (right_mid_x, MID_Y))

            if character_chosen_2:
                display_center(self.screen, green_box_image, (right_mid_x, MID_Y - 69))
            # copy of surface is made because it's hard to calculate position of yellow circle due to variable number of characters

            # circle for player 1 ----------------------
            circle_surface_copy = circle_surface.copy()

            # yellow circle showing which selection the player is on
            pygame.draw.circle(circle_surface_copy, (255, 237, 46), (CIRCLE_RADIUS + CIRCLE_SPACING * character_index1, CIRCLE_RADIUS), CIRCLE_RADIUS)

            display_center(self.screen, circle_surface_copy, (left_mid_x, MID_Y + 150))

            # circle for player 2 ----------------------
            circle_surface_copy = circle_surface.copy()
            # yellow circle showing which selection the player is on
            pygame.draw.circle(circle_surface_copy, (255, 237, 46), (CIRCLE_RADIUS + CIRCLE_SPACING * character_index2, CIRCLE_RADIUS), CIRCLE_RADIUS)

            display_center(self.screen, circle_surface_copy, (right_mid_x, MID_Y + 150))

            # black separator
            pygame.draw.rect(self.screen, BLACK, (MID_X - X_OFFSET, 0, 2 * X_OFFSET, HEIGHT))

            # ------------- usual commands -------------
            self.settings_after(events, keys, screen_key)

        return character_names[character_index1], character_names[character_index2]

'''

'''
# key input detected WHEN released
class PressKey():
    def __init__(self, target_key):
        self.press = False
        self.target_key = target_key

    def use_function(self, key):
        if key[self.target_key]:
            self.press = True
        else:
            if self.press:
                # self.key_function()
                self.press = False
                return True

        return False
'''

'''
class Text():
    def __init__(self, text, font_name, colour, coordinates):
        font = eval(font_name)
        font_size = int(font_name.split('_')[1])
        lines = list(text.split('\n'))

        self.coordinates = coordinates

        self.text_surfaces = []

        self.width, self.height = 0, 0

        for line in lines:
            text = font.render(line, False, colour)
            self.text_surfaces.append((text, self.height))

            self.width = max(self.width, text.get_width())
            self.height += font_size * 1.6

        self.height -= font_size * 0.6 # remove extra empty space at bottom

        if colour != WHITE:
            fill_surf_colour = WHITE
        else:
            fill_surf_colour = BLACK

        self.final_text_surface = pygame.Surface((self.width, self.height)) # surface which contains all the texts
        self.final_text_surface.fill(fill_surf_colour)

        for text, h in self.text_surfaces:
            # width // 2 for centering
            # h + half of font size for centering
            display_center(self.final_text_surface, text, (self.width // 2, h + font_size // 2))
            # recommended line break value font_size timesvalue between 1.4 to 1.8

        self.final_text_surface.set_colorkey(fill_surf_colour)

    def display_text(self, screen):
        display_center(screen, self.final_text_surface, self.coordinates)

    def display_top_left(self, screen):
        screen.blit(self.final_text_surface, self.coordinates)

    def display_top_right(self, screen):
        screen.blit(self.final_text_surface, (self.coordinates[0] - self.width, self.coordinates[1]))
'''

'''
if self.powerup_state == "charging":
    display_center(screen, self.full_charge, (self.powerup_x, self.powerup_y))
    display_center(screen, self.powerup_shade_right, (self.powerup_x, self.powerup_y)) # turning shade

    if self.powerup_charge > 180:
        display_center(screen, self.half_charge, (self.powerup_x, self.powerup_y))
    else:
        display_center(screen, self.powerup_shade_left, (self.powerup_x, self.powerup_y))
else:
    pygame.draw.circle(screen, (0, 255, 0), (self.powerup_x, self.powerup_y), 25)
display_center(screen, self.powerup_image, (self.powerup_x, self.powerup_y))
'''
'''
def powerup_update(self, key, other_player):

    if self.powerup_state == "charging":
        self.powerup_charge += self.powerup_charge_rate

        if self.powerup_charge > 360:
            self.powerup_charge = 360
            self.powerup_state = "ready"

        self.powerup_half_charge_rotate = pygame.transform.rotate(self.powerup_half_charge_rotate_org, self.powerup_charge)

    elif self.powerup_state == "ready" and key[self.controls["powerup"]]:
        self.powerup_state = "in use"

    # not elif, need the use image immediately after state changes to in use
    if self.powerup_state == "in use":
        self.powerup_charge -= self.powerup_use_rate

        if self.powerup_charge < 0:
            self.powerup_charge = 0
            self.powerup_state = "charging"

        self.powerup_half_use_rotate = pygame.transform.rotate(self.powerup_half_use_rotate_org, self.powerup_charge)
'''
'''
class Standard():
    # def __init__(self, path, player_image, player_number, controller_type, powerup_charge_time, powerup_use_time, *animation):
    def __init__(self, player_number, controller_type, *animation):
        self.character_init() # only in specific character classess

        if len(animation) != 0:
            self.animate = True
        else:
            self.animate = False
        # org_image / animations initialised in specific character class

        self.dx = 0
        self.dy = 0

        self.acceleration = 0.15
        self.deceleration = 0.15

        self.radius = 16 # radius for collision detection
        self.mass = 1 # mass for collision formula

        self.controller_type = controller_type

        self.lives = 3
        self.heart_image = image("playing/other/heart.png")

        if self.controller_type == "joystick":
            self.latest_x_event = 0
            self.latest_y_event = 0

        if player_number == 1:
            self.org_x = MID_X - START_POSITION_X_OFFSET
            self.org_y = MID_Y
            self.angle = -90

            if self.controller_type == "keyboard":
                self.controls = {"left": pygame.K_a, "right": pygame.K_d, "up": pygame.K_w, "down": pygame.K_s, "powerup": pygame.K_e}

            self.powerup_x, self.powerup_y = POWERUP_X, POWERUP_Y # coordinates of powerup

            self.lives_x, self.lives_y = LIVES_X, LIVES_Y # coordiantes of first heart shape
            self.lives_spacing = LIVES_SPACING # distance apart for heart shapes

        elif player_number == 2:
            self.org_x = MID_X + START_POSITION_X_OFFSET
            self.org_y = MID_Y
            self.angle = 90

            if self.controller_type == "keyboard":
                self.controls = {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP, "down": pygame.K_DOWN, "powerup": pygame.K_SLASH}

            self.powerup_x, self.powerup_y = WIDTH - POWERUP_X, POWERUP_Y

            self.lives_x, self.lives_y = WIDTH - LIVES_X, LIVES_Y # coordiantes of first heart shape
            self.lives_spacing = -LIVES_SPACING # distance apart for heart shapes

        self.x = self.org_x
        self.y = self.org_y

        # power up section
        self.powerup_state = "charging"
        self.powerup_charge = 0 # how much the powerup is charged out of 360 (degrees)

        # powerup charge time initialised in specific character class
        self.powerup_charge_rate = 360 / (self.powerup_charge_time * 30) # 30 is fps

        # powerup use time initialised in specific character class
        self.powerup_use_rate = 360 / (self.powerup_use_time * 30)

        self.powerup_shade_left = image("playing/powerup_template/semi_left.png") # reflection over y axis

        self.powerup_half_charge_right_org = image("playing/powerup_template/half_charge.png")
        self.powerup_half_charge_rotate_org = pygame.transform.flip(self.powerup_half_charge_right_org, 1, 0) # begins as left semicricle

        self.powerup_half_use_right_org = palette_swap(self.powerup_half_charge_right_org, (77, 155, 230), POWERUP_USE_COLOUR)
        self.powerup_half_use_rotate_org = palette_swap(self.powerup_half_charge_rotate_org, (77, 155, 230), POWERUP_USE_COLOUR)

        self.powerup_base = image("playing/powerup_template/powerup_base.png")
        self.powerup_top = image("playing/powerup_template/powerup_top.png")

        # powerup icon initialised in specific character class
    def update(self, key, events):

        if self.controller_type == "keyboard":
            # x and y movement
            if key[self.controls["left"]]:
                self.dx -= self.acceleration
            elif key[self.controls["right"]]:
                self.dx += self.acceleration
            else:
                temp_dx = self.dx - sgn(self.dx) * self.deceleration
                if sgn(self.dx) != sgn(temp_dx):
                    self.dx = 0
                else:
                    self.dx = temp_dx

            if key[self.controls["up"]]:
                self.dy -= self.acceleration
            elif key[self.controls["down"]]:
                self.dy += self.acceleration
            else:
                temp_dy = self.dy - sgn(self.dy) * self.deceleration
                if sgn(self.dy) != sgn(temp_dy):
                    self.dy = 0
                else:
                    self.dy = temp_dy

            self.x += self.dx
            self.y += self.dy

        elif self.controller_type == "joystick":

            for event in events:
                if event.type == JOYAXISMOTION:
                    if event.axis < 2:
                        if event.axis == 0:
                            # self.dx += event.value * 0.7
                            # move_x = True
                            self.latest_x_event = event.value * self.acceleration
                        elif event.axis == 1:
                            # self.dy += event.value * 0.7
                            # move_y = True
                            self.latest_y_event = event.value * self.acceleration

            self.dx += self.latest_x_event
            self.dy += self.latest_y_event

            if abs(self.latest_x_event) < 0.02:
                temp_dx = self.dx - sgn(self.dx) * self.deceleration
                if sgn(self.dx) != sgn(temp_dx):
                    self.dx = 0
                else:
                    self.dx = temp_dx


            if abs(self.latest_y_event) < 0.02:
                temp_dy = self.dy - sgn(self.dy) * self.deceleration
                if sgn(self.dy) != sgn(temp_dy):
                    self.dy = 0
                else:
                    self.dy = temp_dy

            self.x += self.dx
            self.y += self.dy

        # angle calculation
        if self.dx == 0:
            if self.dy < 0:
                self.angle = 0
            elif self.dy > 0:
                self.angle = 180
        elif self.dy == 0:
            if self.dx < 0:
                self.angle = 90 #90 counterclockwise
            if self.dx > 0:
                self.angle = -90 #90 clockwise
        else:
            self.angle =  math.degrees(math.atan(self.dx / self.dy))

            if self.dy > 0:
                self.angle += 180

        # updating image
        # 180 is acts as flipping the image since the image points down when uploading
        if self.animate:
            self.image = pygame.transform.rotate(self.idle_animation.current_frame(), self.angle + 180) # counter clockwise rotation
        else:
            self.image = pygame.transform.rotate(self.org_image, self.angle + 180)

    def display(self, screen):
        display_center(screen, self.image, (self.x, self.y))

    def reset(self):
        self.powerup_reset()

        self.x = self.org_x
        self.y = self.org_y

        self.dx = 0
        self.dy = 0


    def out_of_bounds(self):
        arena_radius = HEIGHT // 2

        if (MID_X - self.x) ** 2 + (MID_Y - self.y) ** 2 > (arena_radius - self.radius) ** 2: # check collision with side
            self.lives -= 1
            return True
        return False

    # two sub functions on powerup for better code organisation
    def powerup_update_charge(self):
        self.powerup_charge += self.powerup_charge_rate

        if self.powerup_charge > 360:
            self.powerup_charge = 360
            self.powerup_state = "ready"

        self.powerup_half_charge_rotate = pygame.transform.rotate(self.powerup_half_charge_rotate_org, self.powerup_charge)

    def powerup_reset(self):
        if self.powerup_state == "in use":
            self.powerup_state = "charging"
            self.powerup_charge = 0

    def powerup_update_in_use(self):
        self.powerup_charge -= self.powerup_use_rate

        if self.powerup_charge < 0:
            self.powerup_charge = 0
            self.powerup_state = "charging"
            self.powerup_reset()

        self.powerup_half_use_rotate = pygame.transform.rotate(self.powerup_half_use_rotate_org, self.powerup_charge)

    # final function combining powerup_update sub functions
    def powerup_update(self, key, other_player):
        if self.powerup_state == "charging":
            self.powerup_update_charge()

        elif self.powerup_state == "ready" and key[self.controls["powerup"]]:
            self.powerup_state = "in use"

        # not elif, need the use image immediately after state changes to in use
        if self.powerup_state == "in use":
            self.powerup_update_in_use()

    def powerup_update(self, key, other_player):
        if self.powerup_state == "charging":
            self.powerup_update_charge()

        elif self.powerup_state == "ready" and key[self.controls["powerup"]]:
            self.powerup_state = "in use"

        # not elif, need the use image immediately after state changes to in use
        if self.powerup_state == "in use":
            self.powerup_update_in_use()


    def powerup_display(self, screen):

        if self.powerup_state == "charging":
            display_center(screen, self.powerup_base, (self.powerup_x, self.powerup_y))
            display_center(screen, self.powerup_half_charge_rotate, (self.powerup_x, self.powerup_y))

            if self.powerup_charge < 180:
                display_center(screen, self.powerup_shade_left, (self.powerup_x, self.powerup_y))
            else:
                display_center(screen, self.powerup_half_charge_right_org, (self.powerup_x, self.powerup_y))

        elif self.powerup_state == "in use":
            display_center(screen, self.powerup_base, (self.powerup_x, self.powerup_y))
            display_center(screen, self.powerup_half_use_rotate, (self.powerup_x, self.powerup_y))

            if self.powerup_charge < 180:
                display_center(screen, self.powerup_shade_left, (self.powerup_x, self.powerup_y))
            else:
                display_center(screen, self.powerup_half_use_right_org, (self.powerup_x, self.powerup_y))

        elif self.powerup_state == "ready":
            pygame.draw.circle(screen, POWERUP_READY_COLOUR, (self.powerup_x, self.powerup_y), 26)


        display_center(screen, self.powerup_top, (self.powerup_x, self.powerup_y))
        display_center(screen, self.powerup_icon, (self.powerup_x, self.powerup_y))

    def display_lives(self, screen):
        for i in range(self.lives):
            display_center(screen, self.heart_image, (self.lives_x + self.lives_spacing * i, self.lives_y))
'''
