#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gui import *
from archeometre import *
import pygame

gui = Gui(1200, 1000)
archeometre = Archeometre()

archeometre.loadMap("carte")
mapProp = archeometre.getMapProp()

carte = pygame.transform.scale(pygame.image.load(os.path.join(mapProp["urlBackground"])), (1000, 1000))

gui.drawLine(198, 0, 0, 1000, 2, (200, 150, 100))
gui.drawImage(carte, 200, 0)

running = True
while(running):
	running = gui.update()
	