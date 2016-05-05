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

class Button(object):
    """ Each button in the menu is a Button object. """
    def __init__(self, text, position):
        self.text = text
        self.position = position
        self.hovered = False
        self.make_button()

    def color(self):
        # Determines the color of the button depending on whether the mouse is over it
        if self.hovered:
            return (0, 0, 0)
        else:
            return (100, 100, 200)
    
    def make_button_params(self):
        # Defines parameters for the button
        font = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.button_surf = font.render(self.text, True, self.color(), pygame.Color('red'))

    def make_button(self):
        # Makes the bounding rect for the button that allows you to check its collisions with the mouse
        self.make_button_params()
        self.rect = self.button_surf.get_rect()
        self.rect.center = self.position

    def draw(self, screen):
        self.make_button_params()
        screen.blit(self.button_surf, self.rect)

    def pressed(self):
        return self.text

class Menu(object):
    """ Menu object contains a number of buttons and draws them onto the screen. """
    def __init__(self, menu_on):
        self.menu_on = menu_on

        button_width = 300
        self.buttons = []

    def make_buttons(self, names):
        # Evenly spaces the buttons based on how many there are.
        start = 100
        spacing = (SCREEN_HEIGHT - 200)/len(names)
        for number, name in enumerate(names):
            self.buttons.append(Button(name, (SCREEN_WIDTH/2, start + (spacing*number))))

    def draw(self, screen):
        if self.menu_on:
            screen.fill(BLACK) 
            for button in self.buttons:
                button.draw(screen)


