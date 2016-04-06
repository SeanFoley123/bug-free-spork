import math, sys
import pygame
from pygame.locals import *

# -- Global constants
 
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
 
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Save files would not be hard, especially with pickling
# Really important: we need to be consistent on how we define positions. Right now I'm using relative to the upper left hand 
# corner of the current room. All sprites are defined at the center of their bounding rectangles, which might make rolling
# over easier.

class MushroomGuy(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
    controls. """
 
    # Constructor function
    def __init__(self):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
 
        # Set height, width
        self.image = pygame.image.load('dog.jpg')
        self.image = pygame.transform.scale(self.image, (100, 75))
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = 0
        self.rect.x = 0
 
        # Set speed vector
        self.change_x = 0
        self.change_y = 0

        # List of sprites we can bump against
        self.room = None
 
    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6
 
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
        """ Update the player position. """
        # Gravity
        self.calc_grav()
        # Move left/right
        self.rect.x += self.change_x
 
        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.room.wall_list, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Did this update cause us to hit a deadly object?
        block_hit_list = pygame.sprite.spritecollide(self, self.room.sludge, False)
        for block in block_hit_list:
        	self.rect.x -= self.change_x*block.visc

        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.room.wall_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

        block_hit_list = pygame.sprite.spritecollide(self, self.room.sludge, False)
        for block in block_hit_list:
        	self.rect.y -= self.change_y*block.visc

        block_hit_list = pygame.sprite.spritecollide(self, self.room.deadlies, False)
        for block in block_hit_list:
            self.kill()
 
class Obstacle(pygame.sprite.Sprite):
    """ Wall the player can run into. """
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
	def __init__(self, x, y, w, h):
		Obstacle.__init__(self, x, y, w, h, 0, False)

		# Make the color and all different
		self.image = pygame.Surface((w, h))
		self.image.fill(pygame.Color('aquamarine4'))

class Lava(Obstacle):
	def __init__(self, x, y, w, h):
		Obstacle.__init__(self, x, y, w, h, .5, False)

		# Make the color correct
		self.image = pygame.Surface((w, h))
		self.image.fill(pygame.Color('chocolate1'))

class Water(Obstacle):
    def __init__(self, x, y, w, h):
        Obstacle.__init__(self, x, y, w, h, .5, False)

        # Make the color correct
        self.image = pygame.Surface((w, h))
        self.image.fill(pygame.Color('cadetblue1'))

class Room(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
 
    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.wall_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.deadlies = pygame.sprite.Group()
        self.sludge = pygame.sprite.Group()
        self.player = player
         
        # Background image
        self.background = None
 
    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.wall_list.update()
        self.enemy_list.update()
        self.deadlies.update()
 
    def draw(self, screen):
        """ Draw everything on this level. """
 
        # Draw the background
        screen.fill(BLUE)
 
        # Draw all the sprite lists that we have
        self.wall_list.draw(screen)
        self.enemy_list.draw(screen)
        self.deadlies.draw(screen)
        self.sludge.draw(screen)
 
 
# Create platforms for the level
class Room_01(Room):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Room.__init__(self, player)
 
        # Array with width, height, x, and y of obstacle
        room = [[500, 50, 0, 550],
                 [200, 30, 200, 400],
                 [200, 30, 500, 300],
                 ]
        deadlies = [[300, 50, 500, 550]]

        sludge = [[300, 100, 400, 350]]
 
        # Go through the array above and add platforms
        for obstacle in room:
            block = Ground(obstacle[2], obstacle[3], obstacle[0], obstacle[1])
            block.rect.x = obstacle[2]
            block.rect.y = obstacle[3]
            block.player = self.player
            self.wall_list.add(block)

        for obstacle in deadly:
 			block = Lava(obstacle[2], obstacle[3], obstacle[0], obstacle[1])
 			block.rect.x = obstacle[2]
 			block.rect.y = obstacle[3]
 			block.player = self.player
 			self.deadlies.add(block)

        for obstacle in sludge:
            block = Water(obstacle[2], obstacle[3], obstacle[0], obstacle[1])
            block.rect.x = obstacle[2]
            block.rect.y = obstacle[3]
            block.player = self.player
            self.sludge.add(block)

def View():
    """ Main Program """
    pygame.init()
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("Jump Jump Jump")
 
    # Create the player
    player = MushroomGuy()
 
    # Create all the levels
    room_list = []
    room_list.append( Room_01(player) )
 
    # Set the current level
    current_room_no = 0
    current_room = room_list[current_room_no]
 
    active_sprite_list = pygame.sprite.Group()
    player.room = current_room
 
    player.rect.x = 0
    player.rect.y = 0
    active_sprite_list.add(player)
 
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
 
    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
 
        # Update the player.
        active_sprite_list.update()
 
        # Update items in the level
        current_room.update()
 
        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH
 
        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left < 0:
            player.rect.left = 0
 
        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_room.draw(screen)
        active_sprite_list.draw(screen)
 
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
 
        # Limit to 60 frames per second
        clock.tick(60)
 
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
 
    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()
 
if __name__ == "__main__":
    View()

# # Call this function so the Pygame library can initialize itself
# pygame.init()
 
# # Create an 800x600 sized screen
# screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
 
# # Set the title of the window
# pygame.display.set_caption('Test')
 
# # List to hold all the sprites
# all_sprite_list = pygame.sprite.Group()
 
# # Make the walls. (x_pos, y_pos, width, height)
# wall_list = pygame.sprite.Group()
 
# wall = Ground(pygame.Rect(0, 0, 10, 600))
# wall_list.add(wall)
# all_sprite_list.add(wall)
 
# wall = Ground(pygame.Rect(10, 590, 600, 10))
# wall_list.add(wall)
# all_sprite_list.add(wall)
 
# wall = Ground(pygame.Rect(10, 200, 100, 10))
# wall_list.add(wall)
# all_sprite_list.add(wall)

# # Make a list of deadly things
# death_list = pygame.sprite.Group()

# lava_patch = Lava(pygame.Rect(600, 590, 200, 10))
# death_list.add(lava_patch)
# all_sprite_list.add(lava_patch)
 
# # Create the player paddle object
# player = MushroomGuy(50, 50)
# player.walls = wall_list
# player.deadlies = death_list
 
# all_sprite_list.add(player)
 
# clock = pygame.time.Clock()
 
# done = False
 
# while not done:
 
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             done = True
 
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_LEFT:
#                 player.changespeed(-3, 0)
#             elif event.key == pygame.K_RIGHT:
#                 player.changespeed(3, 0)
#             elif event.key == pygame.K_UP:
#                 player.changespeed(0, -3)
#             elif event.key == pygame.K_DOWN:
#                 player.changespeed(0, 3)
 
#         elif event.type == pygame.KEYUP:
#             if event.key == pygame.K_LEFT:
#                 player.changespeed(3, 0)
#             elif event.key == pygame.K_RIGHT:
#                 player.changespeed(-3, 0)
#             elif event.key == pygame.K_UP:
#                 player.changespeed(0, 3)
#             elif event.key == pygame.K_DOWN:
#                 player.changespeed(0, -3)
 
#    all_sprite_list.update()
 
#    screen.fill(BLACK)
 
#    all_sprite_list.draw(screen)
 
#    pygame.display.flip()
 
#    clock.tick(60)
 
# pygame.quit()