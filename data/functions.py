from data.constants import *

# logic

# maths
def sgn(x):
    if x < 0:
        return -1
    if x == 0:
        return 0
    return 1

# display
def display_center(screen, surf, coordinates): # surf is usually an image
    surf_rect = surf.get_rect(center = coordinates)
    screen.blit(surf, surf_rect)

# font
def display_font_center(screen, text, font_name, colour, coordinates):
    font = eval(font_name)
    font_size = int(font_name.split('_')[1])
    lines = list(text.split('\n'))

    x, y = coordinates

    for line in lines:
        text = font.render(line, False, colour)
        display_center(screen, text, (x, y))
        y += font_size * 1.6
        # recommended line break value font_size timesvalue between 1.4 to 1.8

# upload
def image(path):
    return pygame.image.load("data/images/" + path)


# collision
def circle_collision(circle1, circle2):
    # x,y = coordinates, r = radius of circle
    x1, y1, r1 = circle1
    x2, y2, r2 = circle2

    if (x1 - x2) ** 2 + (y1 - y2) ** 2 < (r1 + r2) ** 2:
        return True
    return False

# physics
def angle_move_x(angle, speed):
    return speed * math.sin(math.radians(angle))

def angle_move_y(angle, speed):
    return -speed * math.cos(math.radians(angle)) # negative needed because up is negative in pygame coordinate system

def collision_physics(object1_speed, object1_mass, object2_speed, object2_mass):
    object1_final_speed = object1_speed * (object1_mass - object2_mass) / (object1_mass + object2_mass) + object2_speed * (2 * object2_mass) / (object1_mass + object2_mass)
    object2_final_speed = object2_speed * (object2_mass - object1_mass) / (object1_mass + object2_mass) + object1_speed * (2 * object1_mass) / (object1_mass + object2_mass)
    return object1_final_speed, object2_final_speed

# colours
def palette_swap(org_image, old_colour, new_colour):
    black_surf = pygame.Surface(org_image.get_size())
    black_surf.blit(org_image, (0, 0))
    black_surf.set_colorkey(old_colour)

    final_surf = pygame.Surface(org_image.get_size())
    final_surf.fill(new_colour)
    final_surf.blit(black_surf, (0 ,0))
    final_surf.set_colorkey((0, 0, 0))

    return final_surf
