#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import math
import os
import numpy

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
		self.label = []
		self.progressbar = []

		self.gui.init(self.layout)

		self.onMouseDownedMapFunc = doNothing
		self.onMouseDownedRightMapFunc = doNothing
		self.mouseDowned = False
		self.previousDownedPos = []
		self.buttonPressed = 1

		self.mask = []
		self.mask.append(pygame.surface.Surface(self.size, pygame.SRCALPHA)) #background image
		self.mask.append(pygame.surface.Surface(self.size, pygame.SRCALPHA)) #simulation
		self.mask.append(pygame.surface.Surface(self.size, pygame.SRCALPHA)) #attractor
		self.mask.append(pygame.surface.Surface(self.size, pygame.SRCALPHA)) #nexus
		self.mask.append(pygame.surface.Surface(self.size, pygame.SRCALPHA)) #gui

		pygame.display.set_caption("Archeometre")
		self.screen.fill([0,0,0])
		pygame.display.flip()

	def onMouseDownedMap(self, func):
		self.onMouseDownedMapFunc = func

	def onMouseDownedRightMap(self, func):
		self.onMouseDownedRightMapFunc = func

	def drawImageByUrl(self, url, x, y, maskId=0):
		carte = pygame.image.load(os.path.join(url))
		self.drawImage(carte, x, y, maskId)

	def drawImage(self, image, x, y, maskId=0):
		self.mask[maskId].blit(image, (x, y))

	def drawPixel(self, x, y, color, maskId=0):
		self.mask[maskId].set_at((x,y), color)

	def fillRect(self, x, y, dx, dy, color, maskId=0):
		self.mask[maskId].fill(color, pygame.Rect(x, y, dx, dy))

	def fillCircle(self, x, y, r, color, maskId=0):
		pygame.draw.circle(self.mask[maskId], color, (x, y), r, 0)

	def paintArray(self, data, x, y, lx, ly, maskId=0):
		self.fillRect(0, 0, 1300, 1000, (0,0,0,0.5), maskId)
		for i in range(1000):
			for j in range(1000):
				val = max(0, min(255, round(data[i+x][j+y] * 25.5)))
				self.drawPixel(i+300, j, (val, 255-val, 0), maskId)

	def addButton(self, x, y, text, onClick=doNothing, paramOnClick=0):
		self.btn.append(pgui.Button(text))
		self.btn[-1].connect(pgui.CLICK, onClick, paramOnClick)
		self.layout.add(self.btn[-1], x, y)

		self.gui.init(self.layout)

		return self.btn[-1]

	def addProgressbar(self, x, y, s):
		self.progressbar.append(pgui.slider.HSlider(value=0, min=0, max=100, size=s, width=260))
		self.layout.add(self.progressbar[-1], x, y)
		self.gui.init(self.layout)

		return self.progressbar[-1]

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

	def addLabel(self, x, y, text):
		self.label.append(pgui.Button(text))
		self.layout.add(self.label[-1], x, y)
		self.gui.init(self.layout)

		return self.label[-1]

	def update(self):
		running = True

		self.fillRect(0, 0, 300, 1000, (0,0,0), 4)
		self.gui.paint(self.mask[4])

		for m in self.mask:
			self.screen.blit(m, (0,0))

		pygame.display.flip()

		posTuple = pygame.mouse.get_pos()
		pos = [posTuple[0], posTuple[1]]

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

			if event.type == pygame.MOUSEBUTTONDOWN and pos[0]>300:
				self.mouseDowned = True
				self.buttonPressed = event.button


			if event.type == pygame.MOUSEBUTTONUP:
				self.mouseDowned = False
				self.previousDownedPos = []

			self.gui.event(event)

		if self.mouseDowned and pos[0]>300 and pos!=self.previousDownedPos:
			self.previousDownedPos = pos
			if self.buttonPressed==1:
				self.onMouseDownedMapFunc(pos)
			elif self.buttonPressed==3:
				self.onMouseDownedRightMapFunc(pos)

		return running

	def __del__(self):
		pygame.quit()
