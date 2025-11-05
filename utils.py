import pygame

# some global constants
WIDTH = 800
HEIGHT = 800

# colors.
# if you find it more suitable, change this dictionary to standalone constants like: RED = (255, 0, 0)
COLORS = {
    'RED': (255, 255, 192),           # closed nodes
    'GREEN': (0, 255, 0),         # open nodes
    'BLUE': (0, 0, 255),          # start node
    'YELLOW': (150, 190, 255),      # end node
    'WHITE': (255, 255, 255),     # unvisited nodes
    'BLACK': (0, 0, 0),           # barrier
    'PURPLE': (128, 0, 128),      # path
    'ORANGE': (255, 192, 192),      # nodes being considered
    'GREY': (128, 128, 128),      # grid lines
    'TURQUOISE': (64, 224, 208)   # neighbor nodeS
}