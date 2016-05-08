### All of the living things

import math, sys
import pygame
from pygame.locals import *
from numpy import sign

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
        self.image = pygame.image.load(image_file_name).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))

        # Set position
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        # Set initial_speed vector
        self.change_x = initial_speed
        self.change_y = 0

        # Set basic parameters/all the flags
        self.room = None # makes it so you can check collisions with objects in the room/affect them
        self.flipped = False # flips you over, used to draw you upside-down and let you float
        self.wet = False # checks to see if you are touching water and will make you drown
        self.talked = False # checks to see if you have spoken to your mushroom and triggers text

    def calc_grav(self):
        """ Calculate effect of gravity. Changes based on whether you're in the water or floating or on the ground. """
        if self.wet and self.flipped and not self.is_floating():
            self.change_y -= .2
        elif self.is_floating() and self.flipped:
            pass
        else:
            if self.change_y == 0: # gives an initial speed bump
                self.change_y = 1
            else:
                self.change_y += .35 # steadily increases the fall
 
    def update(self):
        """ Makes sure all living things can update """
        pass

    def is_floating(self):
        """ Check to see if you are floating on top of water """
        # Checks if there is water 1 pixel below you
        self.rect.y += 1
        water_beneath = pygame.sprite.spritecollide(self, self.room.sludge, False)
        
        # Checks if there is water in the spot you actually occupy
        self.rect.y -= 1
        in_water = pygame.sprite.spritecollide(self, self.room.sludge, False)
    
        # If there's water beneath you but you're not in water, you're floating!
        return water_beneath and not in_water

class MushroomGuy(Living):
    """ This class represents the player character. """
    def __init__(self):
        self.size = (75, 75)
        # Call the parent's constructor
        Living.__init__(self, 0, 0, self.size[0], self.size[1], 'png/mg_tc0.png', 0)
 
        # Set images
        self.image_list = [pygame.image.load('png/mg_tc0.png').convert_alpha(), pygame.image.load('png/mg_tc1.png').convert_alpha(), pygame.image.load('png/mg_tc2.png').convert_alpha()]
        for index, image in enumerate(self.image_list):
            self.image_list[index] = pygame.transform.scale(image, self.size)

        # Make list of things your mushroom will say to you
        self.text = ["SYMBIOTE: C'mon, we won't be able to find your family if we don't eat something...!",
                            "SYMBIOTE: Look at how strong we are! We don't need anyone else, aren't I enough for you?",
                            "SYMBIOTE: Wow, um... I think that's... probably enough?"]

        self.speed = 6

        # Corruption starts at zero. Eating mushrooms increases corruption. As corruption increases,
        #  player avatar image changes (every corrupt_change points)
        self.corruption = 0
        self.corrupt_change = 7
        self.list_index = 0

        # Set shot direction: 1 = right, -1 = left
        self.shot_dir = 1

        # Set how much abuse the player can take before dying. wound will increase until it hits max_wound
        self.wound = 0
        self.max_wound = 1000
        
        #sets drowning for sludge
        self.drown = 0
        self.max_drown = 120

        #Fire!
        self.on_fire = False

        self.talk_length = 240 # Sets how long text from hitting 't' will last

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        if ((self.is_floating() or self.wet) and self.flipped) or not self.flipped:
            self.change_x = -self.speed
        else:
            self.change_x = 0
        # Make the shot direction to the left
        self.shot_dir = -1
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        if ((self.is_floating() or self.wet) and self.flipped) or not self.flipped:
            self.change_x = self.speed
        else:
            self.change_x = 0

        # Make the shot direction to the right
        self.shot_dir = 1
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0

    def jump(self):
        """ Called when user hits 'jump' button. Currently does nothing, but can be uncommented if desired. """
        pass
        # # move down a bit and see if there is a platform below us.
        # # Move down 2 pixels because it doesn't work well if we only move down
        # # 1 when working with a platform moving down.
        # self.rect.y += 2
        # wall_hit_list = pygame.sprite.spritecollide(self, self.room.wall_list, False)
        # self.rect.y -= 2
 
        # # If it is ok to jump, set our speed upwards
        # # That's a really cool way to do this
        # if len(wall_hit_list) > 0 and not self.flipped:
        #     self.change_y = -5

    def how_corrupt(self):
        """ Changes the image based on the corruption level of the player. Currently, 3 levels of corruption. """
        self.list_index = self.corruption/self.corrupt_change
        if self.list_index > len(self.image_list) - 1:
            self.list_index = len(self.image_list) - 1
        self.image = self.image_list[self.list_index]

    def draw_flipped(self):
        """Flips the player's sprite based on the value assigned to self.flipped (controlled by keypress)"""
        if self.list_index > len(self.image_list) - 1:
            self.list_index = len(self.image_list) - 1
        if self.flipped:
            self.image = pygame.transform.flip(self.image_list[self.list_index], False, True)

    def climb(self):
        """ Allows the player to climb ledge fungi. """
        if pygame.sprite.spritecollide(self, self.room.can_climb, False):
            self.change_y = -5
 
    def update(self):
        """ Update the player position. """

        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x
        
        # You only get to talk once.
        self.talked = False

        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.room.wall_list, False)
        for block in block_hit_list:
            # Check if it is deadly
            if block.mortality == True:
                self.wound += 50
            else:
                # If we are moving right, snap our right side to the left side of
                # the item we hit
                if self.change_x > 0:
                    self.rect.right = block.rect.left
                else:
                    # Otherwise if we are moving left, do the opposite.
                    self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.room.wall_list, False)
        for block in block_hit_list:
            # Check if it's deadly ISUE: You can survive lava if you're at the bottom of a lake
            if block.mortality == True:
                self.wound += 50

            else:
                # Reset our position based on the top/bottom of the object.
                if self.change_y > 0:
                    self.rect.bottom = block.rect.top
                else:
                    self.rect.top = block.rect.bottom

                    # Stop our vertical movement
                self.change_y = 0

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

        # Check if we're hitting a dangerous enemy
        enemy_hit_list = pygame.sprite.spritecollide(self, self.room.enemy_list, False)
        for enemy in enemy_hit_list:
            if enemy.mortality == True:
                self.wound += 10

        # Kill player if he's beyond max_wound or max_drown
        if self.wound > self.max_wound or self.drown > self.max_drown:
            self.kill()

        # Update corruption and flipped status
        self.how_corrupt()
        self.draw_flipped()

        # Turn off death for easier debugging
        death = True
        if not death:
            self.wound = 0

    def __str__(self):
        # Used in Text
        return 'Player'

