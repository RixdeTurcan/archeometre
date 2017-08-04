#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gui import *
from archeometre import *

gui = Gui(1300, 1000)
archeometre = Archeometre()

mapLoaded = False

def resetMapList():
	dataSelect = []
	mapList = archeometre.getMapList()
	for m in mapList:
		dataSelect.append([m, m])
	gui.resetSelect(objSelectMap, dataSelect)

def loadMapOnClick(e):
	global mapLoaded
	mapName = e.value
	if mapName!=None and len(mapName)>0:
		archeometre.loadMap(mapName)
		mapProp = archeometre.getMapProp()
		carte = pygame.transform.scale(pygame.image.load(os.path.join(mapProp["urlBackground"])), (1000, 1000))
		gui.drawImage(carte, 300, 0)
		mapLoaded = True
		objInputMapUrl.value = mapProp["urlBackground"]
		objInputpixUrl.value = mapProp["pixelSize"]
		objInputDateUrl.value = mapProp["startDate"]
		objInputViewUrl.value = mapProp["viewtimes"]

def deleteMapOnClick(e):
	mapName = e.value
	if mapName!=None and len(mapName)>0:
		archeometre.deleteMap(mapName)
		gui.fillRect(300, 0, 1000, 1000, (0,0,0))
		resetMapList()

def createMapOnClick(e):
	mapName = e.value
	if mapName!=None and len(mapName)>0:
		archeometre.createMap(mapName, "fond/default.png", 200000./1000., "")
		loadMapOnClick(e)
		resetMapList()

def setMapUrlOnClick(e):
	global mapLoaded
	urlMap = e.value
	if urlMap!=None and len(urlMap)>0 and mapLoaded:
		archeometre.setMapUrl(urlMap)
		carte = pygame.transform.scale(pygame.image.load(os.path.join(urlMap)), (1000, 1000))
		gui.drawImage(carte, 300, 0)

def setPixelSamplingOnClick(e):
	global mapLoaded
	pixelSampling = e.value
	if mapLoaded:
		archeometre.setPixelSampling(pixelSampling)

def setStartDateOnClick(e):
	global mapLoaded
	startDate = e.value
	if mapLoaded:
		archeometre.setStartDate(startDate)

def setViewTimesOnClick(e):
	global mapLoaded
	times = e.value
	if mapLoaded:
		archeometre.setViewTimes(times)

def editMagicFieldInitOnClick(e):
	global mapLoaded
	if mapLoaded:
		gui.fillRect(300, 0, 1000, 1000, (0,0,0))
		structMFIEdit.append(gui.addButton(350, 10, "Feu"))
		structMFIEdit.append(gui.addButton(550, 10, "Terre"))
		structMFIEdit.append(gui.addButton(750, 10, "Lune"))
		structMFIEdit.append(gui.addButton(950, 10, "Eau"))
		structMFIEdit.append(gui.addButton(1150, 10, "Air"))

objSelectMap = gui.addSelect(10, 50, [])
objButtonLoad = gui.addButton(10, 10, "Load map", loadMapOnClick, objSelectMap)
objButtonDelete = gui.addButton(120, 10, "Delete map", deleteMapOnClick, objSelectMap)

objInputMap = gui.addInput(130, 90, 15)
objButtonCreate = gui.addButton(10, 90, "Create map", createMapOnClick, objInputMap)

objInputMapUrl = gui.addInput(80, 180, 22)
objButtonSetMapUrl = gui.addButton(10, 180, "Set url", setMapUrlOnClick, objInputMapUrl)

objInputpixUrl = gui.addInput(140, 220, 10)
objButtonSetPixUrl = gui.addButton(10, 220, "Set pixel size", setPixelSamplingOnClick, objInputpixUrl)

objInputDateUrl = gui.addInput(140, 260, 15)
objButtonSetDateUrl = gui.addButton(10, 260, "Set start date", setStartDateOnClick, objInputDateUrl)


objInputViewUrl = gui.addInput(140, 300, 15)
objButtonSetViewUrl = gui.addButton(10, 300, "Set view times", setViewTimesOnClick, objInputViewUrl)

structMFIEdit = []
objMFIEdit = gui.addButton(10, 340, "Edit Magic field Init", editMagicFieldInitOnClick)


resetMapList()




running = True
while(running):
	running = gui.update()
