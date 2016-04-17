### All the stuff for the spore classes
import math, sys
import pygame
from pygame.locals import *
from LivingThings import *

# -- Global constants
 
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_W_MID = SCREEN_WIDTH/2
SCREEN_H_MID = SCREEN_HEIGHT/2

#TODO: there is a bug where after a very long time, the spores loop back around the screen. 
#we need to kill the spores when they hit the edge of the screen

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

    def setup_lists(self):
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

    def setup_lists(self):
        """ Sets up the list of what it can affect and what it cannot. """
        
        # Decompose spores do not affect terrain like ground or water
        for thing in self.room.wall_list:
            self.unaffected.add(thing)

        for thing in self.room.sludge:
            self.unaffected.add(thing)

        # It does, however, destroy enemies and things that are alive. Later implement logs.
        for thing in self.room.enemy_list:
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
        Spore.update(self)

        unaffected_hit_list = pygame.sprite.spritecollide(self, self.unaffected, False)
        for thing in unaffected_hit_list:
            self.kill()

        affected_hit_list = pygame.sprite.spritecollide(self, self.affected, False)
        for thing in affected_hit_list:
            self.kill_it(thing, Edible)

class Ledge_Spore(Spore):
    """ Creates ledge-like fungi that allow you to climb up a surface. Cover the entire surface. """
    def __init__(self, player):
        Spore.__init__(self, player)
        self.image.fill(pygame.Color('darkgoldenrod4'))

    def setup_lists(self):
        """ Sets up the list of what it can affect and what it cannot. """
        
        # Ledge spores affect walls, but not lava, water, or enemies.
        for thing in self.room.wall_list:
            if thing.mortality == False:
                self.affected.add(thing)
            else:
                self.unaffected.add(thing)

        for thing in self.room.sludge:
            self.unaffected.add(thing)

        for thing in self.room.enemy_list:
            self.unaffected.add(thing)

    def grow_fungi(self, wall):
        """ Creates a a surface on the wall which the player can climb up. """
        if self.direction == 1:
            ledge_fungus = Ledge(wall.rect.x - 50, wall.rect.y, wall.rect.height)
            self.room.can_climb.add(ledge_fungus)
        else:
            ledge_fungus = Ledge(wall.rect.x + wall.rect.width + 50, wall.rect.y, wall.rect.height)
            self.room.can_climb.add(ledge_fungus)

    def update(self):
        """ Updates the spore. """
        Spore.update(self)

        unaffected_hit_list = pygame.sprite.spritecollide(self, self.unaffected, False)
        for thing in unaffected_hit_list:
            self.kill()

        affected_hit_list = pygame.sprite.spritecollide(self, self.affected, False)
        for thing in affected_hit_list:
            self.grow_fungi(thing)
            self.kill()

class Ledge(pygame.sprite.Sprite):
    """ A set of fungi which a player can climb up. """
    def __init__(self, x, y, height):
        """ Constructor for the wall that the player can run into. """
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
 
        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([50, height])
        self.image.fill(pygame.Color('darkgoldenrod4'))
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.climb_okay = True
