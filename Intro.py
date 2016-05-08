### This module provides the beginning text intro

import math, sys, pickle
import pygame
from pygame.locals import *

class IntroMovie(object):
	""" This class contains the images for the different intro screens as a list. """
	def __init__(self, screen):
		# IntroMovie must be given the screen you want it to blit onto
		self.screen = screen
		self.done = False

		# Initialize the list of images in order of which you want displayed. Does not currently resize anything.
		self.image_list = [pygame.image.load("png/title.png").convert_alpha(),
							pygame.image.load("png/frame2.png").convert_alpha(),
							pygame.image.load("png/frame3.png").convert_alpha(),
							pygame.image.load("png/frame4.png").convert_alpha(),
							pygame.image.load("png/frame5.png").convert_alpha(),
							pygame.image.load("png/frame6.png").convert_alpha(),
							pygame.image.load("png/frame7.png").convert_alpha(),
							pygame.image.load("png/frame8.png").convert_alpha(),
							pygame.image.load("png/frame9.png").convert_alpha(),
							pygame.image.load("png/frame10.png").convert_alpha(),
							pygame.image.load("png/frame11.png").convert_alpha(),
							pygame.image.load("png/frame12.png").convert_alpha(),
							pygame.image.load("png/frame13.png").convert_alpha()
							]

		# Set the starting image
		self.image_index = -1
		self.change_image()

	def change_image(self):
		# Moves to the next image and centers it
		self.image_index += 1
		self.image = self.image_list[self.image_index]
		self.rect = self.image.get_rect()
		self.rect.center = self.screen.get_rect().center

	def update(self):
		# Check for any updates, such as they are trying to skip through it all. 
		# Controller is not currently running, so this must be done within IntroMovie
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				self.done = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					if self.image_index < len(self.image_list)-1:
						self.change_image()
					else:
						self.done = True

		# Display on-screen with a black background, if applicable
		self.screen.fill((0,0,0)) 
		self.screen.blit(self.image, self.rect)

		pygame.display.flip()

def run(screen, clock):
	""" Makes things run. This is called in game_base.py before the game begins, 
		so that you only see it once. clock and screen are initialized outside of here
		in order to make them be the same as the game will be played with."""
	video = IntroMovie(screen)

	while not video.done:
		video.update()
		clock.tick(60)