import math, sys, pickle
import pygame
from pygame.locals import *
from Spores import *
from LivingThings import *
from Terrain import *
from Room import *
from HUD import *
from Menu import *
from Intro import *
from collections import OrderedDict

# -- Global constants
 
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_W_MID = SCREEN_WIDTH/2
SCREEN_H_MID = SCREEN_HEIGHT/2

class Controller(object):
    """ Controller is responsible for updating the object in the room and handling all user input. """
    def __init__(self, menu):
        # Dictionary of all potential spores
        self.spores_dict = {pygame.K_q: 0, pygame.K_e: 1}
        # Create the player
        self.player = MushroomGuy()
     
        # Create all the levels
        self.room_list = []

        self.room_list.append( Room_00(self.player) )
        self.room_list.append( Room_01(self.player) )
        self.room_list.append( Room_02(self.player) )
 
        # Set the first level
        self.current_room_no = 0
        self.change_room(0)
 
        self.active_sprite_list = pygame.sprite.Group()
        self.active_sprite_list.add(self.player)

        # Loop until the user clicks the close button.
        self.done = False

        # Initialize pause menu
        self.menu = menu
        self.menu_dict = OrderedDict([('Resume', self.resume), ('New Game', main), ('Quit Game', self.quit_game)])
        self.menu.make_buttons(self.menu_dict.keys())

        # Put in all the HUD components
        self.hud_components = pygame.sprite.Group()
        self.hud_components.add(HealthBar(self.player))
        self.spore_box = Spore_Boxes(self.current_room)
        self.hud_components.add(self.spore_box)


    def update(self, other):
        # Main update loop, occurs 60 times a second
        # Check through every user input event that pygame recognized this clock cycle
        for event in pygame.event.get():
            # Handle closing the program
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

            # Handle user input while the game is playing, aka the pause menu is not active
            if not self.menu.menu_on: 
                if event.type == pygame.KEYDOWN:

                    # Changing active spore
                    if event.key in self.spores_dict:
                        self.spore_box.change()
                        self.current_room.active_spore = self.current_room.spore_list[self.spores_dict[event.key]]
                        self.spore_box.change()

                    # Shooting a spore
                    if event.key == pygame.K_SPACE:
                        spore = self.current_room.active_spore(self.player)
                        spore.room = self.current_room
                        spore.setup_lists()
                        self.active_sprite_list.add(spore)

                    # Toggling the flip state
                    if event.key == pygame.K_f:
                        self.player.flipped = not self.player.flipped

                    # Talk to your mushroom hat
                    if event.key == pygame.K_t:
                        self.player.talked = True

                    # Eat mushrooms
                    if event.key == pygame.K_DOWN:
                        food_hit_list = pygame.sprite.spritecollide(self.player, self.current_room.consumeable, False)
                        if food_hit_list:
                            food = food_hit_list[0]
                            self.player.corruption += food.corr_points
                            self.player.wound = max(0, self.player.wound - food.health_points)
                            food.kill()

                # Stop the player from moving when you release the movement keys
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and self.player.change_x < 0:
                        self.player.stop()
                    if event.key == pygame.K_RIGHT and self.player.change_x > 0:
                        self.player.stop()

            # If the pause menu is active, user input doesn't change the current room at all, but causes different effects
            else:
                # Check through every option in the menu to see if it's hovered over and if it's being pressed
                for button in self.menu.buttons:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        button.hovered = True
                        if pygame.mouse.get_pressed()[0]:
                            x = button.pressed()
                            self.menu_dict[x]()                 # Execute the action specified by the button
                    else:
                        button.hovered = False

            # Toggle the pause menu
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    self.menu.menu_on = not self.menu.menu_on

        # Additional update code to be run if the pause menu is not active
        if not self.menu.menu_on:
            # Player movement
            if pygame.key.get_pressed()[pygame.K_UP]:
                self.player.climb()
            if pygame.key.get_pressed()[pygame.K_LEFT]: 
                self.player.go_left()
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.player.go_right()
                        
            # Check who in the room has talked this step and display the most important message
            talkers = ([creature for creature in self.current_room.enemy_list if creature.talked] + [player for player in [self.player] if player.talked]
                      + [tut for tut in [self.current_room.tutorial] if self.current_room.is_tutorial])
            for talker in talkers:
                # In the tutorial, the text to display is determined by the players current position
                if isinstance(talker, Tutorial):
                    self.hud_components.add(Text(other, self.player, talker.text[self.player.rect.x/500], talker.talk_length, talker.__str__()))
                # Otherwise, it's determined by the player's corruption level
                else:
                    self.hud_components.add(Text(other, self.player, talker.text[self.player.list_index], talker.talk_length, talker.__str__()))
            if talkers:
                # This bit removes all but the most important message. In the event of a tie, it removes the earlier message.
                messages = [message for message in self.hud_components if isinstance(message, Text)]
                most_important = max(messages)
                self.hud_components.remove([message for message in messages if message.words != most_important.words])
            
            # Update the player.
            self.active_sprite_list.update()

            # Update items in the level
            self.current_room.update()

            # Stop the player from going off the sides
            self.player.rect.centerx = min(max(self.player.rect.centerx, self.player.rect.w/2), self.current_room.world_size[0]-self.player.rect.w/2)

            # Update the HUD
            for piece in self.hud_components:
                piece.update()

            # Move to the next room if you reach the far right side of this room
            if self.player.rect.right == self.current_room.world_size[0] and self.current_room != self.room_list[-1]:
                self.change_room(self.current_room.next_level)

    def change_room(self, direction):
        # Adds direction to current_room_no and initializes our new room
        self.current_room_no += direction
        self.current_room = self.room_list[self.current_room_no]

        # Initialize the objects in the room
        for enemy in self.current_room.enemy_list:
            enemy.room = self.current_room

        # Put the player in the new room
        self.player.room = self.current_room
        self.player.rect.x = 0
        self.player.rect.y = 0

    def save(self):
        # Save the current state of the game. Not yet tested.
        save_values = {'current_room':self.current_room, 'player':self.player}
        f = open('save_file', 'w')
        pickle.dump(save_values, f)
        f.close()

    def open(self):
        # Load a previous game. Not yet tested.
        f = open('save_file')
        save_values = pickle.load(f)
        f.close()
        self.current_room = self.save_values['current_room']
        self.player = self.save_values['player']

    def resume(self):
        # Restart the game if the player is dead, otherwise just close the pause menu
        if self.player not in self.active_sprite_list:
            main()
        self.menu.menu_on = False

    def quit_game(self):
        self.done = True

