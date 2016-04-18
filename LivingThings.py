### All of the living things

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

class Living(pygame.sprite.Sprite):
    """ This class is all the things that move. """
    def __init__(self, x, y, width, height, image_file_name, initial_speed):
        """ x = upper left corner x component
            y = upper left corner y component
            width = x dimension to resize image to
            height = y dimension to resize image to
            image_file_name = a string of the image file name to load
            initial_speed = how quickly it moves in the x direction
        """
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Set default image
        self.image = pygame.image.load(image_file_name)
        self.image = pygame.transform.scale(self.image, (width, height))

        # Set position
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        # Set initial_speed vector
        self.change_x = initial_speed
        self.change_y = 0

        self.room = None
        self.flipped = False
        self.wet = False

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.wet and self.flipped:
            self.change_y -= .2
        else:
            if self.change_y == 0:
                self.change_y = 1
            else:
                self.change_y += .35
 
    def update(self):
        """ Makes sure all living things can update """
        pass

class MushroomGuy(Living):
    """ This class represents the bar at the bottom that the player
    controls. """
 
    # Constructor function
    def __init__(self):
        # Call the parent's constructor
        Living.__init__(self, 0, 0, 100, 75, 'dog.jpg', 0)
 
        # Set height, width
        self.image_list = [pygame.image.load('dog.jpg').convert(), pygame.image.load('evil_dog1.jpg').convert()]
        for index, image in enumerate(self.image_list):
            self.image_list[index] = pygame.transform.scale(image, (100, 75))

        self.speed = 6

        # Corruption starts at zero. Eating mushrooms increases corruption. As corruption increases,
        #  player avatar image changes (every 5 points)
        self.corruption = 0

        # Set shot direction: 1 = right, -1 = left
        self.shot_dir = 1

        self.wound = 0
        self.max_wound = 5
        
        #sets drowning for sludge
        self.drown = 0
        self.max_drown = 100

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -self.speed

        # Make the shot direction to the left
        self.shot_dir = -1
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = self.speed

        # Make the shot direction to the right
        self.shot_dir = 1
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0

    def jump(self):
        """ Called when user hits 'jump' button. """
 
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        wall_hit_list = pygame.sprite.spritecollide(self, self.room.wall_list, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        # That's a really cool way to do this
        if len(wall_hit_list) > 0 and not self.flipped:
            self.change_y = -10

    #TODO: possible better way to do this: need to discuss
    # a better way to do this may be to keep track of the current sprite in a variable  
    # and have both how_corrupt and draw_flipped use that variable

    def how_corrupt(self):
        """ Changes the image based on the corruption level of the player. """
        self.image = pygame.transform.scale(self.image_list[self.corruption/5], (100, 75))

    def draw_flipped(self):
        """Flips the player's sprite based on the value assigned to self.flipped (controlled by keypress)"""
        if self.flipped:
            self.image = pygame.transform.flip(self.image_list[self.corruption/5], False, True)

    def climb(self):
        if pygame.sprite.spritecollide(self, self.room.can_climb, False):
            self.change_y = -5
 
    def update(self):
        """ Update the player position. """
        #print self.flipped
        #print pygame.sprite.spritecollide(self, self.room.sludge, False)
        # Gravity
        self.calc_grav()
        # Move left/right
        if self.flipped and not self.wet:
            self.change_x = 0
        self.rect.x += self.change_x
 
        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.room.wall_list, False)
        for block in block_hit_list:
            # Check if it is deadly
            if block.mortality == True:
                self.wound += 1
            else:
                # If we are moving right, set our right side to the left side of
                # the item we hit
                if self.change_x > 0:
                    self.rect.right = block.rect.left
                else:
                    # Otherwise if we are moving left, do the opposite.
                    self.rect.left = block.rect.right
                self.wound = 0

        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.room.wall_list, False)
        for block in block_hit_list:
            # Check if it's deadly ISUE: You can survive lava if you're at the bottom of a lake
            if block.mortality == True:
                self.wound += 1

            else:
                # Reset our position based on the top/bottom of the object.
                if self.change_y > 0:
                    self.rect.bottom = block.rect.top
                else:
                    self.rect.top = block.rect.bottom

                    # Stop our vertical movement
                self.change_y = 0
                self.wound = 0

        # Check if we are stuck in something viscous and slow us down + drown us if we are
        block_hit_list = pygame.sprite.spritecollide(self, self.room.sludge, False)
        if block_hit_list:
            self.wet = True
            if not self.flipped:
                self.drown += 1
        else:
            self.drown = 0
            self.wet = False
        for block in block_hit_list:
            self.rect.x -= self.change_x*block.visc
            self.rect.y -= self.change_y*block.visc
        #TODO: for some reason, spritecollide only works when you're crossing the left portion of the rect. 
        #I have no clue why. It doesn't matter with a short max_drown, but it needs to be fixed.
        # Moved this one from the drowning check above.

        # Check to see if we ate anything
        food_hit_list = pygame.sprite.spritecollide(self, self.room.consumeable, True)
        for food in food_hit_list:
            self.corruption += food.corr_points

        # Check if we're going to die
        enemy_hit_list = pygame.sprite.spritecollide(self, self.room.enemy_list, False)
        for enemy in enemy_hit_list:
            if enemy.mortality == True:
                self.kill()

        if self.wound > self.max_wound or self.drown > self.max_drown:
            self.kill()

        self.how_corrupt()
        self.draw_flipped()


class Enemy(Living):
    """ This is the base class for anything that is alive and should move that isn't the player. """
    def __init__(self, x, y, width, height, speed = -2, distance = -200, mortality = True):
        """ x = upper left corner x component
            y = upper left corner y component
            width = x dimension
            height = y dimension 
            speed = how quickly it moves in the x direction
            distance = how far it can walk
            mortality = does it kill you? """
        # Call the parent's constructor
        Living.__init__(self, x, y, width, height, 'evil_dog1.jpg', speed)

        # Set the range of values it can go between
        self.start_x = x
        self.end_x = x + distance - self.rect.width

        # Set speed vector
        self.change_x = speed
        self.change_y = 0

        self.mortality = mortality

    def update(self):
        """ Update the enemy position. """
        # Gravity
        self.calc_grav()
        # Move left/right
        self.rect.x += self.change_x
 
        # Did this update cause it to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.room.wall_list, False)
        for block in block_hit_list:
            # If the enemy is moving right, set its right side to the left side of
            # the item it hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # Otherwise if it is moving left, do the opposite.
                self.rect.left = block.rect.right

            # Change direction
            self.change_x = -self.change_x

        # Check to see if it has hit the end of its range
        if self.rect.x <= self.end_x or self.rect.x >= self.start_x:
            self.change_x = -self.change_x
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if it hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.room.wall_list, False)
        for block in block_hit_list:
 
            # Reset its position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

            # Stop its vertical movement
            self.change_y = 0

class Edible(pygame.sprite.Sprite):
    """ This is the base class; any new foods should be modified from this one.
        Maybe make this an inherited class from Obstacle? """
    def __init__(self, x, y, width, height, corr_points = 1):
        """ Constructor for the wall that the player can run into. """
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Set the visual
        self.image = pygame.image.load('evilmushroom.png')
        self.image = pygame.transform.scale(self.image, (width, height))
        self.corr_points = corr_points

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x