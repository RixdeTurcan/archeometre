#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import math
import os

class Gui:
	def __init__(self, x, y): 
		pygame.init()
		
		self.size = [x, y]
		self.screen = pygame.display.set_mode(self.size)
		
		pygame.display.set_caption("Archeometre")
		self.screen.fill([0,0,0])
		pygame.display.flip()
	
	def drawImageByUrl(self, url, x, y):
		carte = pygame.image.load(os.path.join(url))
		self.drawImage(carte, x, y)
	
	def drawImage(self, image, x, y):
		self.screen.blit(image, (x, y))
		
	def drawRect(self, x, y, dx, dy, w, color):
		pygame.draw.rect(self.screen, color, [x, y, dx, dy], w)
	
	def drawLine(self, x, y, dx, dy, w, color):
		pygame.draw.line(self.screen, color, [x, y], [x+dx, y+dy], w)
		
	def update(self):
		running = True
		
		pygame.display.flip()
		event = pygame.event.wait()
		
		if event.type == pygame.QUIT:
			running = False
			
		return running
	
	def __del__(self):
		pygame.quit()