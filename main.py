#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gui import *
from archeometre import *
import math

gui = Gui(1300, 1000)
archeometre = Archeometre()

mapLoaded = False
statusElem = 0

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
	global statusElem
	if mapLoaded:
		statusElem=1
		objModeElement.value = "mode: Edit Magic field init"
		mapProp = archeometre.getMapProp()

		for i in range(len(objButtonElement)):
			objInputElement[i].value = 0.
			for elem in mapProp["magicFieldInit"]:
				if elem[0]==objIdElement[i]:
					objInputElement[i].value = elem[1]

def validElem(e):
	global mapLoaded
	global statusElem
	if mapLoaded:
		if statusElem==1:
			valueElem = float(e[0].value)
			idElem = float(e[1])
			archeometre.setMagicFieldInit(idElem, valueElem)

def editAttractorOnClick(e):
	global mapLoaded
	global statusElem
	if mapLoaded:
		statusElem=2
		objModeElement.value = "mode: Edit attractors"

		for i in range(len(objButtonElement)):
			objInputElement[i].value = 0.

def onMouseDownedMap(pos):
	global mapLoaded
	global statusElem
	if mapLoaded:
		if statusElem==2:
			data = []
			for i in range(len(objButtonElement)):
				data.append([objIdElement[i], float(objInputElement[i].value)])
			pos[0] = round(pos[0]/5.)*5
			pos[1] = round(pos[1]/5.)*5
			archeometre.addAttractor(data, pos[0], pos[1])

def onMouseDownedRightMap(pos):
	global mapLoaded
	global statusElem
	if mapLoaded:
		if statusElem==2:
			pos[0] = round(pos[0]/5.)*5
			pos[1] = round(pos[1]/5.)*5
			archeometre.removeAttractor(pos[0], pos[1])

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

objMFIEdit = gui.addButton(10, 340, "Get and edit Magic field Init", editMagicFieldInitOnClick)
objMFIEditAttractor = gui.addButton(10, 380, "edit Attractor", editAttractorOnClick)
gui.onMouseDownedMap(onMouseDownedMap)
gui.onMouseDownedRightMap(onMouseDownedRightMap)


objButtonElement = []
objInputElement = []
objIdElement = []

elemList = archeometre.getElemList()
for i in range(len(elemList)):
	objInputElement.append(gui.addInput(80, 1000-40*(i+1), 5))
	objButtonElement.append(gui.addButton(10, 1000-40*(i+1), elemList[i][1], validElem, [objInputElement[-1], elemList[i][0]]))
	objIdElement.append(elemList[i][0])

objModeElement = gui.addLabel(10, 1000-40*(len(elemList)+1), "mode: None")

resetMapList()



t = 0
running = True
while(running):
	t += 1
	if mapLoaded:
		attractorList = archeometre.getAttractorList()
		w = 0.1
		r = math.floor((math.sin(t*w)+1)*64)
		g = math.floor((math.sin(t*w+math.pi*2/3.)+1)*64)
		b = math.floor((math.sin(t*w+math.pi*4/3.)+1)*64)
		gui.fillRect(0, 0, 1300, 1000, (0,0,0,0), 1)
		for a in attractorList:
			for x in range(5):
				for y in range(5):
					gui.drawPixel(a[1]+x-3,a[2]+y-3, (r,g,b), 1)



	running = gui.update()
