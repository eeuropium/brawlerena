import pygame
import sys
import math
import os
import time
import random
from pygame.locals import *

pygame.init()

fullscreen = True

# coordinates -------------------------- #
# 1280 720
WIDTH = 640
HEIGHT = 360

MID_X = WIDTH // 2
MID_Y = HEIGHT // 2

# spcific positions / offsets -------------------------- #
POWERUP_X = 50
POWERUP_Y = MID_Y

LIVES_X = 20
LIVES_Y = MID_Y - 70
LIVES_SPACING = 40

NAME_X = 10
NAME_Y = 50

START_POSITION_X_OFFSET = 50
# colours -------------------------- #
# general colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# specific colours
BACKGROUND_COLOUR = (200, 255, 255)
SILVER = (192, 203, 220)
GREEN_SELECTED = (125, 255, 160)

POWERUP_USE_COLOUR = (214, 0, 36)
POWERUP_READY_COLOUR = (0, 255, 238)

font_20 = pygame.font.Font("data/PressStart2P.ttf", 20)
font_10 = pygame.font.Font("data/PressStart2P.ttf", 10)
