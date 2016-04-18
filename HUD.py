import math, sys
import pygame
from pygame.locals import *
"""This file contains all the HUD elements. These are all drawn onto the screen itself (not the world) after everything else has been drawn to it. So,
in the current framework, HUD is drawn over characters and spores and all that junk."""

class HUD_Object(object):
	def __init__(self, view, player):
		self.view, self.player = view, player


class Text(HUD_Object):
	# This guy should always draw above the player.
	def __init__(self, view, player, words):
		HUD_Object.__init__(self, view, player)
		drawing_font = pygame.font.Font(pygame.font.get_default_font(), 18)
		self.text = drawing_font.render(words, True, pygame.Color('black'), pygame.Color('azure3'))
		self.size = drawing_font.size(words)
	
	def update(self):
		self.center = (self.player.rect.centerx - self.view.position[0] - self.size[0]/2,
		self.player.rect.centery - self.player.rect.h - self.view.position[1] - self.size[1]/2)

	def draw(self):
		self.view.screen.blit(self.text, self.center)