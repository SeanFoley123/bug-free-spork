import pygame
from pygame.locals import *
import random, math, sys
screen = pygame.display.set_mode((400, 400))
background = pygame.image.load('dog.jpg').convert()
screen.blit(background, (0, 0))
rect1 = pygame.Rect(100, 100, 80, 80)
rect2 = pygame.Rect(rect1)
rect2.center = (300, 300)
pygame.draw.rect(screen, (0, 0 , 0), rect1)
pygame.draw.rect(screen, (0, 0 , 0), rect2)
running = True
while running:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	pygame.display.update()