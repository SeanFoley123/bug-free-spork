import math, sys
import pygame
from pygame.locals import *
from Spores import *
from LivingThings import *
from Terrain import *
from Room import *

# -- Global constants
 
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_W_MID = SCREEN_WIDTH/2
SCREEN_H_MID = SCREEN_HEIGHT/2

# 

# Save files would not be hard, especially with pickling
# Really important: we need to be consistent on how we define positions. Right now I'm using relative to the upper left hand 
# corner of the current room. All sprites are defined at the center of their bounding rectangles, which might make rolling
# over easier.

class Controller(object):
    """ Main Program """
    def __init__(self):
        
        # Create the player
        self.player = MushroomGuy()
     
        # Create all the levels
        self.room_list = []
        self.room_list.append( Room_01(self.player) )
 
        # Set the first level
        self.current_room_no = 0
        self.change_room(0)
 
        self.active_sprite_list = pygame.sprite.Group()
        self.active_sprite_list.add(self.player)

        # Loop until the user clicks the close button.
        self.done = False

    def update(self):
        # -------- Main Program Loop -----------
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.done = True
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.go_left()
                if event.key == pygame.K_RIGHT:
                    self.player.go_right()
                if event.key == pygame.K_UP:
                    self.player.jump()
                if event.key == pygame.K_q:
                    # Switches the active projectile spore into the decomposition spore
                    self.current_room.active_spore = self.current_room.spore_list[0]
                if event.key == pygame.K_e:
                    # Switches the active projectile spore to the ledge-maker
                    self.current_room.active_spore = self.current_room.spore_list[1]
                if event.key == pygame.K_c and self.player.climb_okay == True:
                    self.player.climb()
                if event.key == pygame.K_SPACE:
                    spore = self.current_room.active_spore(self.player)
                    spore.room = self.current_room
                    spore.setup_lists()
                    self.active_sprite_list.add(spore)
                #toggles the flip state
                if event.key == pygame.K_f:
                    self.player.flipped = not self.player.flipped
                    #print self.player.flipped
                if self.player.flipped:
                    self.image = pygame.transform.flip(self.player.image_list[self.player.corruption/5], False, True)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and self.player.change_x < 0:
                    self.player.stop()
                if event.key == pygame.K_RIGHT and self.player.change_x > 0:
                    self.player.stop()
     
        # Update the player.
        self.active_sprite_list.update()
 
        # Update items in the level
        self.current_room.update()
 
        # Stop the player from going off the sides
        self.player.rect.centerx = min(max(self.player.rect.centerx, self.player.rect.w/2), self.current_room.world_size[0]-self.player.rect.w/2)
          
    def change_room(self, direction):
        # Adds direction to current_room_no and initializes our new room
        self.current_room_no += direction
        self.current_room = self.room_list[self.current_room_no]

        for enemy in self.current_room.enemy_list:
            enemy.room = self.current_room

        self.player.room = self.current_room
        self.player.rect.x = 0
        self.player.rect.y = 0

class View(object):
    def __init__(self):
        # Set the height and width of the screen
        size = [SCREEN_WIDTH, SCREEN_HEIGHT]
        self.screen = pygame.display.set_mode(size)
     
        pygame.display.set_caption("Jump Jump Jump")

        # Where relative to the screen the world should be blit
        self.position = (0, 0)

    def update(self, other):
            # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
            if other.player not in other.active_sprite_list:
                self.draw_end()
            else:
                other.current_room.draw()
                other.active_sprite_list.draw(other.current_room.world)
                self.position = (max(min(SCREEN_W_MID-other.player.rect.centerx, 0), SCREEN_WIDTH - other.current_room.world_size[0]),
                max(min(SCREEN_H_MID-other.player.rect.centery, 0), SCREEN_HEIGHT - other.current_room.world_size[1]))
                self.screen.blit(other.current_room.world, self.position)
            # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

    def draw_end(self):
        """ Draw the game over screen. """
        self.screen.fill(BLACK) 
        game_over_pic = pygame.transform.scale(pygame.image.load('game_over_mushroom.jpg').convert(), [350, 350])
        self.screen.blit(game_over_pic, (SCREEN_W_MID-175, SCREEN_H_MID-175))

if __name__ == "__main__":
    pygame.init()
        
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    view = View()
    controller = Controller()

    while not controller.done:
        controller.update()
        view.update(controller)
        # Limit to 60 frames per second
        clock.tick(60)

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()

    #view.play()
