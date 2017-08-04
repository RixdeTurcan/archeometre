#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import math
import os

from pgu.pgu import gui as pgui

def doNothing(val):
	pass

class Gui:
	def __init__(self, x, y):
		pygame.init()

		self.size = [x, y]
		self.screen = pygame.display.set_mode(self.size)

		self.gui = pgui.App()
		self.layout = pgui.Container(width=280, height=980, align=-1)

		self.btn = []
		self.select = []
		self.inpt = []
		self.menu = []

		self.gui.init(self.layout)



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

	def fillRect(self, x, y, dx, dy, color):
		self.screen.fill(color, pygame.Rect(x, y, dx, dy))

	def drawLine(self, x, y, dx, dy, w, color):
		pygame.draw.line(self.screen, color, [x, y], [x+dx, y+dy], w)

	def addButton(self, x, y, text, onClick=doNothing, paramOnClick=0):
		self.btn.append(pgui.Button(text))
		self.btn[-1].connect(pgui.CLICK, onClick, paramOnClick)
		self.layout.add(self.btn[-1], x, y)

		self.gui.init(self.layout)

		return self.btn[-1]

	def addSelect(self, x, y, data, onSelect=doNothing):
		self.select.append(pgui.Select())
		for d in data:
			self.select[-1].add(d[0], d[1])

		self.select[-1].connect(pgui.CHANGE, onSelect, self.select[-1])
		self.layout.add(self.select[-1], x, y)

		self.gui.init(self.layout)

		return self.select[-1]

	def resetSelect(self, select, data):
		select.options.clear()

		for d in data:
			select.add(d[0], d[1])


	def addInput(self, x, y, l, val="", onInput=doNothing):
		self.inpt.append(pgui.Input(size=l, value=val))

		self.inpt[-1].connect(pgui.CHANGE, onInput, self.inpt[-1])
		self.layout.add(self.inpt[-1], x, y)

		self.gui.init(self.layout)

		return self.inpt[-1]

	def addMenu(self, x, y, data):
		self.menu.append(pgui.Menus(data))

		self.layout.add(self.menu[-1], x, y)

		self.gui.init(self.layout)

		return self.menu[-1]



	def update(self):
		running = True

		self.fillRect(0, 0, 300, 1000, (0,0,0))
		self.gui.paint(self.screen)

		pygame.display.flip()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

			self.gui.event(event)

		return running

	def __del__(self):
		pygame.quit()
