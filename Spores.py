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

        self.rect.y = player.rect.centery
        self.change_x = speed[0] * self.direction
        self.change_y = speed[1] * self.direction

        self.rect.x = player.rect.centerx

        # Set up the room and list of things it can hit
        self.room = None
        self.unaffected = pygame.sprite.Group()
        self.affected = pygame.sprite.Group()
        self.life = 240

    def setup_lists(self):
        """ Sets up the list of what it can affect and what it cannot. """
        pass

    def update(self):
        """ Updates the spore. """
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        self.life -= 1
        if self.life == 0:
            self.kill()

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

        for thing in self.room.can_climb:
            self.affected.add(thing)

    def kill_it(self, other):
        """ Kills the creature and leaves a food in its place """
        if isinstance(other, Friend): # or isinstance(other, ChildDuck):
            new_food = FriendEdible(other.rect.x, other.rect.y, 75, 50)
            height_change = other.rect.height - 50
            new_food.rect.x = other.rect.x
            new_food.rect.y = other.rect.y + height_change
            new_food.player = other.room.player
            other.room.consumeable.add(new_food)
        elif isinstance(other, Enemy):
            new_food = Edible(other.rect.x, other.rect.y, 50, 50)
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
            self.kill_it(thing)

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
            ledge_fungus = FirstLedge(self.rect.centery, self.room, wall, 'right')
            self.room.can_climb.add(ledge_fungus)
        else:
            ledge_fungus = FirstLedge(self.rect.centery, self.room, wall, 'left')
            self.room.can_climb.add(ledge_fungus)

    def update(self):
        """ Updates the spore. """
        Spore.update(self)

        unaffected_hit_list = pygame.sprite.spritecollide(self, self.unaffected, False)
        for thing in unaffected_hit_list:
            if not isinstance(thing, Enemy):
                self.kill()

        affected_hit_list = pygame.sprite.spritecollide(self, self.affected, False)
        for thing in affected_hit_list:
            self.grow_fungi(thing)
            self.kill()

class FirstLedge(pygame.sprite.Sprite):
    """ A set of fungi which a player can climb up. 
        hit_y: the y-coordinate of the spore when it hits the wall
        room: the room so that new ledges can be added to the room
        wall: the wall object the fungus is growing on
        wall_direction: 'left' or 'right' to tell which side the fungus is growing on
        is_first: boolian to see if it is the first ledge to be grown.
        """
    def __init__(self, hit_y, room, wall, wall_direction):
        """ Constructor for the wall that the player can run into. """
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        self.wall = wall
        self.room = room
        self.direction = wall_direction

        if self.wall.rect.height <= 50:
            height = self.wall.rect.height
        else:
            height = 50
 
        # Make a blue wall, of the size specified in the parameters
        if self.direction == 'right':
            self.image = pygame.image.load('png/ledge_attach_right.png').convert_alpha()
        else:
            self.image = pygame.image.load('png/ledge_attach_left.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, height))
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.centery = hit_y
        if wall_direction == 'right':
            self.rect.x = self.wall.rect.left - 50
        else:
            self.rect.x = self.wall.rect.right
        self.spread_per_update = 1
        self.spread_up = self.rect.top
        self.spread_down = self.rect.bottom
        self.climb_okay = True
        # Keep track of the most recent fungi grown on the wall, looking at the top of the ones growing
        #  upward and the bottom of the ones growing down
        self.grow_above = self.rect.top
        self.grow_below = self.rect.bottom

    def grow_new_above(self):
        new_ledge = Ledge(self.spread_up, self.grow_above, self.rect.centerx, self.direction)
        blah = True
        for thing in self.room.wall_list:
            if new_ledge.rect.colliderect(thing):
                blah = False
        if blah:
            self.room.can_climb.add(new_ledge)
            self.grow_above = new_ledge.rect.top

    def grow_new_below(self):
        new_ledge = Ledge(self.grow_below, self.spread_down, self.rect.centerx, self.direction)
        blah = True
        for thing in self.room.wall_list:
            if new_ledge.rect.colliderect(thing):
                blah = False
        if blah:
            self.room.can_climb.add(new_ledge)
            self.grow_below = new_ledge.rect.bottom

    def update(self):
        """ Makes the fungi grow """
        if self.spread_up > self.wall.rect.top:
            self.spread_up -= self.spread_per_update
            if (self.grow_above - self.spread_up) == 50:
                self.grow_new_above()
        elif self.spread_up == self.wall.rect.top and (self.grow_above-self.spread_up) > 25:
            self.grow_new_above()

        if self.spread_down < self.wall.rect.bottom:
            self.spread_down += self.spread_per_update
            if self.spread_down - self.grow_below == 50:
                self.grow_new_below()
        elif self.spread_down == self.wall.rect.bottom and (self.spread_down - self.grow_below) > 25:
            self.grow_new_below()


class Ledge(pygame.sprite.Sprite):
    def __init__(self, top, bottom, centerx, direction):
        pygame.sprite.Sprite.__init__(self)

        height = abs(top-bottom)
        self.direction = direction
        if self.direction == 'right':
            self.image = pygame.image.load('png/ledge_attach_right.png').convert_alpha()
        else:
            self.image = pygame.image.load('png/ledge_attach_left.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, height))
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.y = top
        self.climb_okay = True