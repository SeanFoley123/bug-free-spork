import math, sys
import pygame
from pygame.locals import *

class View(object):
	### The room object in the model keeps track of the positions of all the things, and the view needs to draw them in 
	### the right places. It should keep track of its own position (top left corner) relative to the top left of the current room too.
	def __init__(self, model, screen_size):
		# Model is the big container, and screen_size is a tuple (width, height)
		self.model = model
		self.screen_size = screen_size
		self.screen = pygame.display.set_mode(screen_size)
		self.position = (0, self.model.current_room.room_size[1] - self.screen_size[1])

	def update(self):
		self.screen.blit(self.model.current_room.background, (-self.position[0], -self.position[0]))
		pygame.display.update()