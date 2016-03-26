import math, sys
import pygame
from pygame.locals import *
# Save files would not be hard, especially with pickling
# Really important: we need to be consistent on how we define positions. Right now I'm using relative to the upper left hand 
# corner of the current room. All sprites are defined at the center of their bounding rectangles, which might make rolling
# over easier.
class Room(object):
	### Assumes you make a self.objects_list, a self.start_positions, and a self.hero in your __init__. 
	def update(self):
		for thing in self.objects_list:
			thing.update()

	def enter_room(self, direction):
		# Direction is +1 if you're coming in from the left and -1 if you're coming in from the right. So start_positions should
		# have the rightmost start position first and the leftmost second.
		self.hero.position = self.start_positions[int(direction/2.0+.5)]


class Room1(Room):
	### Needs to be specialized for the particular arrangement of things in it; should have a list of objects, which will
	### keep track of their own position, a room size, and a background picture. Which should have clouds. And trees.
	def __init__(self, hero):
		self.hero = hero
		self.room_size = (3000, 1000)
		self.background = pygame.Surface(self.room_size)
		# Color chart at https://sites.google.com/site/meticulosslacker/pygame-thecolors
		self.background.fill(pygame.Color('deepskyblue'))
		self.background.fill(pygame.Color('lightsalmon3'), pygame.Rect(0, self.room_size[1]-200, self.room_size[0], 200))
		# This sets start positions based on how big the room is, where the ground is (200 from bottom), and how big the hero is.
		self.start_positions = [(self.room_size[0]-100, self.room_size[1]-200-self.hero.rect.h/2), (100, self.room_size[1]-200-self.hero.rect.h/2)]
		self.objects_list = [self.hero]


class Room2(Room):
	def __init__(self, hero):
		pass	


class Walking_things(object):
	###Defines basic movement for things that can move/jump
	def walk(self, direction):
		# print 'walking'
		self.position = (self.position[0]+direction*self.speed, self.position[1])

	def update(self):
		self.moved = False
		if self.position != self.rect.center:
			# print 'i moved from ', self.rect.center, ' to ', self.position

			self.model.dirty_rects.append(pygame.Rect(self.rect))
			self.moved = True
		self.rect.center = self.position
			# print self.rect.center


class Mushroom_Guy(Walking_things):
	### He moves, he shoots spores. I guess he needs to decide if he's just a funky little furry guy or a guy with a
	### mushroom.
	def __init__(self, model):
		# Possible variables: corruption, position, weight, power, flipped/not flipped, health
		self.model = model
		self.rect = pygame.Rect(0, 0, 100, 75)
		self.position = (self.rect.centerx, self.rect.centery)
		self.moved = False
		self.speed = 10 #how fast you walk


class View(object):
	### The room object in the model keeps track of the positions of all the things, and the view needs to draw them in 
	### the right places. It should keep track of its own position (top left corner) relative to the top left of the current room too.
	def __init__(self, model, screen_size):
		# Model is the big container, and screen_size is a tuple (width, height)
		self.model = model
		self.screen_size = screen_size
		self.screen = pygame.display.set_mode(screen_size)
		self.position = (0, self.model.current_room.room_size[1] - self.screen_size[1])

	def update(self, dirty_rects):
		# if dirty_rects:
		# 	print dirty_rects
		for old_rect in dirty_rects: #this should only contain the rectangles that had something in them last step but need to be drawn over now
			absolute_rect = old_rect.copy()
			old_rect.topleft = old_rect.left - self.position[0], old_rect.top - self.position[1]
			# print durr
			self.screen.blit(self.model.current_room.background, old_rect, absolute_rect)
			# pygame.draw.rect(self.screen,  pygame.Color('deepskyblue'), durr)
		for thing in self.model.current_room.objects_list:
			#This seems super inefficient; creates a new rectangle to draw every step.
			if thing.moved:
				# print 'hi'
				# print dirty_rects
				# print thing.rect
				# print
				place = pygame.Rect(thing.rect.left-self.position[0], thing.rect.top-self.position[1], thing.rect.w, thing.rect.h)    #placing it on the screen
				print 'old_rect: ' , old_rect
				print 'place: ', place
				print
				dirty_rects.append(place)
				pygame.draw.rect(self.screen, pygame.Color('orange'), place)
				print dirty_rects
		pygame.display.update(dirty_rects)

	def enter_room(self):
		self.screen.blit(self.model.current_room.background, (-self.position[0], -self.position[1]))
		for thing in self.model.current_room.objects_list:
			pygame.draw.rect(self.screen, pygame.Color('orange'), pygame.Rect(thing.rect.left-self.position[0], thing.rect.top-self.position[1], thing.rect.w, thing.rect.h))
		pygame.display.update()


class Controller(object):
	def __init__(self, model):
		self.model = model
		self.walking = 0

	def update(self):
		if self.walking:
			self.model.hero.walk(self.walking)
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN and event.key == pygame.K_RIGHT:
				self.walking += 1				
			elif event.type == KEYDOWN and event.key == pygame.K_LEFT:
				self.walking -= 1
			elif event.type == KEYUP and event.key == pygame.K_RIGHT:
				self.walking -= 1
			elif event.type == KEYUP and event.key == pygame.K_LEFT:
				self.walking += 1

class Model(object):
	### Contains the controller, the view, the current room, and the mushroom guy. Keeps track of the current room.
	### Changes self.currentroom when told to, and puts the mushroom guy in the current room. I think it might make sense
	### to do all the collision checking junk in the room instances.
	def __init__(self):
		# Need some kind of spatially-organized list of rooms/levels
		# Need a mushroom guy
		# Need a current room
		# Need a viewer of the proper size and a controller
		self.hero = Mushroom_Guy(self)

		self.room_list = [Room1(self.hero), Room2(self.hero)]
		self.current_room = self.room_list[0]
		self.current_room.enter_room(1)

		self.controller = Controller(self)

		screen_size = (800, 600)
		self.view = View(self, screen_size)
		self.view.enter_room()
		self.dirty_rects = []

	def update(self):
		self.controller.update()
		self.current_room.update()
		self.view.update(self.dirty_rects)
		self.dirty_rects = []

	def change_room(self, direction):
		### You try to move into the room that's in the direction you want to go: -1 means going left (so entering from the right), 
		### and 1 means going right.
		try:
			self.current_room = self.room_list.index(self.current_room) + direction
			self.current_room.enter_room(direction)
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