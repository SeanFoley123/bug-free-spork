### All the stuff for the spore classes
import math, sys
import pygame
from pygame.locals import *
from LivingThings import *

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

class Spore(pygame.sprite.Sprite):
    """ Base class of spores. 

        player: pass the player into the shot
        speed: a tuple of the x velocity and the y velocity
        size: a tuple of the width and height of the shot"""
    def __init__(self, player, speed = (8,0), size = (10,10)):
        # Call the parent's init
        pygame.sprite.Sprite.__init__(self)

        # Make visible and set direction
        self.image = pygame.Surface([size[0], size[1]])
        self.image.fill(pygame.Color('blueviolet'))
        self.direction = player.shot_dir

        # Set up initial position and direction of shot
        self.rect = self.image.get_rect()

        self.rect.y = player.rect.y + player.rect.height/2
        self.change_x = speed[0] * self.direction
        self.change_y = speed[1] * self.direction

        if self.direction == 1:
            self.rect.x = player.rect.x + player.rect.width
        else:
            self.rect.x = player.rect.x

        # Set up the room and list of things it can hit
        self.room = None
        self.unaffected = pygame.sprite.Group()
        self.affected = pygame.sprite.Group()

    def setup_lists(self, room):
        """ Sets up the list of what it can affect and what it cannot. """
        pass

    def update(self):
        """ Updates the spore. """
        self.rect.x += self.change_x
        self.rect.y += self.change_y

class Decompose_Spore(Spore):
    """ A spore that decomposes things it touches. """
    def __init__(self, player):
        Spore.__init__(self, player)
        self.image.fill(pygame.Color('chartreuse3'))

    def setup_lists(self, room):
        """ Sets up the list of what it can affect and what it cannot. """
        
        # First, the unaffected things
        for thing in room.wall_list:
            self.unaffected.add(thing)

        for thing in room.sludge:
            self.unaffected.add(thing)

        # Then the things it can affect
        for thing in room.enemy_list:
            self.affected.add(thing)

    def kill_it(self, other, consumeable_type):
        """ Kills the creature and leaves a food in its place """
        new_food = consumeable_type(other.rect.x, other.rect.y, 50, 50)
        height_change = other.rect.height - 50
        new_food.rect.x = other.rect.x
        new_food.rect.y = other.rect.y + height_change
        new_food.player = other.room.player
        other.room.consumeable.add(new_food)
        other.kill()
        self.kill()

    def update(self):
        """ Updates the spore. """
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        unaffected_hit_list = pygame.sprite.spritecollide(self, self.unaffected, False)
        for thing in unaffected_hit_list:
            self.kill()

        affected_hit_list = pygame.sprite.spritecollide(self, self.affected, False)
        for thing in affected_hit_list:
            self.kill_it(thing, Edible)