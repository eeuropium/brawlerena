# testing a change again
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
