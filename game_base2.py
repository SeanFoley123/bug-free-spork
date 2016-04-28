import math, sys, pickle
import pygame
from pygame.locals import *
from Spores import *
from LivingThings import *
from Terrain import *
from Room import *
from HUD import *

# -- Global constants
 
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_W_MID = SCREEN_WIDTH/2
SCREEN_H_MID = SCREEN_HEIGHT/2

# Save files would not be hard, especially with pickling
# Really important: we need to be consistent on how we define positions. Right now I'm using relative to the upper left hand 
# corner of the current room. All sprites are defined at the center of their bounding rectangles, which might make rolling
# over easier.

class Controller(object):
    """ Main Program """
    def __init__(self):
        # Dictionary of all potential spores
        self.spores_dict = {pygame.K_q: 0, pygame.K_e: 1}
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

    def update(self, other):
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

                if event.key in self.spores_dict:
                    # Switches the active projectile spore to the ledge-maker
                    self.current_room.active_spore = self.current_room.spore_list[self.spores_dict[event.key]]

                if event.key == pygame.K_SPACE:
                    spore = self.current_room.active_spore(self.player)
                    spore.room = self.current_room
                    spore.setup_lists()
                    self.active_sprite_list.add(spore)

                #toggles the flip state
                if event.key == pygame.K_f:
                    self.player.flipped = not self.player.flipped
                    #print self.player.flipped

                # Talk
                if event.key == pygame.K_t:
                    other.hud_components.append(Text(other, self.player, 'hullabaloo'))

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and self.player.change_x < 0:
                    self.player.stop()
                if event.key == pygame.K_RIGHT and self.player.change_x > 0:
                    self.player.stop()
        # Checks if c is pressed, and climbs if it is
        if pygame.key.get_pressed()[pygame.K_c]:
            self.player.climb()
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.player.go_left()
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.player.go_right()
        # Update the player.
        self.active_sprite_list.update()
 
        # Update items in the level
        self.current_room.update()

        # Stop the player from going off the sides
        self.player.rect.centerx = min(max(self.player.rect.centerx, self.player.rect.w/2), self.current_room.world_size[0]-self.player.rect.w/2)

        # Update the HUD
        for piece in other.hud_components:
            piece.update()
          
    def change_room(self, direction):
        # Adds direction to current_room_no and initializes our new room
        self.current_room_no += direction
        self.current_room = self.room_list[self.current_room_no]

        for enemy in self.current_room.enemy_list:
            enemy.room = self.current_room

        self.player.room = self.current_room
        self.player.rect.x = 0
        self.player.rect.y = 0

    def save(self):
        save_values = {'current_room':self.current_room, 'player':self.player}
        f = open('save_file', 'w')
        pickle.dump(save_values, f)
        f.close()

    def open(self):
        f = open('save_file')
        save_values = pickle.load(f)
        f.close()
        self.current_room = self.save_values['current_room']
        self.player = self.save_values['player']

class View(object):
    def __init__(self):
        # Set the height and width of the screen
        size = [SCREEN_WIDTH, SCREEN_HEIGHT]
        self.screen = pygame.display.set_mode(size)
     
        pygame.display.set_caption("Jump Jump Jump")

        # Where relative to the screen the world should be blit
        self.position = (0, 0)

        # Put in all the HUD bits
        self.hud_components = []

    def update(self, other):
            # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
            if other.player not in other.active_sprite_list:
                self.draw_end()
            else:
                other.current_room.draw()
                other.active_sprite_list.draw(other.current_room.world)
                # Position tracks the top left corner of the screen relative to the world. It should always be positive and no greater
                # than the w/h of the world minus the w/h of the screen.
                # self.position = (min(max(SCREEN_W_MID-other.player.rect.centerx, 0), SCREEN_WIDTH - other.current_room.world_size[0]),
                # min(max(SCREEN_H_MID-other.player.rect.centery, 0), SCREEN_HEIGHT - other.current_room.world_size[1]))
                self.position = (min(max(0, other.player.rect.centerx - SCREEN_W_MID), other.current_room.world_size[0]-SCREEN_WIDTH),
                    min(max(0, other.player.rect.centery - SCREEN_H_MID), other.current_room.world_size[1]-SCREEN_HEIGHT))
                # Now you blit the background, whose coordinate in the world coordinate system is (0, 0), at the negative of your position.
                self.screen.blit(other.current_room.world, (-self.position[0], -self.position[1]))
                for piece in self.hud_components:
                    piece.draw()

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
        # We should not have to feed view into controller and controller into view. Either all those lists should be contained in room,
        # or they should be contained in some larger model class. I'd opt for the latter.
        controller.update(view)
        view.update(controller)
        # Limit to 60 frames per second
        clock.tick(60)

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()

    #view.play()
