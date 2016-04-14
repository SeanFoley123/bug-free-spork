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

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
 
        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

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
        self.climb_okay = False

        # Corruption starts at zero. Eating mushrooms increases corruption. As corruption increases,
        #  player avatar image changes (every 5 points)
        self.corruption = 0

        # Set shot direction: 1 = right, -1 = left
        self.shot_dir = 1

        self.wound = 0
        self.max_wound = 5
 
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
        if len(wall_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

    def how_corrupt(self):
        """ Changes the image based on the corruption level of the player. """
        self.image = pygame.transform.scale(self.image_list[self.corruption/5], (100, 75))

    def climb(self):
        self.change_y = -5
 
    def update(self):
        """ Update the player position. """
        # Gravity
        self.calc_grav()
        # Move left/right
        self.rect.x += self.change_x
 
        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.room.wall_list, False)
        for block in block_hit_list:
            # Check if it is deadly
            if block.mortality == True:
                self.wound += 1
                if self.wound > self.max_wound:
                    self.kill()
            else:
                # If we are moving right, set our right side to the left side of
                # the item we hit
                if self.change_x > 0:
                    self.rect.right = block.rect.left
                else:
                    # Otherwise if we are moving left, do the opposite.
                    self.rect.left = block.rect.right
                self.wound = 0

        # Did this update cause us to hit a deadly object?
        block_hit_list = pygame.sprite.spritecollide(self, self.room.sludge, False)
        for block in block_hit_list:
            self.rect.x -= self.change_x*block.visc

        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.room.wall_list, False)
        for block in block_hit_list:
            # Check if it is deadly
            if block.mortality == True:
                self.wound += 1
                if self.wound > self.max_wound:
                    self.kill()
            else:
                # Reset our position based on the top/bottom of the object.
                if self.change_y > 0:
                    self.rect.bottom = block.rect.top
                else:
                    self.rect.top = block.rect.bottom

                    # Stop our vertical movement
                self.change_y = 0
                self.wound = 0

        # Check if we are stuck in something viscous and slow us down if we are
        block_hit_list = pygame.sprite.spritecollide(self, self.room.sludge, False)
        for block in block_hit_list:
            self.rect.y -= self.change_y*block.visc

        enemy_hit_list = pygame.sprite.spritecollide(self, self.room.enemy_list, False)
        for enemy in enemy_hit_list:
            if enemy.mortality == True:
                self.kill()

        # Check to see if we ate anything
        food_hit_list = pygame.sprite.spritecollide(self, self.room.consumeable, True)
        for food in food_hit_list:
            self.corruption += food.corr_points

        if pygame.sprite.spritecollide(self, self.room.can_climb, False) != []:
            self.climb_okay = True
        else:
            self.climb_okay = False

        # Update the picture if necessary
        self.how_corrupt()


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