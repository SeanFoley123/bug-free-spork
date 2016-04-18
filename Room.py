### All the stuff for Rooms
import math, sys
import pygame
from pygame.locals import *
from Spores import *
from LivingThings import *
from Terrain import *

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

class Room(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
 
    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.wall_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.sludge = pygame.sprite.Group()
        self.consumeable = pygame.sprite.Group()
        self.can_climb = pygame.sprite.Group()
        self.player = player
        self.spore_list = [Decompose_Spore, Ledge_Spore]
        self.active_spore = self.spore_list[0]
         
        # Background image
        self.background = None
 
    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.wall_list.update()
        self.enemy_list.update()
        self.sludge.update()
        self.consumeable.update()
        self.can_climb.update()

    def draw(self):
        """ Draw everything on this level. """
 
        # Draw the background
        self.world.fill(BLUE)
 
        # Draw all the sprite lists that we have
        self.wall_list.draw(self.world)
        self.enemy_list.draw(self.world)
        self.sludge.draw(self.world)
        self.consumeable.draw(self.world)
        self.can_climb.draw(self.world)

# Create platforms for the level
class Room_01(Room):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Room.__init__(self, player)
        
        self.world_size = (1000, 600)
        self.world = pygame.Surface(self.world_size)

        # Solid objects. Array with width, height, x, y, and class of obstacle
        room = [[500, 50, 0, 550, Ground],
                 [180, 30, 200, 400, Ground],
                 [200, 30, 500, 300, Ground],
                 [100, 400, 900, 200, Ground],
                 [150, 90, 700, 550, Lava]
                 ]

        # Objects that hinder movement (and drown the player if they are not flipped) 
        # Array with width, height, x, y, and class of obstacle
        sludge = [
                 #[300, 100, 400, 350, Water],
                 [200, 50, 500, 550, Water]]

        # Objects you can eat. Array with width, height, x, y, and class of obstacle
        consumeable = [[50, 50, 450, 500, Edible],
                        [50, 50, 245, 350, Edible],
                        [50, 50, 160, 500, Edible],
                        [50, 50, 300, 500, Edible],
                        [50, 50, 400, 500, Edible]]

        # Enemies on the level
        enemy_list = [[75, 75, 425, 475, Enemy]]
 
        # Go through the array above and add obstacles
        for obstacle in room:
            block = obstacle[4](obstacle[2], obstacle[3], obstacle[0], obstacle[1])
            block.rect.x = obstacle[2]
            block.rect.y = obstacle[3]
            block.player = self.player
            self.wall_list.add(block)

        for obstacle in sludge:
            block = obstacle[4](obstacle[2], obstacle[3], obstacle[0], obstacle[1])
            block.rect.x = obstacle[2]
            block.rect.y = obstacle[3]
            block.player = self.player
            self.sludge.add(block)

        for food in consumeable:
            block = food[4](food[2], food[3], food[0], food[1])
            block.rect.x = food[2]
            block.rect.y = food[3]
            block.player = self.player
            self.consumeable.add(block)

        for enemy in enemy_list:
            block = enemy[4](enemy[2], enemy[3], enemy[0], enemy[1])
            self.enemy_list.add(block)