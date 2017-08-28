#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gui import *
from archeometre import *
import math
import json


size = 1024
sizeScreen = 800
sizeMenu = 300
margin = 256
subSampling = 8
gui = Gui(size, size, sizeMenu, sizeScreen, sizeScreen)
archeometre = Archeometre(size/subSampling, size/subSampling, margin/subSampling, margin/subSampling, subSampling)

mapLoaded = False
hour = 0
elemId = 0
sensibilityMin = 0
sensibilityMax = 1
viewData = None
shouldRepaint = False
transparency = 255
viewTimeId = 0

def resetMapList():
	dataSelect = []
	mapList = archeometre.getMapList()
	for m in mapList:
		dataSelect.append([m, m])
	gui.resetSelect(objSelectMap, dataSelect)

def resetElementList():
	dataSelect = []
	elemList = archeometre.getElemList()
	for n in elemList:
		dataSelect.append([str(n[1]), n[0]])
	gui.resetSelect(objSelectElem, dataSelect)

def resetViewTimesList():
	dataSelect = []
	elemList = archeometre.getElemList()
	mapProp = archeometre.getMapProp()
	viewTimes = json.loads(mapProp["viewtimes"])
	offstepHour = viewTimes[0]
	for n in viewTimes[1]:
		day = (n-offstepHour)/24
		heures = (n-offstepHour)%24
		name = str(day)+" j "+str(heures)+" h"
		if day==0:
			name = str(heures)+" h"
		dataSelect.append([name, int(n)])
	gui.resetSelect(objSelectViewTime, dataSelect)

def loadMapOnClick(e):
	global mapLoaded
	global size
	global sizeScreen
	mapName = e.value
	if mapName!=None and len(mapName)>0:
		archeometre.loadMap(mapName)
		mapProp = archeometre.getMapProp()
		carte = pygame.transform.smoothscale(pygame.image.load(os.path.join(mapProp["urlBackground"])), (sizeScreen, sizeScreen))
		gui.drawImage(carte, sizeMenu, 0)
		mapLoaded = True
		objInputpixUrl.value = "1 pixel = "+str(int(mapProp["pixelSize"]))+" m"
		objInputDateUrl.value = "Start date : "+str(mapProp["startDate"])

		resetViewTimesList()

def chooseViewTimeOnClick(e):
	global mapLoaded
	global elemId
	global hour
	global viewData
	global shouldRepaint
	global viewTimeId

	hour = int(e.value)
		
	if mapLoaded and hour!=None:
		mapProp = archeometre.getMapProp()
		viewTimes = json.loads(mapProp["viewtimes"])
		for i in range(len(viewTimes[1])):
			if viewTimes[1][i] == hour:
				viewTimeId = i
				break
		viewData = archeometre.getStep(hour, elemId)
		shouldRepaint = True
		
		day = (hour-viewTimes[0])/24
		heures = (hour-viewTimes[0])%24
		name = str(day)+" j "+str(heures)+" h"
		objLabelViewTime.value = name
		
def chooseViewTimePlusOnClick(e):
	global mapLoaded
	global viewTimeId
	global elemId
	global hour
	global viewData
	global shouldRepaint
	
	if mapLoaded:
		mapProp = archeometre.getMapProp()
		viewTimes = json.loads(mapProp["viewtimes"])
		viewTimeId += 1
		viewTimeId = min(viewTimeId, len(viewTimes[1])-1)
		hour = viewTimes[1][viewTimeId]
		viewData = archeometre.getStep(hour, elemId)
		shouldRepaint = True

		day = (hour-viewTimes[0])/24
		heures = (hour-viewTimes[0])%24
		name = str(day)+" j "+str(heures)+" h"
		objLabelViewTime.value = name

def chooseViewTimeMinusOnClick(e):
	global mapLoaded
	global viewTimeId
	global elemId
	global hour
	global viewData
	global shouldRepaint
	
	if mapLoaded:
		mapProp = archeometre.getMapProp()
		viewTimes = json.loads(mapProp["viewtimes"])
		viewTimeId -= 1
		viewTimeId = max(viewTimeId, 0)
		hour = viewTimes[1][viewTimeId]
		viewData = archeometre.getStep(hour, elemId)
		shouldRepaint = True

		day = (hour-viewTimes[0])/24
		heures = (hour-viewTimes[0])%24
		name = str(day)+" j "+str(heures)+" h"
		objLabelViewTime.value = name
	
def chooseElementOnClick(e):
	global elemId
	global shouldRepaint
	global hour
	global viewData

	elemId = e.value
	viewData = archeometre.getStep(hour, elemId)
	shouldRepaint = True

def transparencyOnChange(e):
	global mapLoaded
	global shouldRepaint
	global transparency
	value = e.value
	if mapLoaded:
		transparency = round(255-value*2.55)
		shouldRepaint = True


def sensibilityOnChange(e):
	global margin
	global subSampling
	global viewData
	global shouldRepaint

	shouldRepaint = True

def sensibilityOnChangeMin(e):
	global mapLoaded
	global margin
	global subSampling

	objProgressBarSensibilityMax.value = max(min(objProgressBarSensibilityMin.value+10,100), objProgressBarSensibilityMax.value)
	objProgressBarSensibilityMin.value = min(max(objProgressBarSensibilityMax.value-10,0), objProgressBarSensibilityMin.value)

	if mapLoaded:
		sensibilityOnChange(e)

