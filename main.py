#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gui import *
from archeometre import *

gui = Gui(1300, 1000)
archeometre = Archeometre()


def resetMapList():
	dataSelect = [["", ""]]
	mapList = archeometre.getMapList()
	for m in mapList:
		dataSelect.append([m, m])
	gui.resetSelect(objSelectMap, dataSelect)

def loadMapOnClick(e):
	mapName = e.value
	if mapName!=None and len(mapName)>0:
		archeometre.loadMap(mapName)
		mapProp = archeometre.getMapProp()
		carte = pygame.transform.scale(pygame.image.load(os.path.join(mapProp["urlBackground"])), (1000, 1000))
		gui.drawImage(carte, 300, 0)

def deleteMapOnClick(e):
	mapName = e.value
	if mapName!=None and len(mapName)>0:
		archeometre.deleteMap(mapName)
		gui.fillRect(300, 0, 1000, 1000, (0,0,0))
		resetMapList()

def createMapOnClick(e):
	mapName = e.value
	if mapName!=None and len(mapName)>0:
		archeometre.createMap(mapName, "fond/carte.png", 200000./1000., "[535, 12, 20, 0]")
		loadMapOnClick(e)
		resetMapList()



objSelectMap = gui.addSelect(10, 50, [])
objButtonLoad = gui.addButton(10, 10, "Load map", loadMapOnClick, objSelectMap)
objButtonDelete = gui.addButton(120, 10, "Delete map", deleteMapOnClick, objSelectMap)

obInputMap = gui.addInput(130, 90, 15)
objButtonCreate = gui.addButton(10, 90, "Create map", createMapOnClick, obInputMap)

resetMapList()



running = True
while(running):
	running = gui.update()
