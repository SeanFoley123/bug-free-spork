#import math, sys
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
    
    def __init__(self, text, position):
        self.text = text
        self.position = position
        self.hovered = False
        self.make_button()


    #determines the color of the button depending on whether the mouse is over it
    def color(self):
        if self.hovered:
            return (0, 0, 0)
        else:
            return (100, 100, 200)
    
    #defines parameters for the button
    def make_button_params(self):
        font = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.button_surf = font.render(self.text, True, self.color(), pygame.Color('red'))
        #self.button_params = (self.text, True, self.color())

    #makes the rect for the button
    def make_button(self):
        self.make_button_params()
        self.rect = self.button_surf.get_rect()
        self.rect.center = self.position

    def draw(self, screen):
        self.make_button_params()
        screen.blit(self.button_surf, self.rect)

    def pressed(self):
        return self.text

class Menu(object):
    
    def __init__(self, menu_on):
        self.menu_on = menu_on

        button_width = 300
        self.buttons = []
        # self.buttons = [Button("New Game", (SCREEN_WIDTH/2, 100)),
        #                 Button("Continue", (SCREEN_WIDTH/2, 200)),
        #                 Button("Quit Game", (SCREEN_WIDTH/2, 300)),
        #                 Button("Resume", (SCREEN_WIDTH/2, 400))]
    
    def make_buttons(self, names):
        start = 100
        spacing = (SCREEN_HEIGHT - 200)/len(names)
        for number, name in enumerate(names):
            self.buttons.append(Button(name, (SCREEN_WIDTH/2, start + (spacing*number))))

    def draw(self, screen):
        if self.menu_on:
            screen.fill(BLACK) 
            for button in self.buttons:
                button.draw(screen)


