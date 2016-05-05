import math, sys
import pygame
from pygame.locals import *
"""This file contains all the HUD elements. These are all drawn onto the screen itself (not the world) after everything else has been drawn to it. So,
in the current framework, HUD is drawn over characters and spores and terrain. """

class HUD_Object(pygame.sprite.Sprite):
	""" Base class for parts of the HUD. """
	def __init__(self, view, player):
		pygame.sprite.Sprite.__init__(self)
		self.view, self.player = view, player


class Text(HUD_Object):
	""" Text displayed at the bottom of the screen. """
	def __init__(self, view, player, words, duration, speaker):
		HUD_Object.__init__(self, view, player)

		# Initialize font and draw it with the given words
		drawing_font = pygame.font.Font(pygame.font.get_default_font(), 18)
		self.image = drawing_font.render(words, True, pygame.Color('black'), pygame.Color('azure3'))

		# Duration means how long the message stays on the screen in clock ticks
		self.timer = duration

		# Set parameters: rectangle for positioning, words for string, and speaker for order of importance
		self.rect = self.image.get_rect()
		self.speaker = speaker
		self.words = words
	
	def update(self):
		""" Keeps the words at the bottom of the screen and keeps track of time. """
		self.rect.center = (400, 550)
		self.timer -= 1
		if self.timer <= 1:
			self.kill()

	def __cmp__(self, other):
		# Ascending order of importance: Monster, Mushroom Hat, Friendly
		if self.speaker == other.speaker:
			return -1    #This will always make it return the last entry in a list.
		elif self.speaker == 'Enemy' and (other.speaker == 'Player' or other.speaker == 'Friend'):
			return -1
		elif self.speaker == 'Player' and other.speaker == 'Friend':
			return -1
		else:
			return 1

	def __str__(self):
		return self.words

class HealthBar(pygame.sprite.Sprite):
	""" A red on black health bar drawn on the left side of the screen. """
	def __init__(self, player):
		# Set the height and position of the red surface,
		# inner_rect, based on the player's current wound value.
		pygame.sprite.Sprite.__init__(self)
		self.player = player
		self.max = self.player.max_wound/5
		self.current = self.max - self.player.wound/5
		self.health_diff = self.player.wound/5

		# image is slightly larger than the red bar at max, in order to have a border of 2 px
		self.image = pygame.Surface((24, self.max+4))
		self.image.fill((0,0,0))

		# puts it on the left side of the screen, halfway up the side
		self.rect = self.image.get_rect()
		self.rect.centery = 300
		self.rect.centerx = 32

		# creates the red health bar inside the black boundary
		self.inner_rect = pygame.Rect(2, 2, 20, self.current)
		self.inner_rect.centery = self.rect.centery
		self.inner_rect.bottom = self.rect.bottom-2

	def update(self):
		# Update based on changing wound values, blits the new over the old
		self.inner_rect.height = self.max - self.player.wound/5
		self.inner_rect.top = 2+self.player.wound/5
		self.image.fill((0, 0, 0))
		self.image.fill((255,0,0), self.inner_rect)

class Spore_Boxes(pygame.sprite.Sprite):
	""" A class that contains all the possible spore indicators. """
	def __init__(self, current_room):
		pygame.sprite.Sprite.__init__(self)

		# List of all possible spores
		self.spores = [One_Spore('q'), One_Spore('e')]
		self.image = pygame.Surface((32, 84))
		self.image.set_colorkey((0,0,0))	# Makes the default color of a surface, black, into transparent

		# Draws each OneSpore onto self.image
		for index, spore in enumerate(self.spores):
			self.image.blit(spore.image, (0, 52*index))

		self.rect = self.image.get_rect()
		self.rect.centerx = 32
		self.rect.y = 420
		self.current_room = current_room

	def change(self):
		# Updates the currently boxed OneSpore based on the current spore selected in current_room
		self.spores[self.current_room.spore_list.index(self.current_room.active_spore)].change_state()
		self.image = pygame.Surface((32, 84))
		self.image.set_colorkey((0,0,0))
		for index, spore in enumerate(self.spores):
			self.image.blit(spore.image, (0, 52*index))

class One_Spore(pygame.sprite.Sprite):
	""" Each spore indicator. The currently selected spore is boxed in blue. """
	def __init__(self, key):
		# Key means which key each spore corresponds to
		self.key = key

		self.image_unselect = pygame.Surface((32, 32))
		self.image_select = pygame.Surface((32, 32))

		colors_dict = {'q':pygame.Color('chartreuse3'), 'e':pygame.Color('darkgoldenrod4')}
		
		self.image_unselect.fill(colors_dict[key], pygame.Rect(10, 10, 14, 14))
		self.image_select.fill(colors_dict[key], pygame.Rect(10, 10, 14, 14))
		pygame.draw.rect(self.image_select, pygame.Color('cyan'), pygame.Rect(0, 0, 32, 32), 2)

		# By default, q, the devour spore, is selected
		if key == 'q':
			self.selected = True
		else:
			self.selected = False

		if self.selected:
			self.image = self.image_select
		else:
			self.image = self.image_unselect

	def change_state(self):
		self.selected = not self.selected
		if self.selected:
			self.image = self.image_select
		else:
			self.image = self.image_unselect