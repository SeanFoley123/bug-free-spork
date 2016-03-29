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
		for thing in self.objects_list[0] + self.objects_list[1]:
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
		self.room_size = (1000, 600)
		self.background = pygame.transform.scale(pygame.image.load('dog.jpg'), self.room_size)
		# Color chart at https://sites.google.com/site/meticulosslacker/pygame-thecolors
		# This sets start positions based on how big the room is, where the ground is (200 from bottom), and how big the hero is.
		self.start_positions = [(self.room_size[0]-100, self.room_size[1]-200-self.hero.rect.h/2), (100, self.room_size[1]-200-self.hero.rect.h/2)]
		# A list of lists of objects in the room. objects_list[0] is non-solid objects, objects_list[1] are solid.
		self.objects_list = [[self.hero, Lava(pygame.Rect(self.room_size[0]/3, self.room_size[1]-210, self.room_size[0]/3, 210))],
								[Ground(pygame.Rect(0, self.room_size[1]-200, self.room_size[0]/3, 200)), 
								Ground(pygame.Rect(2*self.room_size[0]/3, self.room_size[1]-200, self.room_size[0]/3, 200))]]


class Room2(Room):
	def __init__(self, hero):
		pass	


class Obstacle(object):
	def __init__(self, rect, sprite, mortality = False, hardness = False):
		self.hardness = hardness
		self.mortality = mortality
		self.sprite = sprite
		self.rect = rect
	
	def update(self):
		pass


class Ground(Obstacle):
	def __init__(self, rect):
		sprite = pygame.Surface((rect.w, rect.h))
		sprite.fill(pygame.Color('aquamarine4'))
		Obstacle.__init__(self, rect, sprite, False, True)

		
class Lava(Obstacle):
	def __init__(self, rect):
		sprite = pygame.Surface((rect.w, rect.h))
		sprite.fill(pygame.Color('chocolate1'))
		Obstacle.__init__(self, rect, sprite, True, False)


class WalkingThings(object):
	###Defines basic movement for things that can move/jump
	def walk(self, direction):
		# print 'walking'
		self.position = (self.position[0]+direction*self.speed, self.position[1])

	def update(self):
		self.rect.center = self.position
		self.check_collisions()

	def check_collisions(self):
		# I think we only care about collisions with non-solid things. We shouldn't actually ever overlap with a solid object.
		for thing in self.model.current_room.objects_list[0]:
			if self.rect.colliderect(thing.rect):
				if thing.mortality:
					self.die()

	def is_clear(self, direction):
		# Direction is vertical or horizontal
		# Checks if there's a solid object at the rectangle shifted by vx or vy, whichever is appropriate
		pass

	def die(self):
		self.model.current_room.objects_list[0].remove(self)


class MushroomGuy(WalkingThings):
	### He moves, he shoots spores. I guess he needs to decide if he's just a funky little furry guy or a guy with a
	### mushroom.
	def __init__(self, model):
		# Possible variables: corruption, position, weight, power, flipped/not flipped, health
		self.model = model
		self.rect = pygame.Rect(0, 0, 100, 75)
		self.position = (self.rect.centerx, self.rect.centery)
		self.moved = False
		self.speed = 10 #how fast you walk
		self.sprite = pygame.image.load('dog.jpg')
		self.sprite = pygame.transform.scale(self.sprite, (100, 75))
		self.mortality = False

	def die(self):
		self.sprite.fill(pygame.Color('red'), pygame.Rect(0, self.rect.h/2, self.rect.w, self.rect.h/2))


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
		self.position = min(max(self.model.hero.position[0] - self.screen_size[0]/2, 0), self.model.current_room.room_size[0]-self.screen_size[0]), self.position[1]
		self.screen.blit(self.model.current_room.background, (-self.position[0], -self.position[1]))
		for thing in self.model.current_room.objects_list[0] + self.model.current_room.objects_list[1]:
			self.screen.blit(thing.sprite, (thing.rect.left-self.position[0], thing.rect.top-self.position[1]))
		pygame.display.update()


class Controller(object):
	def __init__(self, model):
		self.model = model
		self.walking = 0

	def update(self):
		if self.walking:
			self.model.hero.walk(self.walking)
		for event in pygame.event.get():
			if event.type == QUIT or event.type == KEYDOWN and event.key == pygame.K_ESCAPE:
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
			elif event.type == KEYDOWN and event.key == pygame.K_a:
				self.model.view.position = self.model.view.position[0] - 100, self.model.view.position[1]
			elif event.type == KEYDOWN and event.key == pygame.K_d:
				self.model.view.position = self.model.view.position[0] + 100, self.model.view.position[1]


class Model(object):
	### Contains the controller, the view, the current room, and the mushroom guy. Keeps track of the current room.
	### Changes self.currentroom when told to, and puts the mushroom guy in the current room. I think it might make sense
	### to do all the collision checking junk in the room instances.
	def __init__(self):
		# Need some kind of spatially-organized list of rooms/levels
		# Need a mushroom guy
		# Need a current room
		# Need a viewer of the proper size and a controller
		self.hero = MushroomGuy(self)

		self.room_list = [Room1(self.hero), Room2(self.hero)]
		self.current_room = self.room_list[0]
		self.current_room.enter_room(1)

		self.controller = Controller(self)

		screen_size = (800, 600)
		self.view = View(self, screen_size)

	def update(self):
		self.controller.update()
		self.current_room.update()
		self.view.update()

	def change_room(self, direction):
		### You try to move into the room that's in the direction you want to go: -1 means going left (so entering from the right), 
		### and 1 means going right.
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