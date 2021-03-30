import pygame


# geometry
SIZE = WIDTH, HEIGHT = 800, 600


# color
WHITE = pygame.Color('white')
BLACK = pygame.Color('black')
GREY = pygame.Color(200, 200, 200)

RED = pygame.Color(255, 0, 0)
LIGHTRED = pygame.Color(255, 59, 0)
ORANGERED = pygame.Color(255, 118, 2)
ORANGE = pygame.Color(255, 177, 8)
YELLOW = pygame.Color(255, 235, 24)
YELLOWGREEN = pygame.Color(234, 255, 53)
GREEN = pygame.Color(160, 255, 99)
LIGHTGREEN = pygame.Color(99, 255, 160)
AQUAMARINE = pygame.Color(53, 255, 234)
CYAN = pygame.Color(24, 235, 255)
VERYLIGHTBLUE = pygame.Color(8, 177, 255)
LIGHTBLUE = pygame.Color(2, 118, 255)
BLUE = pygame.Color(0, 59, 255)
DARKBLUE = pygame.Color(0, 0, 255)

LIST_OF_COLORS = [DARKBLUE, BLUE, LIGHTBLUE, VERYLIGHTBLUE, CYAN,
                  AQUAMARINE, LIGHTGREEN, GREEN, YELLOWGREEN,
                  YELLOW, ORANGE, ORANGERED, LIGHTRED, RED]

DICT_OF_COLOR = {'WHITE' : WHITE, 'BLACK' : BLACK, 'GREY' : GREY,
                 'RED' : RED, 'LIGHTRED' : LIGHTRED, 'ORANGERED' : ORANGERED,
                 'ORANGE' : ORANGE, 'YELLOW' : YELLOW, 'YELLOWGREEN' : YELLOWGREEN, 
                 'GREEN' : GREEN, 'LIGHTGREEN' : LIGHTGREEN, 'AQUAMARINE' : AQUAMARINE, 
                 'CYAN' : CYAN, 'VERYLIGHTBLUE' : VERYLIGHTBLUE, 'LIGHTBLUE' : LIGHTBLUE,
                 'BLUE' : BLUE, 'DARKBLUE' : DARKBLUE}

def str_to_color(string):
    return DICT_OF_COLOR[string]
        


