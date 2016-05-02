import math, sys
import pygame
from pygame.locals import *
"""This file contains all the HUD elements. These are all drawn onto the screen itself (not the world) after everything else has been drawn to it. So,
in the current framework, HUD is drawn over characters and spores and all that junk."""

class HUD_Object(pygame.sprite.Sprite):
	def __init__(self, view, player):
		pygame.sprite.Sprite.__init__(self)
		self.view, self.player = view, player


class Text(HUD_Object):
	# This guy should always draw above the player.
	def __init__(self, view, player, words, duration, speaker):
		HUD_Object.__init__(self, view, player)
		drawing_font = pygame.font.Font(pygame.font.get_default_font(), 18)
		self.image = drawing_font.render(words, True, pygame.Color('black'), pygame.Color('azure3'))
		self.rect = self.image.get_rect()
		self.timer = duration
		self.speaker = speaker
		self.words = words
		#self.size = drawing_font.size(words)
	
	def update(self):
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
	# This should be drawn on the left side of the screen, with red marking how much health is left
	def __init__(self, player):
		pygame.sprite.Sprite.__init__(self)
		self.player = player
		self.max = self.player.max_wound/5
		self.current = self.max - self.player.wound/5
		self.health_diff = self.player.wound/5
		self.image = pygame.Surface((24, self.max+4))
		self.image.fill((0,0,0))

		self.rect = self.image.get_rect()
		self.rect.centery = 300
		self.rect.x = 20

		self.inner_rect = pygame.Rect(2, 2, 20, self.current)
		self.inner_rect.centery = self.rect.centery
		self.inner_rect.bottom = self.rect.bottom-2
		#pygame.draw.rect(self.image, (255,0,0), self.inner_rect)

	def update(self):
		self.inner_rect.height = self.max - self.player.wound/5
		self.inner_rect.top = 2+self.player.wound/5
		self.image.fill((0, 0, 0))
		self.image.fill((255,0,0), self.inner_rect)
