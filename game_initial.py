import math
import pygame
from pygame.locals import *

class Room(object):
	def __init__(self):
		pass
	def update(self):
		pass

class Room1(Room):
	pass


class Walking_things(object):
	###Defines basic movement for things that can move/jump


class Mushroom_Guy(Walking_things):
	pass


class View(object):
	### The room object in the model keeps track of the positions of all the things, and the view needs to draw them in 
	### the right places. It should keep track of its own position relative to the top left of the current room too.
	def __init__(self, model, screen_size):
		# Model is the big container, and screen_size is a tuple (width, height)
		self.model = model
		self.screen_size = screen_size


class Controller(object):
	def __init__(self, model):
		pass


class Model(object):
	### Contains the controller, the view, the current room, and the mushroom guy. Keeps track of the current room.
	### Changes self.currentroom when told to, and puts the mushroom guy in the currentroom.
	def __init__(self):
		# Need some kind of spatially-organized list of rooms/levels
		# Need a mushroom guy
		# Need a current room
		# Need a viewer of the proper size and a controller
		screen_size = (800, 600)
		view = View(self, screen_size)

	def update(self):
		pass		

	def change_room(self, direction):
		pass


def main():
	pygame.init()
	clock = pygame.time.Clock()
	model = Model()
	running = True
	while running:
		clock.tick(60)
		model.update()