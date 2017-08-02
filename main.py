#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gui import *
from archeometre import *

gui = Gui(1200, 1000)
archeometre = Archeometre()

gui.drawImageByUrl("fond/carte.png", 10, 10)

running = True
while(running):
	running = gui.update()
	