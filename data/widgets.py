from data.constants import *

class CircularButton():
    def __init__(self, x, y, diametre, cor_type, image, on_image):

        self.image = Image(image, diametre, diametre)
        self.on_image = Image(on_image, diametre, diametre)


        self.radius = diametre // 2

        if cor_type == "centre":
            self.centre_x = x
            self.centre_y = y

            self.x =  x - self.radius
            self.y =  y - self.radius
        else:
            self.x = x
            self.y = y

            self.centre_x = self.x + self.radius
            self.centre_y = self.y + self.radius

        self.on_button = False

    def display(self, screen, events, offset):
        for event in events:
            try:
                mouse_x, mouse_y = event.pos

                # +1 used for more allowance
                if math.sqrt(((mouse_x - self.centre_x) ** 2) + ((mouse_y - self.centre_y) ** 2)) <= self.radius + 1:
                    self.on_button = True
                else:
                    self.on_button = False

            except AttributeError:
                pass

        if self.on_button:
            screen.blit(self.on_image, (self.x, self.y))
        else:
            screen.blit(self.image, (self.x, self.y))
