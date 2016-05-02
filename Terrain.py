### All the stuff for terrain

import math, sys
import pygame
from pygame.locals import *

# -- Global constants
 
# Colors - check out pygame.Colors. Probably does exactly what you want
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
 
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_W_MID = SCREEN_WIDTH/2
SCREEN_H_MID = SCREEN_HEIGHT/2

class Obstacle(pygame.sprite.Sprite):
    """ Immobile things that the player might run into. """
    def __init__(self, x, y, width, height, visc = 1, mortality = False):
        """ Constructor for the wall that the player can run into. """
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
 
        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(BLUE)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        # Add the extra attributes we want
        self.visc = visc
        self.mortality = mortality

class Ground(Obstacle):
    """ Solid surfaces or walls. """
    def __init__(self, x, y, w, h):
		Obstacle.__init__(self, x, y, w, h, 0, False)

		# Make the color and all different
		self.image = pygame.Surface((w, h))
		self.image.fill((85, 140, 90))

class Lava(Obstacle):
    """ Deadly red terrain. """
    def __init__(self, x, y, w, h):
		Obstacle.__init__(self, x, y, w, h, .5, True)

		# Make the color correct
		self.image = pygame.Surface((w, h))
		self.image.fill(pygame.Color('chocolate1'))

class Water(Obstacle):
    """ Slows you down. """
    def __init__(self, x, y, w, h):
        Obstacle.__init__(self, x, y, w, h, .5, False)

        # Make the color correct
        self.image = pygame.Surface((w, h))
        self.image.fill((85, 200, 255))