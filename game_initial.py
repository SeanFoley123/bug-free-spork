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
	def __init__(self):
		pass


class Room2(Room):
	def __init__(self):
		pass	


class Walking_things(object):
	###Defines basic movement for things that can move/jump
	pass

class Mushroom_Guy(Walking_things):
	### He moves, he shoots spores. I guess he needs to decide if he's just a funky little furry guy or a guy with a
	### mushroom.
	def __init__(self):
		# Possible variables: corruption, position, weight, power, flipped/not flipped, health
		pass


class View(object):
	### The room object in the model keeps track of the positions of all the things, and the view needs to draw them in 
	### the right places. It should keep track of its own position relative to the top left of the current room too.
	def __init__(self, model, screen_size):
		# Model is the big container, and screen_size is a tuple (width, height)
		self.model = model
		self.screen_size = screen_size
		self.screen = pygame.display.set_mode(screen_size)
		self.position = (0, 0)

	def update(self):
		pass


class Controller(object):
	def __init__(self, model):
		self.model = model

	def update(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()


class Model(object):
	### Contains the controller, the view, the current room, and the mushroom guy. Keeps track of the current room.
	### Changes self.currentroom when told to, and puts the mushroom guy in the current room. I think it might make sense
	### to do all the collision checking junk in the room instances.
	def __init__(self):
		# Need some kind of spatially-organized list of rooms/levels
		# Need a mushroom guy
		# Need a current room
		# Need a viewer of the proper size and a controller
		self.controller = Controller(self)

		screen_size = (800, 600)
		self.view = View(self, screen_size)

		self.hero = Mushroom_Guy()

		self.room_list = [Room1(), Room2()]
		self.current_room = self.room_list(0)

	def update(self):
		self.controller.update()
		self.view.update()

	def change_room(self, direction):
		try:
			self.current_room = self.room_list.index(self.current_room) + direction
		except:
			print "You can't go there! What have you done you foolish programmer? You've doomed us all!"
			pygame.quit()
			sys.exit()


def main():
	pygame.init()
	clock = pygame.time.Clock()
	model = Model()
	running = True
	while running:
		clock.tick(60)
		model.update()

main()