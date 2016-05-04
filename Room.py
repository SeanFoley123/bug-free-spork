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
BLUE = pygame.Color('cadetblue1')
 
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_W_MID = SCREEN_WIDTH/2
SCREEN_H_MID = SCREEN_HEIGHT/2

GROUND_LEVEL = 550
STARTING_LEVEL = 100
NEXT_LEVEL = -150

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

        # Makes it so you can change to the next level if there is one
        self.next_level = 0

        # Checks if the Room is a tutorial level
        self.is_tutorial = False
 
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
        
        self.world_size = (SCREEN_WIDTH*5, 800)
        self.world = pygame.Surface(self.world_size)

        # Solid objects. Array with width, height, x, y, and class of obstacle
        room = [[200, SCREEN_HEIGHT-STARTING_LEVEL, 0, STARTING_LEVEL, Ground],
                 [300, 300, 200, 300, Ground],
                 [50, SCREEN_HEIGHT-150, 500, 150, Ground],
                 [200, 425, 550, 375, Ground],
                 [100, 500, 750, 300, Ground],
                 [100, 425, 850, 375, Ground],
                 [100, 325, 950, 475, Ground],
                 [650, 100, 1200, 350, Ground],
                 [400, 200, 1450, 150, Ground],
                 [350, 125, 1500, 350, Ground],
                 [275, 50, 1575, 425, Ground],
                 [150, 325, 1700, 475, Ground],
                 [200, 100, 2050, 300, Lava],
                 [200, 400, 2050, 400, Ground],
                 [400, 500, 2250, 300, Ground],
                 [200, 600, 2650, 200, Ground],
                 [150, 325, 3050, 100, Ground],
                 [400, 100, 3400, 150, Ground],
                 [200, 100, 3800, 200, Ground],
                 [self.world_size[0], 25, 0, 775, Ground]]

        # Objects that hinder movement (and drown the player if they are not flipped) 
        # Array with width, height, x, y, and class of obstacle
        sludge = [[200, 75, 550, 300, Water],
                 [700, 225, 1050, 550, Water],
                 [200, 475, 1850, 300, Water],
                 [200, 500, 2850, 275, Water],
                 [150, 350, 3050, 425, Water],
                 [800, 500, 3200, 275, Water]
                 ]

        # Objects you can eat. Array with width, height, x, y, and class of obstacle
        consumeable = [[50, 50, 150, 50, Edible],
                        [50, 50, 300, 250, Edible],
                        [50, 50, 875, 325, Edible],
                        [50, 50, 1625, 100, Edible],
                        [50, 50, 1625, 500, Edible],
                        [50, 50, 2600, 250, Edible],
                        [50, 50, 3950, 150, Edible]]

        # Enemies on the level- (width, height, start_x, start_y, end_x)
        enemy_list = [[75, 75, 500, 300, 200, Enemy],
                     [75, 75, 1850, 75, 1450, Enemy],
                     [75, 75, 2650, 75, 2252, Enemy],
                     [75, 75, 3800, 75, 3400, Enemy],
                     [100, 100, 3700, 100, 0, AdultDuck],
                     [75, 75, 2550, 75, 0, ChildDuck]]
 
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
            block = enemy[5](enemy[2], enemy[3], enemy[0], enemy[1], enemy[4])
            self.enemy_list.add(block)

class Room_00(Room):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Room.__init__(self, player)
        
        self.world_size = (3000, 800)
        self.world = pygame.Surface(self.world_size)
        self.next_level = 1
        self.is_tutorial = True
        self.tutorial = Tutorial()

        # Solid objects. Array with width, height, x, y, and class of obstacle
        room = [[3000, 200, 0, 600, Ground],
                [500, 400, 0, 200, Ground],
                [200, 300, 500, 300, Ground],
                [300, 200, 700, 400, Ground],
                [200, 300, 1000, 300, Ground],
                [200, 500, 1500, 100, Ground],
                [100, 400, 1700, 200, Ground],
                [200, 300, 2000, 300, Lava],
                [200, 300, 2200, 300, Ground],
                [600, 500, 2400, 100, Ground]]

        # Objects that hinder movement (and drown the player if they are not flipped) 
        # Array with width, height, x, y, and class of obstacle
        sludge = [[300, 100, 700, 300, Water],
                    [300, 300, 1200, 300, Water],
                    [200, 300, 1800, 300, Water]]

        # Objects you can eat. Array with width, height, x, y, and class of obstacle
        consumeable = []

        # Enemies on the level- (width, height, start_x, start_y, end_x)
        enemy_list = [[100, 100, 400, 100, 0, Log],
                     [100, 100, 1100, 200, 0, Log],
                     [75, 75, 2900, 25, 2400, Enemy],
                     [75, 75, 2900, 25, 0, ChildDuck]]
 
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
            block = enemy[5](enemy[2], enemy[3], enemy[0], enemy[1], enemy[4])
            self.enemy_list.add(block)

class Tutorial(object):
    def __init__(self):
        self.text = ['Shoot a spore to decompose the enemy with space! Then eat it... if you dare.',
                    "You're not very buoyant unless you 'f'lip over!",
                    "Try getting up higher using the things you know!",
                    "Y'know... lava doesn't look very safe to touch.",
                    "Use 'e' and 'q' to switch between your spore powers!",
                    "Talk to me with 't'. Also... that duck looks... tasty. Er, fun. Yeah. Fun."]
        self.talk_length = 60

    def __str__(self):
        return 'Enemy'
