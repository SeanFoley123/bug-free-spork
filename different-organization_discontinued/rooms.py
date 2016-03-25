import math, sys
import pygame
from pygame.locals import *

class Room(object):
	### Assumes you make a self.objects_list in your __init__. 
	def update(self):
		pass


class Room1(Room):
	### Needs to be specialized for the particular arrangement of things in it; should have a list of objects, which will
	### keep track of their own position, a room size, and a background picture.
	def __init__(self, hero):
		self.room_size = (3000, 1000)
		self.background = pygame.Surface(self.room_size)
		self.background.fill(pygame.Color('blue'))


class Room2(Room):
	def __init__(self, hero):
		pass	