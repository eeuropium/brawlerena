from data.constants import *
from data.functions import *
from data.managers import *

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

            self.outline_colour = PLAYER_BLUE

        elif player_number == 2:
            self.org_x = MID_X + START_POSITION_X_OFFSET
            self.org_y = MID_Y
            self.angle = 90

            if self.controller_type == "keyboard":
                self.controls = {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP, "down": pygame.K_DOWN, "powerup": pygame.K_SLASH}

            self.powerup_x, self.powerup_y = WIDTH - POWERUP_X, POWERUP_Y

            self.lives_x, self.lives_y = WIDTH - LIVES_X, LIVES_Y # coordiantes of first heart shape
            self.lives_spacing = -LIVES_SPACING # distance apart for heart shapes

            self.outline_colour = PLAYER_RED

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
    def update(self, keys, events):

        if self.controller_type == "keyboard":
            # x and y movement
            if keys[self.controls["left"]]:
                self.dx -= self.acceleration
            elif keys[self.controls["right"]]:
                self.dx += self.acceleration
            else:
                temp_dx = self.dx - sgn(self.dx) * self.deceleration
                if sgn(self.dx) != sgn(temp_dx):
                    self.dx = 0
                else:
                    self.dx = temp_dx

            if keys[self.controls["up"]]:
                self.dy -= self.acceleration
            elif keys[self.controls["down"]]:
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
        # 180 is acdded as flipping the image since the image points down when uploading
        if self.animate:
            self.image = pygame.transform.rotate(self.idle_animation.current_frame(), self.angle + 180) # counter clockwise rotation
        else:
            self.image = pygame.transform.rotate(self.org_image, self.angle + 180)

    def display(self, screen):
        # displaying character
        display_center(screen, self.image, (self.x, self.y))

        # creating outline
        outline_surf = pygame.Surface((self.image.get_width(), self.image.get_height()))
        outline_surf.set_colorkey(BLACK)

        mask = pygame.mask.from_surface(self.image)
        try:
            pygame.draw.lines(outline_surf, self.outline_colour, False, mask.outline(), 2)
        except ValueError:
            pass

        # displaying outline
        display_center(screen, outline_surf, (self.x, self.y))

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
        pass

    def powerup_initialise(self):
        pass

    def powerup_update_in_use(self):
        pass

    def powerup_function(self, other_player):
        pass

    def powerup_reset(self):
        if self.powerup_state == "in use":
            self.powerup_state = "charging"
            self.powerup_charge = 0

    def powerup_update(self, keys, other_player):
        if self.powerup_state == "charging":
            self.powerup_charge += self.powerup_charge_rate

            if self.powerup_charge > 360:
                self.powerup_charge = 360
                self.powerup_state = "ready"

            self.powerup_half_charge_rotate = pygame.transform.rotate(self.powerup_half_charge_rotate_org, self.powerup_charge)
            self.powerup_update_charge()

        elif self.powerup_state == "ready" and keys[self.controls["powerup"]]:
            self.powerup_state = "in use"
            self.powerup_initialise()

        # not elif, need the use image immediately after state changes to in use
        if self.powerup_state == "in use":
            self.powerup_charge -= self.powerup_use_rate

            if self.powerup_charge < 0:
                self.powerup_charge = 0
                self.powerup_state = "charging"
                self.powerup_reset()

            self.powerup_half_use_rotate = pygame.transform.rotate(self.powerup_half_use_rotate_org, self.powerup_charge)
            self.powerup_update_in_use()

        self.powerup_function(other_player)

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

class GroundHog(Standard):
    def character_init(self):
        self.org_image = image("playing/characters/GroundHog/character.png")
        self.powerup_icon = image("playing/characters/GroundHog/icon.png")

        self.powerup_charge_time = 3
        self.powerup_use_time = 2


    def __init__(self, player_number, controller_type):
        super().__init__(player_number, controller_type)

        self.spike_particle_group = []

        self.circle_particle_group = []

        spike_particle_var1 = image("playing/characters/GroundHog/spike_particle.png")

        spike_particle_var2 = palette_swap(spike_particle_var1, (64, 57, 66), (103, 90, 112)) # dark colour
        spike_particle_var2 = palette_swap(spike_particle_var1, (98, 85, 101), (127, 112, 138)) # light colour

        spike_particle_var3 = palette_swap(spike_particle_var1, (64, 57, 66), (72, 74, 119)) # dark colour
        spike_particle_var3 = palette_swap(spike_particle_var1, (98, 85, 101), (77, 101, 180)) # light colour

        spike_particle_var4 = palette_swap(spike_particle_var1, (64, 57, 66), (85, 72, 96)) # dark colour
        spike_particle_var4 = palette_swap(spike_particle_var1, (98, 85, 101), (62, 53, 70)) # light colour

        self.spike_particle_images = [spike_particle_var1, spike_particle_var2, spike_particle_var3, spike_particle_var4]


    class SpikeParticle(ParticleImage):
        def __init__(self, x, y, image_, angle, speed):
            self.x = x
            self.y = y

            self.dx = angle_move_x(angle, speed)
            self.dy = angle_move_y(angle, speed)

            self.radius = 5
            self.mass = 0.7

            self.image = pygame.transform.rotate(image_, -angle)
            self.diameter = self.image.get_width()

            self.collide = False

        def update(self, other_player):
            self.x += self.dx
            self.y += self.dy

            if circle_collision((self.x, self.y, self.radius),
                                (other_player.x, other_player.y, other_player.radius)):
                self.dx, other_player.dx = collision_physics(self.dx, self.mass, other_player.dx, other_player.mass)
                self.dy, other_player.dy = collision_physics(self.dy, self.mass, other_player.dy, other_player.mass)

                self.collide = True

        def should_remove(self):
            return (self.collide or super().should_remove())

    def powerup_initialise(self):
        particle_angle_offset = random.randint(0, 45)

        for i in range(8):
            self.spike_particle_group.append(self.SpikeParticle(self.x, self.y, random.choice(self.spike_particle_images), (i * 45 + particle_angle_offset) % 360, 5))

    def powerup_function(self, other_player):
        if len(self.spike_particle_group) > 0:
            remove = []

            for particle in self.spike_particle_group:
                particle.update(other_player)

                if particle.should_remove():
                    remove.append(particle)

            for particle in remove:
                self.spike_particle_group.remove(particle)
            remove.clear()

    def powerup_display(self, screen):
        super().powerup_display(screen)

        for particle in self.spike_particle_group:
            particle.display(screen)

    def reset(self):
        super().reset()
        self.spike_particle_group.clear()

