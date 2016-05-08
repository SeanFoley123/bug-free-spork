import math, sys
import pygame
from pygame.locals import *
from model import *

def main():
	pygame.init()
	clock = pygame.time.Clock()
	model = Model()
	running = True
	while running:
		clock.tick(60)
		model.update()

main()