class View(object):
    """ View is responsible for drawing everything in the current gameworld. It blits (pastes) the pygame surface representing the game world, world, onto
    the surface representing the viewing window, screen, every step. """
    def __init__(self, screen, menu):
        self.screen = screen

        # Where relative to the screen the world should be blit
        self.position = (0, 0)

        self.menu = menu
        self.end_timer = 0
        self.end_timer_max = 120

    def update(self, other):
            # If the player is dead, draw the game over screen
            if other.player not in other.active_sprite_list:
                self.draw_end()
                self.end_timer += 1
                # After end_time_max clock ticks, put in the pause menu (eventually a game over menu)
                if self.end_timer >= self.end_timer_max:
                    other.menu.menu_on = True
            else:
                other.current_room.draw()
                other.active_sprite_list.draw(other.current_room.world)
                # Position tracks the top left corner of the screen relative to the world. It should always be positive and no greater
                # than the w/h of the world minus the w/h of the screen.
                self.position = (min(max(0, other.player.rect.centerx - SCREEN_W_MID), other.current_room.world_size[0]-SCREEN_WIDTH),
                    min(max(0, other.player.rect.centery - SCREEN_H_MID), other.current_room.world_size[1]-SCREEN_HEIGHT))
                # Blit the background, whose coordinate in the world coordinate system is (0, 0), at the negative of your position.
                self.screen.blit(other.current_room.world, (-self.position[0], -self.position[1]))
                other.hud_components.draw(self.screen)
            self.menu.draw(self.screen)
            # Useful debugging tool below: prints current mouse position
            #print (self.position[0] + pygame.mouse.get_pos()[0], self.position[1] + pygame.mouse.get_pos()[1])

            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

    def draw_end(self):
        # Draw the game over screen.
        self.screen.fill(BLACK) 
        game_over_pic = pygame.transform.scale(pygame.image.load('game_over_mushroom.jpg').convert(), [350, 350])
        self.screen.blit(game_over_pic, (SCREEN_W_MID-175, SCREEN_H_MID-175))

def main():
    # Initialize all the main components of the game
    pygame.init()
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    menu = Menu(False)
    view = View(screen, menu)
    controller = Controller(menu)

    while not controller.done:
        controller.update(view)
        view.update(controller)
        clock.tick(60)

    pygame.quit()


# This block of code runs the introductory sequence
pygame.init()
clock = pygame.time.Clock()
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)
     
pygame.display.set_caption("Symbiosis")
run(screen, clock)
# Once run() is done playing the intro sequence, start the actual game
main()