import pygame
import sys
import math
import os
import time
import random
import platform
from pygame.locals import *

pygame.init()

fullscreen = True

# OS -------------------------- #
OS = platform.system()

# values  -------------------------- #
FPS = 30
WIN_COINS = 10

# coordinates -------------------------- #
# 1280 720
WIDTH = 640
HEIGHT = 360

MID_X = WIDTH // 2
MID_Y = HEIGHT // 2

# specific positions / offsets -------------------------- #

# character selection
X_OFFSET = 10 # x value offset from the middle
SPACING_X = 300 # spacing between characters
SCROLL_SPEED = 15

CIRCLE_SPACING = 20
CIRCLE_RADIUS = 5

BUTTON_OFFSET = 50
BUTTON_SPACING = 65
BUTTON_Y = 20
BUTTON_HEIGHT = 18
BUTTON_BORDER_RADIUS = 10

USERNAME_Y = MID_Y - 50
PASSWORD_Y = MID_Y + 5

MAX_LEN = 14

WHITE_BOX_WIDTH = 120

HEADING_OFFSET = 20
TITLE_Y = 70

PLAYER_NAME_Y = 25

INCORRECT_TEXT_Y = MID_Y + 50

# fighting
POWERUP_X = 50
POWERUP_Y = MID_Y

LIVES_X = 20
LIVES_Y = MID_Y - 70
LIVES_SPACING = 40

NAME_X = 10
NAME_Y = 50

START_POSITION_X_OFFSET = 50

# specific positions / offsets -------------------------- #

# colours -------------------------- #
'''
Palletes:
ENDESGA 32
RESURRECT 64 PALETTE - https://lospec.com/palette-list/resurrect-64
'''
# general colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# specific colours
BACKGROUND_COLOUR = (200, 255, 255)
SILVER = (192, 203, 220)
GREEN_SELECTED = (125, 255, 160)
AUTHENTICATE_GREEN = (35, 144, 99) # RESURRECT
YELLOW = (249, 194, 43) # RESURRECT

INTERMEDIATE_COLORKEY = (255, 0, 242)

COIN_PURPLE = (156, 132, 243)
MID_BLUE = (77, 156, 230) # RESURRECT

PLAYER_BLUE = (77, 101, 180) # RESURRECT
PLAYER_RED = (232, 59, 59)

POWERUP_USE_COLOUR = (214, 0, 36)
POWERUP_READY_COLOUR = (0, 255, 238)


# fonts -------------------------- #
FONT_20 = pygame.font.Font("data/PressStart2P.ttf", 20)
FONT_10 = pygame.font.Font("data/PressStart2P.ttf", 10)
FONT_8 = pygame.font.Font("data/PressStart2P.ttf", 8)
