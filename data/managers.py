from data.constants import *
from data.functions import *

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

class FadeImage():
    def __init__(self, image_): # underscore to not confuse it with the function image
        self.image = image(image_)
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

# Animation
class Animation():
    # playing/characters/Blob
    def __init__(self, length, interval, path, prefix):

        if length == 1:
            self.change = False # boolean to see if character has animation
            self.image = image(path + "/" + prefix + ".png")
        else:
            self.change = True

        if self.change:
            self.length = length # total number of frames

            # interval is the number of frames each image (frame) lasts for
            self.speed = 30 / interval # speed at which index increases

            self.frames = [image(path + "/" + prefix + str(i + 1) + ".png") for i in range(self.length)]
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
        return (self.radius < 0 or # collided with other player
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
