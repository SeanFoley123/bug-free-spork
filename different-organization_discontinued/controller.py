import math, sys
import pygame
from pygame.locals import *

class Controller(object):
	def __init__(self, model):
		self.model = model

	def update(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()