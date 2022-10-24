from data.constants import *
from data.functions import *
import json

# Texts
class Text():
    def __init__(self, screen, font_name, colour, coordinates, *optional_text, display_method = "center"):

        self.screen = screen
        self.coordinates = coordinates
        self.colour = colour
        self.display_method = display_method

        self.font = eval(font_name) # get font
        self.font_size = int(font_name.split('_')[1]) # font size from font_name

        if optional_text: # premade text
            text = str(optional_text[0])
            self.generate_text_surf(text)

    def generate_text_surf(self, text): # generates a text surface from the text
        if '\n' in text:
            self.final_text_surface = self.generate_multi_text(text)
        else:
            self.final_text_surface = self.generate_simple_text(text)

    def generate_simple_text(self, text): # get single line text surface
        text_surf = self.font.render(text, False, self.colour)
        return text_surf

    def generate_multi_text(self, text): # get multi line text surface
        lines = list(text.split('\n')) # get each lines of text separated by /n (new line)

        text_surfaces = []

        width, height = 0, 0

        for line in lines: # each line of text
            text_surf = self.font.render(line, False, self.colour)
            text_surfaces.append((text_surf, height))

            width = max(width, text_surf.get_width()) # calculate width of rectangle of text
            height += self.font_size * 1.6 # recommended value for line spacing
            # recommended line break value = font_size times value between 1.4 to 1.8

        height -= self.font_size * 0.6 # remove extra empty space at bottom

        if self.colour != WHITE:
            fill_surf_colour = WHITE
        else:
            fill_surf_colour = BLACK

        final_text_surface = pygame.Surface((width, height)) # surface which contains all the texts
        final_text_surface.fill(fill_surf_colour)

        for text_surf, h in text_surfaces:
            # width // 2 for centering
            # h + half of font size for centering
            display_center(final_text_surface, text_surf, (width // 2, h + self.font_size // 2))

        final_text_surface.set_colorkey(fill_surf_colour)

        return final_text_surface

    def display(self, *optional_text): # display text surface on screen

        if optional_text: # variable text
            text = str(optional_text[0])
            self.generate_text_surf(text)

        if hasattr(self, "final_text_surface"): # check if text surface exists (generated)
            if self.display_method == "center":
                display_center(self.screen, self.final_text_surface, self.coordinates)
            elif self.display_method == "top_left":
                self.screen.blit(self.final_text_surface, self.coordinates)
            elif self.display_method == "top_right":
                self.screen.blit(self.final_text_surface, (self.coordinates[0] - self.final_text_surface.get_width(), self.coordinates[1]))
        else: #raise an error
            assert False

class FadeText(Text):
    def __init__(self, screen, font_name, colour, coordinates, text, total_time, display_method = "center"):
        super().__init__(screen, font_name, colour, coordinates, text, display_method = display_method)
        self.total_time = total_time

    def display(self, *optional_text): # display text surface on screen
        if hasattr(self, "timer"):
            if optional_text: # variable text
                text = str(optional_text[0])
                self.generate_text_surf(text)

            if hasattr(self, "final_text_surface"): # check if text surface exists (generated)
                fade_float = self.timer.time_elapsed() / self.total_time
                self.final_text_surface.set_alpha(255 - (fade_float * 255))

                if self.display_method == "center":
                    display_center(self.screen, self.final_text_surface, self.coordinates)
                elif self.display_method == "top_left":
                    self.screen.blit(self.final_text_surface, self.coordinates)
                elif self.display_method == "top_right":
                    self.screen.blit(self.final_text_surface, (self.coordinates[0] - self.final_text_surface.get_width(), self.coordinates[1]))
            else: #raise an error
                assert False

            if self.timer.time_elapsed() >= self.total_time:
                delattr(self, "timer")

    def start_display(self):
        self.timer = Timer()

class MovingText(Text):
    def __init__(self, screen, font_name, colour, coordinates, text):
        super().__init__(screen, font_name, colour, coordinates, text)

        self.pause_x, self.pause_y = self.coordinates

        self.width = self.final_text_surface.get_width()

        self.x = - self.width // 2
        self.y = self.pause_y

        self.initial_speed = 118

        self.minimum_speed = 2
        self.change_constant = 1.05 #1.2

        n = math.ceil(math.log(1 - (((WIDTH + self.width) / 2) * (1 - self.change_constant)) / self.minimum_speed) / math.log(self.change_constant))

        self.initial_speed = self.minimum_speed * (self.change_constant ** n)

        self.x = WIDTH // 2 - self.minimum_speed * (1 - self.change_constant ** n) / (1 - self.change_constant)

        self.speed = self.initial_speed

        self.done = False # keep tracks of if the text has exited the screen

    def update(self):

        if self.x <= self.pause_x:
            # if self.speed > self.minimum_speed:
            self.speed /= self.change_constant
        else:
            self.speed *= self.change_constant

        self.x += self.speed

        if self.x >= WIDTH + self.width // 2:
            self.done = True
            del self.final_text_surface # to clear up memory
        # self.x += max(self.speed, self.minimum_speed)

    def display(self):

        if not self.done:
            self.update()

        # self.done is only updated here so need two separate if statements
        if not self.done:
            display_center(self.screen, self.final_text_surface, (self.x, self.y))

    def is_finished(self):
        return self.done

# Button
class Button():
    def __init__(self, text_object, rect, colour, responsiveness = 0, border_radius = 0):
        # arguments taken in
        self.text = text_object
        self.screen = text_object.screen


        if not 1 <= len(colour) <= 2:
            assert False # raise error if not 1 or 2 colour given
        else:
            self.colour_list = colour

        self.rect = rect # rect is based on center
        self.border_radius = border_radius

        x, y, width, height = rect

        # when button on text
        self.respond = bool(responsiveness) or len(self.colour_list) > 1

        if self.respond:
            self.on_rect = (x, y, width + responsiveness * 2, height + responsiveness * 2) # rect when mouse is on the button
            self.on_border_radius = border_radius + responsiveness

        # checking mouse on the button
        self.collision_rect = pygame.Rect(x - width // 2, y - height // 2, width, height)

        # button functions
        self.state = False # general state which changes every time the button is clicked

    def display(self, *args):
        if self.respond:
            mouse_pos = args[0]

        # displaying the rectangle
        if self.respond and self.collision_rect.collidepoint(mouse_pos): # mouse is on button
            display_rect = self.on_rect

            if len(self.colour_list) == 2:
                display_colour = self.colour_list[1]
            else:
                display_colour = self.colour_list[0]

            center_draw_rect(self.screen, display_colour, display_rect, self.on_border_radius)
        else:
            center_draw_rect(self.screen, self.colour_list[0], self.rect, self.border_radius)


        if self.respond and len(args) == 2:
            self.text.display(args[1])
        if not self.respond and len(args) == 1:
            self.text.display(args[0])
        else:
            self.text.display()

    def is_clicked(self, events, mouse_pos):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.collision_rect.collidepoint(mouse_pos):
                    self.state = not self.state # change state if button clicked
                    return True
                return False

# Image
class FadeImage():
    def __init__(self, image_): # underscore to not confuse it with the function image
        self.image = get_image(image_)
        self.alpha_value = 255 # 0 is fully transparent, 255 is fully visible (fully opaque)

    def remove(self, fade_speed):
        self.alpha_value -= fade_speed # how much the alpha value decreases fer update
        self.image = self.image.set_alpha(self.alpha_value)

# Time
class Timer():
    def __init__(self):
        self.start_time = time.time()

    def time_elapsed(self):
        return time.time() - self.start_time

    def restart(self):
        self.start_time = time.time()

# States
class AlternatingState():
    def __init__(self, period):
        self.period = period

        self.state = True
        self.prev_key_time = time.time()

    def get_state(self):
        if time.time() - self.prev_key_time >= self.period:
            self.state = not self.state # flip states
            self.prev_key_time += self.period

        return self.state

# Animation
class Animation():
    # playing/characters/Blob
    def __init__(self, length, interval, path, prefix):

        if length == 1:
            self.change = False # boolean to see if character has animation
            self.image = get_image(path + "/" + prefix + ".png")
        else:
            self.change = True

        if self.change:
            self.length = length # total number of frames

            # interval is the number of frames each image (frame) lasts for
            self.speed = 30 / interval # speed at which index increases

            self.frames = [get_image(path + "/" + prefix + str(i + 1) + ".png") for i in range(self.length)]
            self.index = 0

    def current_frame(self):

        if not self.change:
            return self.image

        else:
            image = self.frames[int(self.index)]
            self.index += self.speed
            self.index %= self.length

            return image

# Input

class AdvancedKey():
    def __init__(self, key):
        self.key = key
        self.pressed = False

    def is_pressed(self, keys):
        if keys[self.key] and not self.pressed:
            self.pressed = True
            return True

        if not keys[self.key]:
            self.pressed = False

        return False

# Particle Effects
class ParticleCircle():
    def __init__(self, x, y, angle, speed, radius, decay_rate, colour):
        self.x = x
        self.y = y

        self.dx = angle_move_x(angle, speed)
        self.dy = angle_move_y(angle, speed)

        self.radius = radius
        self.diameter = 2 * radius

        self.decay_rate = decay_rate

        self.colour = colour

    def update(self):
        self.x += self.dx
        self.y += self.dy

        self.radius -= self.decay_rate

    # only for out of screen
    def should_remove(self):
        return (self.radius < 0 or
                self.x < -self.diameter or # checking for out of bounds
                self.x > WIDTH + self.diameter or
                self.y < -self.diameter or
                self.y > HEIGHT + self.diameter)

    def display(self, screen):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.radius)

class ParticleImage(): # for attack weapons
    def __init__(self, x, y, angle, speed, radius, image):
        self.x = x
        self.y = y

        self.dx = angle_move_x(angle, speed)
        self.dy = angle_move_y(angle, speed)

        self.radius = radius

        self.image = image

        self.diameter = self.image.get_width()

    def update(self):
        self.x += self.dx
        self.y += self.dy

    # only for out of screen
    def should_remove(self):
        return (self.collide or # collided with other player
                self.x < -self.diameter or # checking for out of bounds
                self.x > WIDTH + self.diameter or
                self.y < -self.diameter or
                self.y > HEIGHT + self.diameter)

    def display(self, screen):
        display_center(screen, self.image, (int(self.x), int(self.y)))

# gamestate sub functions
class PlayerSelection():
    def __init__(self, player_number, screen, character_names, player_data):
        self.screen = screen
        self.num_characters = len(character_names)
        self.player_data = player_data

        self.selection_surface = self.generate_selection_surface(character_names)
        self.circle_surface = self.generate_circle_surface()
        self.green_box_image = get_image("selection/other/green_box.png")

        self.subsurf_x = 0
        self.subsurf_target_x = 0

        self.character_index = 0
        self.character_chosen = 0

        if player_number == 1:
            # keys
            self.controls = {"left":  AdvancedKey(pygame.K_a),
                            "right":  AdvancedKey(pygame.K_d),
                            "up":     AdvancedKey(pygame.K_w),
                            "down":   AdvancedKey(pygame.K_s),
                            "select": AdvancedKey(pygame.K_e),
                            "enter":  AdvancedKey(pygame.K_RETURN)}

            # coordinates
            self.MID_X = MID_X * 0.5 - X_OFFSET // 2
            self.left_x = 0

            # colours
            self.PLAYER_NAME_COLOUR = PLAYER_BLUE

            # default username
            self.username = "GUEST 1"
        else:
            # keys
            self.controls = {"left":  AdvancedKey(pygame.K_LEFT),
                            "right":  AdvancedKey(pygame.K_RIGHT),
                            "up":     AdvancedKey(pygame.K_UP),
                            "down":   AdvancedKey(pygame.K_DOWN),
                            "select": AdvancedKey(pygame.K_SLASH),
                            "enter":  AdvancedKey(pygame.K_RETURN)}

            # coordinates
            self.MID_X = MID_X * 1.5 + X_OFFSET // 2
            self.left_x = MID_X

            # colours
            self.PLAYER_NAME_COLOUR = PLAYER_RED

            # default username
            self.username = "GUEST 2"

        self.login_button = Button(
                            Text(self.screen, "FONT_7", BLACK, (self.MID_X + BUTTON_OFFSET, BUTTON_Y), "log in"),
                            (self.MID_X + BUTTON_OFFSET, BUTTON_Y, 56, BUTTON_HEIGHT),
                            [PLAYER_BLUE, MID_BLUE],
                            responsiveness = 1,
                            border_radius = BUTTON_BORDER_RADIUS
                            )

        self.signup_button = Button(
                            Text(self.screen, "FONT_7", BLACK, (self.MID_X + BUTTON_OFFSET + BUTTON_SPACING, BUTTON_Y), "sign up"),
                            (self.MID_X + BUTTON_OFFSET + BUTTON_SPACING, BUTTON_Y, 62, BUTTON_HEIGHT),
                            [PLAYER_BLUE, MID_BLUE],
                            responsiveness = 1,
                            border_radius = BUTTON_BORDER_RADIUS
                            )

        self.navigation = "cards"
        '''
        stores where the player currently is on / clicks on
        "cards" - choosing character cards
        "login" - login button
        "signin" - signin button
        "input" - user keying in username / password in login or signin page
        '''

        self.state = "cards"
        '''
        stores what the player is currently doing
        "cards" - choosing cards
        "login, username" - keying username in login page
        "login, password" - keying password in login page
        "signup, username" - keying username in signup page
        "signup, password" - keying password in signup page
        '''

        # username and password
        # mask used to grey out the entire screen during authentication

        self.signup_title = Text(self.screen, "FONT_10", SILVER, (self.MID_X, TITLE_Y), "SIGN UP")
        self.login_title = Text(self.screen, "FONT_10", SILVER, (self.MID_X, TITLE_Y), "LOG IN")

        self.screen_mask = pygame.Surface((MID_X, HEIGHT), pygame.SRCALPHA)
        self.screen_mask.fill((54, 62, 79, 200))

        self.username_string = ""
        self.password_string = ""

        self.username_text = Text(self.screen, "FONT_7", BLACK, (self.MID_X, USERNAME_Y), self.username_string)
        self.password_text = Text(self.screen, "FONT_7", BLACK, (self.MID_X, PASSWORD_Y), self.password_string)

        self.username_heading = Text(self.screen, "FONT_7", SILVER, (self.MID_X, USERNAME_Y - HEADING_OFFSET), "USERNAME:")
        self.password_heading = Text(self.screen, "FONT_7", SILVER, (self.MID_X, PASSWORD_Y - HEADING_OFFSET), "PASSWORD:")

        self.logged_in = False

        self.INCORRECT_DISPLAY_TIME = 3.3

        self.incorrect_username_text = FadeText(self.screen, "FONT_7", PLAYER_RED, (self.MID_X, INCORRECT_TEXT_Y), "Username not found.\nPlease try again.", self.INCORRECT_DISPLAY_TIME)
        self.incorrect_password_text = FadeText(self.screen, "FONT_7", PLAYER_RED, (self.MID_X, INCORRECT_TEXT_Y), "Incorrect password.\nPlease try again.", self.INCORRECT_DISPLAY_TIME)

        self.correct_username_text = FadeText(self.screen, "FONT_7", AUTHENTICATE_GREEN, (self.MID_X, INCORRECT_TEXT_Y), "User found!", self.INCORRECT_DISPLAY_TIME)
        self.correct_password_text = FadeText(self.screen, "FONT_10", AUTHENTICATE_GREEN, (self.MID_X, 100), "Log in\nsuccessful!", self.INCORRECT_DISPLAY_TIME)

        self.account_exists_text = FadeText(self.screen, "FONT_7", PLAYER_RED, (self.MID_X, INCORRECT_TEXT_Y), "Account\nalready exists!", self.INCORRECT_DISPLAY_TIME)
        self.signin_text = FadeText(self.screen, "FONT_10", AUTHENTICATE_GREEN, (self.MID_X, 100), "Account\ncreated!", self.INCORRECT_DISPLAY_TIME)

        # text which shows waiting for other player to key in username / password
        self.waiting_text = Text(self.screen, "FONT_10", SILVER, (self.MID_X, MID_Y), "WAITING FOR\nOTHER\nPLAYER")

        # colour (flashing colour)
        self.prev_flash_time = time.time()
        self.flash_frequency = 3

        # cursor
        self.cursor_state = AlternatingState(0.7)

        # button
        self.center_x = self.MID_X + 65
        self.center_y = 50
        self.x_button_radius = 13
        self.on_x_button = False

    def generate_selection_surface(self, character_names):
        character_images = [get_image("playing/characters/" + i + "/character.png") for i in character_names]
        character_powerup_images = [get_image("playing/characters/" + i + "/icon.png") for i in character_names]

        selection_surface = pygame.Surface((SPACING_X * (self.num_characters - 1) + MID_X, HEIGHT))

        selection_surface.fill(INTERMEDIATE_COLORKEY)

        position_x = MID_X // 2
        position_y = MID_Y

        for i in range(self.num_characters):
            card_image = get_image("selection/cards/card_" + character_names[i] + ".png")
            character_name_surf = Text(selection_surface, "FONT_10", SILVER, (position_x, position_y - 115), character_names[i])

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

        return selection_surface

    def generate_circle_surface(self):
        circle_surface = pygame.Surface((CIRCLE_SPACING * (self.num_characters - 1) + CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2))
        circle_surface.set_colorkey(BLACK)

        position_x = CIRCLE_RADIUS
        position_y = CIRCLE_RADIUS

        for i in range(self.num_characters):
            pygame.draw.circle(circle_surface, (148, 148, 148), (position_x, position_y), CIRCLE_RADIUS)
            position_x += CIRCLE_SPACING

        return circle_surface

    def get_flash_colour(self):
        time_passed = time.time() - self.prev_flash_time
        colour = pygame.Color(YELLOW).lerp(pygame.Color(WHITE), (time_passed % self.flash_frequency) / self.flash_frequency)

        if time_passed >= self.flash_frequency:
            self.prev_flash_time = time.time()

        return colour

    def input_update(self, keys, events, mouse_pos):

        if self.navigation == "cards":
            if not self.character_chosen:
                if self.controls["right"].is_pressed(keys):
                    self.character_index += 1

                if self.controls["left"].is_pressed(keys):
                    self.character_index -= 1

            if self.controls["select"].is_pressed(keys):
                self.character_chosen = not self.character_chosen

            self.character_index %= self.num_characters

            if self.controls["up"].is_pressed(keys):
                self.navigation = "login"

        elif self.navigation == "login":
            if self.controls["right"].is_pressed(keys):
                self.navigation = "signup"

            if self.controls["down"].is_pressed(keys):
                self.navigation = "cards"

            if self.controls["select"].is_pressed(keys):
                self.navigation = "input"
                self.state = "login, username"

        elif self.navigation == "signup":
            if self.controls["left"].is_pressed(keys):
                self.navigation = "login"

            if self.controls["down"].is_pressed(keys):
                self.navigation = "cards"

            if self.controls["select"].is_pressed(keys):
                self.navigation = "input"
                self.state = "signup, username"

        elif self.navigation == "input":

            if self.state == "login, username":
                if self.controls["enter"].is_pressed(keys):
                    if self.username_string in self.player_data.keys():
                        self.correct_username_text.start_display()
                        self.state = "login, password"
                    else:
                        self.incorrect_username_text.start_display()
                else:
                    if keys[pygame.K_BACKSPACE]:
                        self.username_string = self.username_string[:-1]

                    for event in events:
                        if event.type == pygame.KEYDOWN:
                            self.username_string += event.unicode

            elif self.state == "login, password":
                if self.controls["enter"].is_pressed(keys):
                    if self.password_string == self.player_data[self.username_string]["password"]:
                        self.correct_password_text.start_display()

                        self.state = "cards"
                        self.navigation = "cards"

                        self.logged_in = True

                        self.username = self.username_string # confirmed username
                        self.player_name_text = Text(self.screen, "FONT_10", WHITE, (self.MID_X, 25), self.username)
                    else:
                        self.incorrect_password_text.start_display()
                else:
                    if keys[pygame.K_BACKSPACE]:
                        self.password_string = self.password_string[:-1]

                    for event in events:
                        if event.type == pygame.KEYDOWN:
                            self.password_string += event.unicode

            elif self.state == "signup, username":
                if self.controls["enter"].is_pressed(keys):
                    if self.username_string in self.player_data.keys():
                        self.account_exists_text.start_display()
                    else:
                        self.state = "signup, password"
                else:
                    if keys[pygame.K_BACKSPACE]:
                        self.username_string = self.username_string[:-1]

                    for event in events:
                        if event.type == pygame.KEYDOWN:
                            self.username_string += event.unicode

            elif self.state == "signup, password":
                if self.controls["enter"].is_pressed(keys):
                    self.signin_text.start_display()

                    self.state = "cards"
                    self.navigation = "cards"

                    self.logged_in = True

                    self.username = self.username_string # confirmed username
                    self.player_name_text = Text(self.screen, "FONT_10", WHITE, (self.MID_X, 25), self.username)

                    self.player_data[self.username] =  {"password": self.password_string,
                                                        "games_played": 0}

                    with open('data/player_data.json', 'w') as f:
                        json.dump(self.player_data, f, indent = 4)

                else:
                    if keys[pygame.K_BACKSPACE]:
                        self.password_string = self.password_string[:-1]

                    for event in events:
                        if event.type == pygame.KEYDOWN:
                            self.password_string += event.unicode

        if self.login_button.is_clicked(events, mouse_pos):
            self.navigation = "input"
            self.state = "login, username"

        elif self.signup_button.is_clicked(events, mouse_pos):
            self.navigation = "input"
            self.state = "signup, username"

        if self.navigation == "input":
            if math.sqrt((mouse_pos[0] - self.center_x) ** 2 + (mouse_pos[1] - self.center_y) ** 2) <= self.x_button_radius:
                self.on_x_button = True
            else:
                self.on_x_button = False

            if self.on_x_button:
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.navigation = "cards"
                        self.state = "cards"

    def scroll(self):
        # updating target x position
        self.subsurf_target_x = SPACING_X * self.character_index

        # scrolling
        if self.subsurf_x < self.subsurf_target_x:
            self.subsurf_x += SCROLL_SPEED
            self.subsurf_x = min(self.subsurf_x, self.subsurf_target_x)

        if self.subsurf_x > self.subsurf_target_x:
            self.subsurf_x -= SCROLL_SPEED
            self.subsurf_x = max(self.subsurf_x, self.subsurf_target_x)

    def cards_display(self):
        if self.character_chosen:
            pygame.draw.rect(self.screen, GREEN_SELECTED, (self.left_x, 0, MID_X, HEIGHT)) # green background

        screen_subsurf = self.selection_surface.subsurface(self.subsurf_x, 0, 320, 360) # subsurface for player 1

        display_surf = pygame.Surface((320, 360))
        display_surf.fill(INTERMEDIATE_COLORKEY)
        display_surf.set_colorkey(INTERMEDIATE_COLORKEY)

        # yellow highlight rectangle
        if self.navigation == "cards":
            center_draw_rect(display_surf, self.get_flash_colour(), ((self.subsurf_target_x - self.subsurf_x) % SPACING_X + MID_X // 2, MID_Y, 214, 274), 20)

        # card surf
        display_surf.blit(screen_subsurf, (0, 0))

        display_center(self.screen, display_surf, (self.MID_X, MID_Y))

        if self.character_chosen:
            display_center(self.screen, self.green_box_image, (self.MID_X, MID_Y - 69))

    def selection_circle_display(self):
        # copy of surface must be made to prevent multiple circles being yellow at the same time
        circle_surface_copy = self.circle_surface.copy()

        # yellow circle showing which selection the player is on
        pygame.draw.circle(circle_surface_copy, (255, 237, 46), (CIRCLE_RADIUS + CIRCLE_SPACING * self.character_index, CIRCLE_RADIUS), CIRCLE_RADIUS)

        display_center(self.screen, circle_surface_copy, (self.MID_X, MID_Y + 150))

    def button_display(self, mouse_pos):
        if not self.logged_in:

            if self.navigation == "login":
                center_draw_rect(self.screen, self.get_flash_colour(), (self.MID_X + BUTTON_OFFSET, BUTTON_Y, 60, BUTTON_HEIGHT + 4), BUTTON_BORDER_RADIUS)
            elif self.navigation == "signup":
                center_draw_rect(self.screen, self.get_flash_colour(), (self.MID_X + BUTTON_OFFSET + BUTTON_SPACING, BUTTON_Y, 66, BUTTON_HEIGHT + 4), BUTTON_BORDER_RADIUS)

            self.login_button.display(mouse_pos)
            self.signup_button.display(mouse_pos)


    def authentication_display(self):
        if self.navigation == "input":

            # displaying grey mask
            display_center(self.screen, self.screen_mask, (self.MID_X, MID_Y))

            # username part
            self.username_heading.display()

            if self.state == "login, password": # green outline for correct username
                center_draw_rect(self.screen, AUTHENTICATE_GREEN, (self.MID_X, USERNAME_Y, 104, 24), border_radius = 10)

            center_draw_rect(self.screen, WHITE, (self.MID_X, USERNAME_Y, 100, 20), border_radius = 10)
            self.username_text.display(self.username_string)

            # password part
            self.password_heading.display()
            center_draw_rect(self.screen, WHITE, (self.MID_X, PASSWORD_Y, 100, 20), border_radius = 10)
            self.password_text.display("*" * len(self.password_string))

            # title_rect
            center_draw_rect(self.screen, BLACK, (self.MID_X, TITLE_Y, 100, 30), border_radius = 10)

            if self.state == "login, username" or self.state == "login, password":
                self.login_title.display()
            elif self.state == "signup, username" or self.state == "signup, password":
                self.signup_title.display()

            # cursor and title
            if self.cursor_state.get_state():
                if self.state == "login, username" or self.state == "signup, username":
                    center_draw_rect(self.screen, BLACK, (self.MID_X + self.username_text.final_text_surface.get_width() // 2, USERNAME_Y, 1, 10))

                elif self.state == "login, password" or self.state == "signup, password":
                    center_draw_rect(self.screen, BLACK, (self.MID_X + self.password_text.final_text_surface.get_width() // 2, PASSWORD_Y, 1, 10))

            # incorrect handling - please try again texts
            # for log in
            self.incorrect_username_text.display()
            self.incorrect_password_text.display()

            # for sign in
            self.account_exists_text.display()

            # correct handling - username found
            self.correct_username_text.display()

            # quit circle
            if not self.on_x_button:
                pygame.draw.circle(self.screen, PLAYER_RED, (self.center_x, self.center_y), self.x_button_radius)
                cross_len = 5
            else:
                pygame.draw.circle(self.screen, (240, 79, 119), (self.center_x, self.center_y), self.x_button_radius + 1)
                cross_len = 6

            pygame.draw.line(self.screen, WHITE, (self.center_x - cross_len, self.center_y - cross_len), (self.center_x + cross_len, self.center_y + cross_len), width = 5)
            pygame.draw.line(self.screen, WHITE, (self.center_x - cross_len, self.center_y + cross_len), (self.center_x + cross_len, self.center_y - cross_len), width = 5)

        elif self.logged_in:
            center_draw_rect(self.screen, self.PLAYER_NAME_COLOUR, (self.MID_X, PLAYER_NAME_Y, 120, 20), border_radius = 10)
            self.player_name_text.display()

            # correct handling - password found
            self.correct_password_text.display()
            self.signin_text.display()

    def waiting_display(self):
        # displaying grey mask
        display_center(self.screen, self.screen_mask, (self.MID_X, MID_Y))

        # displaying waiting text
        self.waiting_text.display()
