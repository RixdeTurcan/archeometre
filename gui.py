import pygame
import math


class Gui:
	def __init__(self): 
		pygame.init()
		
		self.size = [1200, 1000]
		self.screen = pygame.display.set_mode(self.size)
		pygame.display.set_caption("Archeometre")
		
		self.screen.fill([0,0,0])
		pygame.display.flip()
		
	def __del__(self):
		pygame.quit()