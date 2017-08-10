#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gui import *
from archeometre import *
import math

size = 1000
sizeMenu = 300
margin = 250
gui = Gui(size, size, sizeMenu)
archeometre = Archeometre(size, size, margin, margin)

mapLoaded = False
statusElem = 0
nexusId = -1
simulationStep = 0

def resetMapList():
	dataSelect = []
	mapList = archeometre.getMapList()
	for m in mapList:
		dataSelect.append([m, m])
	gui.resetSelect(objSelectMap, dataSelect)

def resetNexusList():
	dataSelect = [["Create nexus", -1]]
	nexusList = archeometre.getNexusList()
	for n in nexusList:
		dataSelect.append([str(n[1][0]), n[0]])
	gui.resetSelect(objSelectNexus, dataSelect)

def loadMapOnClick(e):
	global mapLoaded
	global size
	global sizeMenu
	mapName = e.value
	if mapName!=None and len(mapName)>0:
		archeometre.loadMap(mapName)
		mapProp = archeometre.getMapProp()
		carte = pygame.transform.scale(pygame.image.load(os.path.join(mapProp["urlBackground"])), (size, size))
		gui.drawImage(carte, sizeMenu, 0)
		mapLoaded = True
		objInputMapUrl.value = mapProp["urlBackground"]
		objInputpixUrl.value = mapProp["pixelSize"]
		objInputDateUrl.value = mapProp["startDate"]
		objInputViewUrl.value = mapProp["viewtimes"]
		resetNexusList()

def deleteMapOnClick(e):
	global size
	global sizeMenu
	mapName = e.value
	if mapName!=None and len(mapName)>0:
		archeometre.deleteMap(mapName)
		gui.fillRect(sizeMenu, 0, size, size, (0,0,0))
		resetMapList()

def createMapOnClick(e):
	mapName = e.value
	if mapName!=None and len(mapName)>0:
		archeometre.createMap(mapName, "fond/default.png", 1., "")
		loadMapOnClick(e)
		resetMapList()

def setMapUrlOnClick(e):
	global size
	global sizeMenu
	global mapLoaded
	urlMap = e.value
	if urlMap!=None and len(urlMap)>0 and mapLoaded:
		archeometre.setMapUrl(urlMap)
		carte = pygame.transform.scale(pygame.image.load(os.path.join(urlMap)), (size, size))
		gui.drawImage(carte, sizeMenu, 0)

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
	global nexusId
	global margin
	global sizeMenu
	if mapLoaded:
		if statusElem==2:
			data = []
			for i in range(len(objButtonElement)):
				data.append([objIdElement[i], float(objInputElement[i].value)])
			pos[0] = round(pos[0]/5.)*5
			pos[1] = round(pos[1]/5.)*5
			archeometre.addAttractor(data, pos[0]+margin-sizeMenu, pos[1]+margin)
		if statusElem==3:
			nexusName = str(objNexusNameElement.value)
			nexusX = int(round(pos[0]/10.)*10)
			nexusY = int(round(pos[1]/10.)*10)
			nexusTime = str(objNexusDataElement.value)
			nexusPower = []
			for i in range(len(objButtonElement)):
				nexusPower.append([objIdElement[i], float(objInputElement[i].value)])
			nexusId = archeometre.addNexus(nexusId, nexusName, nexusX+margin-sizeMenu, nexusY+margin, nexusTime, nexusPower)
			resetNexusList()

def onMouseDownedRightMap(pos):
	global mapLoaded
	global statusElem
	global margin
	if mapLoaded:
		if statusElem==2:
			pos[0] = round(pos[0]/5.)*5
			pos[1] = round(pos[1]/5.)*5
			archeometre.removeAttractor(pos[0]+margin-sizeMenu, pos[1]+margin)

def chooseNexusOnClick(e):
	global mapLoaded
	global statusElem
	global nexusId
	if mapLoaded:
		statusElem=3
		objModeElement.value = "mode: Edit nexus"
		nexusId = e.value

		if nexusId>0:
			nexusList = archeometre.getNexusList()
			for n in nexusList:
				if n[0] == nexusId:
					objNexusNameElement.value = n[1][0]
					objNexusDataElement.value = "["+str(n[1][3][0])+", "+str(n[1][3][1])+", "+str(n[1][3][2])+"]"
					for i in range(len(objButtonElement)):
						for elem in n[1][4]:
							if elem[0] == objIdElement[i]:
								objInputElement[i].value = elem[1]
								break
					break
		else:
			objNexusDataElement.value = "[0, 0, 0]"
			for i in range(len(objButtonElement)):
				objInputElement[i].value = 0.