class Enemy(Living):
    """ This is the base class for anything that is alive and should move that isn't the player. """
    def __init__(self, x, y, width, height, end_x, speed = -2, mortality = True):
        """ x = upper left corner x component
            y = upper left corner y component
            width = x dimension
            height = y dimension 
            speed = how quickly it moves in the x direction
            distance = how far it can walk
            mortality = does it kill you? """

        # Set the range of values it can go between
        self.start_x = x - width
        self.end_x = end_x

         # Call the parent's constructor
        Living.__init__(self, self.start_x, y, width, height, 'png/enemy.png', speed)

        # Set speed vector
        self.speed = abs(speed)
        self.change_x = speed
        self.change_y = 0

        self.mortality = mortality
        self.text = ['MONSTER: Rawr!', 'MONSTER: Rawr!', 'MONSTER: Rawr!']
        self.talk_length = 60

        self.near_player = False

    def update(self):
        """ Update the enemy position. """
        # Gravity
        self.calc_grav()
        # Move left/right
        self.rect.x += self.change_x
        # If you talked last time, you don't talk this time
        self.talked = False
        #Check if you're on the same level as the player and close to the player
        if (abs(self.room.player.rect.centerx - self.rect.centerx) <= 300 and
            self.room.player.rect.bottom == self.rect.bottom):
            # Move towards him ISSUE: Enemy occasionally teleport far away and disappears
            self.change_x = sign(self.room.player.rect.centerx - self.rect.centerx)*self.speed*1.5
            if not self.near_player:       # If I wasn't near him last step
                self.talked = True
            self.near_player = True
        else:
            #Reset your speed if you choose to change it
            self.change_x = sign(self.change_x)*self.speed
            self.near_player = False
 
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
        if self.rect.x <= self.end_x:
            self.change_x = self.speed
        elif self.rect.x >= self.start_x:
            self.change_x = -self.speed
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

    def __str__(self):
        return 'Enemy'

class Friend(Enemy):
    """ A class of living creatures that will not kill you. Currently, it does not move."""
    def __init__(self, x, y, width, height, not_used, image_file_name):
        """ x = upper left corner x component
            y = upper left corner y component
            width = x dimension
            height = y dimension 
            image_file_name = the image wanted for the friend.
            The friend does not move, so speed and distance are 0 and mortality is False"""
        Enemy.__init__(self, x, y, width, height, 0, 0, False)
        self.image = pygame.image.load(image_file_name).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.near_player = False
        self.talk_length = 180

    def update(self):
        self.calc_grav()
        self.talked = False

        # Talks to you if you are within a certain distance
        if abs(self.room.player.rect.centerx - self.rect.centerx) <= 150:
            if not self.near_player:
                self.talked = True
            self.near_player = True
        else:
            self.near_player = False

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

    def __str__(self):
        return 'Friend'

class AdultDuck(Friend):
    """ Makes an Adult Duck. No difference in corruption, just a different image and default size."""
    def __init__(self, x, y, width = 100, height = 100, not_used = 0):
        self.width = width
        self.height = height
        Friend.__init__(self, x, y, self.width, self.height, not_used, "png/adult_duck.png")
        self.text = ["DUCK: I'm sorry, but you can't stay with us. Good luck.",
                    "DUCK: Ugh! Leave us alone, you don't belong with us!",
                    "DUCK: Get away, you monster! We don't want you here!"]

class ChildDuck(Friend):
    """ Baby Duck. Smaller than Adult. """
    def __init__(self, x, y, width = 75, height = 75, not_used = 0):
        self.width = width
        self.height = height
        Friend.__init__(self, x, y, self.width, self.height, not_used, "png/child_duck_friend.png")
        self.text = ["BABY DUCK: Hi! Wanna play?",
                    "BABY DUCK: Uh... what's that on your head?",
                    "BABY DUCK: Eek! Get away! MOMMY!"]

class Log(Enemy):
    """ Unmoving enemy class, does not block or harm. """
    def __init__(self, x, y, width = 100, height = 100, not_used = 0):
        Enemy.__init__(self, x, y, width, height, not_used, speed = 0, mortality = False)
        self.text = ["Shhhh, it's sleeping", "Hah, it can't see us coming!", "This just makes it easier!"]

class Edible(pygame.sprite.Sprite):
    """ This is the base class; any new foods should be modified from this one. """
    def __init__(self, x, y, width, height, corr_points = 1, health_points = 50):
        """ Constructor for the wall that the player can run into. """
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Set the visual
        self.image = pygame.image.load('png/edible.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))

        # Set parameters
        self.corr_points = corr_points
        self.health_points = health_points

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

class FriendEdible(Edible):
    """ This is an edible food that only comes from when you have killed a friendly creature. """
    def __init__(self, x, y, width, height):
        Edible.__init__(self, x, y, width, height, 5, 150)