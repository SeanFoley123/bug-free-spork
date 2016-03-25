import math, sys
import pygame
from pygame.locals import *
from view import *
from controller import *
from rooms import *
from objects import *

class Model(object):
	### Contains the controller, the view, the current room, and the mushroom guy. Keeps track of the current room.
	### Changes self.currentroom when told to, and puts the mushroom guy in the current room. I think it might make sense
	### to do all the collision checking junk in the room instances.
	def __init__(self):
		# Need some kind of spatially-organized list of rooms/levels
		# Need a mushroom guy
		# Need a current room
		# Need a viewer of the proper size and a controller
		self.hero = Mushroom_Guy()

		self.room_list = [Room1(self.hero), Room2(self.hero)]
		self.current_room = self.room_list[0]

		self.controller = Controller(self)

		screen_size = (800, 600)
		self.view = View(self, screen_size)

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