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
def display_center(screen, surf, coordinates, special_flags = ""): # surf is usually an image
    surf_rect = surf.get_rect(center = coordinates)

    if special_flags:
        screen.blit(surf, surf_rect, special_flags = special_flags)
    else:
        screen.blit(surf, surf_rect)

def center_draw_rect(screen, colour, rect, border_radius = 0):
    x, y, width, height = rect

    new_rect = pygame.Rect(0, 0, width, height)
    new_rect.center = (x, y)

    if border_radius == 0:
        pygame.draw.rect(screen, colour, new_rect)
    else:
        pygame.draw.rect(screen, colour, new_rect, border_radius = border_radius) # the argument "border radius" passed in

def circle_surf(radius, colour):
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, colour, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf

def glow_surf(min_radius, max_radius, total_circles, in_colour, out_colour):
    surf = pygame.Surface((max_radius * 2, max_radius * 2))

    # if (max_radius - min_radius) % radius_interval != 0: # check if number of glows is a whole number
    #     assert False

    radius_interval = (max_radius - min_radius) // total_circles

    colour_diff = [in_colour[i] - out_colour[i] for i in range(3)]

    curr_radius = max_radius

    for count in range(total_circles):
        curr_radius -= radius_interval
        curr_colour = tuple(out_colour[i] + colour_diff[i] * count / total_circles for i in range(3))
        display_center(surf, circle_surf(curr_radius, curr_colour), (max_radius, max_radius))
        print(count, curr_radius, curr_colour)

    return surf

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
def get_image(path):
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
