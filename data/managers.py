from data.constants import *
from data.functions import *

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

class MovingText(Text):
    def __init__(self, text, font_name, colour, coordinates):
        super().__init__(text, font_name, colour, coordinates)


        self.pause_x, self.pause_y = self.coordinates

        self.x = - self.width // 2
        self.y = self.pause_y

        self.initial_speed = 118

        self.minimum_speed = 2
        self.change_constant = 1.05 #1.2

        n = math.ceil(math.log(1 - (((WIDTH + self.width) / 2)*(1 - self.change_constant)) / self.minimum_speed) / math.log(self.change_constant))

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
            del self.final_text_surface # to clean up memory
        # self.x += max(self.speed, self.minimum_speed)

    def display_text(self, screen):

        if not self.done:
            self.update()

        # self.done is only updated here so need two separate if statements

        if not self.done:
            display_center(screen, self.final_text_surface, (self.x, self.y))

    def is_finished(self):
        return self.done

class FadeImage():
    def __init__(self, image_): # underscore to not confuse it with the function image
        self.image = image(image_)
        self.alpha_value = 255 # 0 is fully transparent, 255 is fully visible (fully opaque)

    def remove(self, fade_speed):
        self.alpha_value -= fade_speed # how much the alpha value decreases fer update
        self.image = self.image.set_alpha(self.alpha_value)

class Timer():
    def __init__(self):
        self.start_time = time.time()

    def time_elapsed(self):
        return time.time() - self.start_time

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
        return (self.collide or # collided with other player
                self.x < -self.diameter or # checking for out of bounds
                self.x > WIDTH + self.diameter or
                self.y < -self.diameter or
                self.y > HEIGHT + self.diameter)

    def display(self, screen):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.radius)

class ParticleImage():
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