class Blob(Standard):
    def character_init(self):
        self.idle_animation = Animation(4, 4, "playing/characters/Blob/", "character")
        self.powerup_icon = image("playing/characters/GroundHog/icon.png")

        self.powerup_charge_time = 3
        self.powerup_use_time = 2

    def __init__(self, player_number, controller_type):
        super().__init__(player_number, controller_type, "True")

class B79(Standard):
    def character_init(self):
        self.org_image = image("playing/characters/B79/character.png")
        self.powerup_icon = image("playing/characters/GroundHog/icon.png")

        self.powerup_charge_time = 3
        self.powerup_use_time = 2

        path = "playing/characters/B79/"

        self.org_radius = 16
        self.powerup_radius = 32

        self.different_images = [image(path + "battery.png"),
                                 image(path + "happy.png"),
                                 image(path + "lose.png"),
                                 image(path + "character.png")]

        self.powerup_image = image(path + "powerup.png")


        self.change_timer = Timer()
        self.change_interval = random.randint(10, 15)
        self.change_interval = random.randint(1, 2)

    # def __init__(self, player_number, controller_type):
    #     super().__init__("B79", "neutral.png",
    #                      player_number, controller_type,
    #                      1, 10)
    #     path = "playing/characters/B79/"
    #
    #     self.org_radius = 16
    #     self.powerup_radius = 32
    #
    #     self.different_images = [image(path + "battery.png"),
    #                              image(path + "happy.png"),
    #                              image(path + "lose.png"),
    #                              image(path + "neutral.png")]
    #
    #     self.powerup_image = image(path + "powerup.png")
    #
    #
    #     self.change_timer = Timer()
    #     self.change_interval = random.randint(10, 15)
    #     self.change_interval = random.randint(1, 2)

    def update(self, keys, events):
        super().update(keys, events)

        if self.powerup_state != "in use":
            if self.change_timer.time_elapsed() > self.change_interval:
                self.change_interval = random.randint(1, 2) # change interval for more random behaviour
                self.change_timer = Timer()
                self.org_image = random.choice(self.different_images)

class Aurora(Standard):
    def character_init(self):
        self.org_image = image("playing/characters/Aurora/character.png")
        self.powerup_icon = image("playing/characters/GroundHog/icon.png")

        self.powerup_charge_time = 3
        self.powerup_use_time = 2

class Volta(Standard):
    def character_init(self):
        self.org_image = image("playing/characters/Volta/character.png")
        self.powerup_icon = image("playing/characters/GroundHog/icon.png")

        self.powerup_charge_time = 3
        self.powerup_use_time = 2

class Jian(Standard):
    def character_init(self):
        self.jian_image = image("playing/characters/Jian/character.png")

        self.org_image = self.jian_image # org_image is the rotated displayed image
        self.powerup_icon = image("playing/characters/GroundHog/icon.png")

        self.powerup_charge_time = 5
        self.powerup_use_time = 5

        self.org_radius = 16
        self.powerup_radius = 37

        self.powerup_image = image("playing/characters/Jian/powerup.png")

    def out_of_bounds(self):
        arena_radius = HEIGHT // 2

        if (MID_X - self.x) ** 2 + (MID_Y - self.y) ** 2 > (arena_radius - self.org_radius) ** 2: # check collision with side
            self.lives -= 1
            return True
        return False

    def powerup_reset(self):
        super().powerup_reset()

        self.radius = self.org_radius
        self.org_image = self.jian_image

    def powerup_update_charge(self):
        self.radius = self.org_radius

    def powerup_initialise(self):
        self.org_image = self.powerup_image
        self.radius = self.powerup_radius

        self.mass = 1.1

class Metor(Standard):
    def character_init(self):
        self.org_image = image("playing/characters/Metor/character.png")
        self.powerup_icon = image("playing/characters/GroundHog/icon.png")

        self.powerup_charge_time = 3
        self.powerup_use_time = 2