def sensibilityOnChangeMax(e):
	global mapLoaded
	global viewData
	global margin
	global subSampling

	objProgressBarSensibilityMin.value = min(max(objProgressBarSensibilityMax.value-10,0), objProgressBarSensibilityMin.value)
	objProgressBarSensibilityMax.value = max(min(objProgressBarSensibilityMin.value+10,100), objProgressBarSensibilityMax.value)
	if mapLoaded:
		sensibilityOnChange(e)

objSelectMap = gui.addSelect(10, 40, [["", ""]], loadMapOnClick)
objButtonLoad = gui.addButton(10, 10, "Load map", loadMapOnClick, objSelectMap)


objInputpixUrl = gui.addLabel(10, 80, "1 pixel = ? m")
objInputDateUrl = gui.addLabel(10, 110, "Start date : ?")


objSelectElem = gui.addSelect(170, 170, [["", ""]], chooseElementOnClick)
objButtonElem = gui.addButton(10, 170, "Choose element", chooseElementOnClick, objSelectElem)

objSelectViewTime = gui.addSelect(170, 210, [["", ""]], chooseViewTimeOnClick)
objButtonViewTime = gui.addButton(10, 210, "Choose view time", chooseViewTimeOnClick, objSelectViewTime)
objButtonViewTime = gui.addButton(100, 240, "-", chooseViewTimeMinusOnClick, objSelectViewTime)
objButtonViewTime = gui.addButton(130, 240, "+", chooseViewTimePlusOnClick, objSelectViewTime)
objLabelViewTime = gui.addLabel(170, 240, "")
gui.onMouseScrolldown(chooseViewTimePlusOnClick)
gui.onMouseScrollup(chooseViewTimeMinusOnClick)

objLabelBackground = gui.addLabel(10, 310, "Background transparency")
objProgressBarBackground = gui.addProgressbar(10, 350, 30, transparencyOnChange)


objLabelSensibility = gui.addLabel(10, 370, "Element sensibility")
objProgressBarSensibilityMin = gui.addProgressbar(10, 450, 30, sensibilityOnChangeMin)
objProgressBarSensibilityMax = gui.addProgressbar(10, 490, 30, sensibilityOnChangeMax)
objProgressBarSensibilityMax.value = 28
objLabelSens = gui.addLabel(10, 520, "Range : ?")

objLabelXMouse = gui.addLabel(10, 590, "Position X : ? m")
objLabelYMouse = gui.addLabel(10, 630, "Position Y : ? m")

objLabelMFV = gui.addLabel(10, 680,  "Presence elem : ?")
objLabelMFV2 = gui.addLabel(10, 710, "Puces : ?")

resetMapList()
resetElementList()

NumToNameElem = []
NumToNameElem.append("Pas")
NumToNameElem.append("Peu")
NumToNameElem.append("Assez")
NumToNameElem.append("...")
NumToNameElem.append("Tres")
for i in range(100):
	NumToNameElem.append("Tres+"+str(i+1))

t = 0
running = True
while(running):
	t +=1
	if mapLoaded:
		if shouldRepaint and t%10==0 and viewData!=None:
			gui.paintArray(viewData, margin/subSampling, margin/subSampling, subSampling, 1, objProgressBarSensibilityMin.value/3., objProgressBarSensibilityMax.value/3., transparency)
			shouldRepaint = False

		posTuple = pygame.mouse.get_pos()
		pos = [posTuple[0], posTuple[1]]
		pos[0] = int((pos[0]-sizeMenu)*size/sizeScreen)
		pos[1] = int(pos[1]*size/sizeScreen)
		
		
		valMin = objProgressBarSensibilityMin.value/3./2.
		nameMin = NumToNameElem[int(math.floor(valMin))]
		valMax = objProgressBarSensibilityMax.value/3./2.
		nameMax = NumToNameElem[int(math.floor(valMax))]
		objLabelSens.value = "Range : "+nameMin+" / "+nameMax

		if pos[0]<0:
			objLabelXMouse.value = "Position X : ? m"
			objLabelYMouse.value = "Position Y : ? m"
			objLabelMFV.value = "Presence elem : ?"
			objLabelMFV2.value = "Puces : ?"
		else:
			mapProp = archeometre.getMapProp()
			objLabelXMouse.value = "Position X : "+str(int(round((pos[0])*mapProp["pixelSize"]/1000., 0)))+" "+str(int(round(((pos[0])*mapProp["pixelSize"])%1000, 0)))+" m"
			objLabelYMouse.value = "Position Y : "+str(int(round(pos[1]*mapProp["pixelSize"]/1000., 0)))+" "+str(int(round((pos[1]*mapProp["pixelSize"])%1000, 0)))+" m"

			if viewData!=None:
				x = int((pos[0]+margin)/subSampling)
				y = int((pos[1]+margin)/subSampling)
				val = viewData[x][y]/2.

				name = NumToNameElem[int(math.floor(val))]
				puces=math.floor((val%1)*11)

				objLabelMFV.value = "Presence elem : "+name
				objLabelMFV2.value = "Puces : "+str(int(puces))


	running = gui.update()