def deleteNexusOnClick(e):
	global mapLoaded
	global statusElem
	global nexusId
	if mapLoaded:
		statusElem=0
		objModeElement.value = "mode: None"
		archeometre.deleteNexus(nexusId)
		nexusId = -1
		resetNexusList()

def onProgress(percent):
	objProgressBar.value = percent
	gui.update()

def simulateOnClick(e):
	global size
	global sizeMenu
	global margin
	global mapLoaded
	global simulationStep
	global statusElem
	if mapLoaded and statusElem!=4:
		statusElem = 4
		objModeElement.value = "mode: Simulating"
		simulationStep = int(e.value) + 1
		objInputStep.value = str(simulationStep)
		data = archeometre.simulate(simulationStep, onProgress)
		gui.paintArray(data, margin, margin, size+2*margin, size+2*margin, 1)
		statusElem = 0
		objModeElement.value = "mode: None"

def viewOnClick(e):
	global size
	global margin
	global mapLoaded
	global simulationStep
	global statusElem
	if mapLoaded and statusElem!=4:
		stepVal = int(e.value)
		data = archeometre.getStep(stepVal)
		gui.paintArray(data, margin, margin, size+2*margin, size+2*margin, 1)

def viewPlusOnClick(e):
	global size
	global margin
	global mapLoaded
	global simulationStep
	global statusElem
	if mapLoaded and statusElem!=4:
		stepVal = int(e.value)
		stepVal += 1
		e.value = stepVal
		data = archeometre.getStep(stepVal)
		gui.paintArray(data, margin, margin, size+2*margin, size+2*margin, 1)

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
objMFIEditAttractor = gui.addButton(10, 380, "Edit Attractor", editAttractorOnClick)

objSelectNexus = gui.addSelect(150, 420, [["", ""]])
objMFIChooseNexus = gui.addButton(10, 420, "Edit nexus", chooseNexusOnClick, objSelectNexus)
objMFIDeleteNexus = gui.addButton(10, 460, "Delete nexus", deleteNexusOnClick, objSelectNexus)

objInputStep = gui.addInput(160, 540, 10)
objSimulate = gui.addButton(10, 540, "Simulate step: ", simulateOnClick, objInputStep)
objProgressBar = gui.addProgressbar(10, 580, 30)

objInputStep.value = str(simulationStep)

objInputViewStep = gui.addInput(130, 620, 10)
objView = gui.addButton(10, 620, "View step: ", viewOnClick, objInputViewStep)
objPlusView = gui.addButton(250, 620, "+", viewPlusOnClick, objInputViewStep)

objInputViewStep.value = "1"

objButtonElement = []
objInputElement = []
objIdElement = []

elemList = archeometre.getElemList()
for i in range(len(elemList)):
	objInputElement.append(gui.addInput(80, size-40*(i+1), 5))
	objButtonElement.append(gui.addButton(10, size-40*(i+1), elemList[i][1], validElem, [objInputElement[-1], elemList[i][0]]))
	objIdElement.append(elemList[i][0])

objNexusNameElement = gui.addInput(145, size-40*(len(elemList)+1), 14)
objNexusDataElement = gui.addInput(145, size-40*(len(elemList)+2), 14)
objNexusNameLabel = gui.addLabel(10, size-40*(len(elemList)+1), "Nexus Name: ")
objNexusDataLabel = gui.addLabel(10, size-40*(len(elemList)+2), "Nexus times: ")
objModeElement = gui.addLabel(10, size-40*(len(elemList)+3), "mode: None")


gui.onMouseDownedMap(onMouseDownedMap)
gui.onMouseDownedRightMap(onMouseDownedRightMap)
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
		gui.fillRect(0, 0, size+sizeMenu, size, (0,0,0,0), 2)
		for a in attractorList:
			gui.fillRect(a[1]-margin+sizeMenu-3, a[2]-margin+-3, 5, 5, (r,g,b), 2)

		gui.fillRect(0, 0, size+sizeMenu, size, (0,0,0,0), 3)
		if nexusId != -1:
			nexusList = archeometre.getNexusList()
			for n in nexusList:
				if n[0] == nexusId:
					w = 0.1
					b = math.floor((math.sin(t*w)+1)*64)
					g = math.floor((math.sin(t*w+math.pi*2/3.)+1)*64)
					r = math.floor((math.sin(t*w+math.pi*4/3.)+1)*64)
					gui.fillCircle(n[1][1]-margin, n[1][2]-margin, 5, (r,g,b), 3)
					break

	running = gui.update()
