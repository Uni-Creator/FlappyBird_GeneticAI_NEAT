import pygame
import os
pygame.font.init()


#=================== General constants ==================================
FPS = 30
GEN = 0
WIN_WIDTH = 500
WIN_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
             pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
             pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png')))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))

NODE_FONT = pygame.font.SysFont("comicsans", 15)
BUTTON_FONT = pygame.font.SysFont('consolas', 24)
STAT_FONT = pygame.font.SysFont('comicsans', 24)

HIGH_SCORE_FILE = "high_score.txt"

INPUT_NEURONS = 3
OUTPUT_NEURONS = 1

NODE_RADIUS = 10
NODE_SPACING = 5
LAYER_SPACING = 40
CONNECTION_WIDTH = 1

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
DARK_RED = (100, 0, 0)
RED_PALE = (250, 200, 200)
DARK_RED_PALE = (150, 100, 100)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 100, 0)
GREEN_PALE = (200, 250, 200)
DARK_GREEN_PALE = (100, 150, 100)
BLUE = (0,0,255)
BLUE_PALE = (200, 200, 255)
DARK_BLUE = (100, 100, 150)


#=================== Constants for internal use ==================================
GEN = 0

#enumerations
JUMP = 0

INPUT = 0
MIDDLE = 1
OUTPUT = 2
