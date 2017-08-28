#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gui import *
from archeometre import *
import math
import json


size = 1024
sizeMenu = 300
margin = 256
subSampling = 8
gui = Gui(size, size, sizeMenu)
archeometre = Archeometre(size/subSampling, size/subSampling, margin/subSampling, margin/subSampling, subSampling)

mapLoaded = False
hour = 0
elemId = 0
sensibilityMin = 0
sensibilityMax = 1
viewData = None
shouldRepaint = False
transparency = 255

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
	global sizeMenu
	mapName = e.value
	if mapName!=None and len(mapName)>0:
		archeometre.loadMap(mapName)
		mapProp = archeometre.getMapProp()
		carte = pygame.transform.scale(pygame.image.load(os.path.join(mapProp["urlBackground"])), (size, size))
		gui.drawImage(carte, sizeMenu, 0)
		mapLoaded = True
		objInputpixUrl.value = "1 pixel = "+str(int(mapProp["pixelSize"]))+" m"
		objInputDateUrl.value = "Start date : "+str(mapProp["startDate"])

		resetViewTimesList()

def chooseViewTimeOnClick(e):
	global mapLoaded
	global margin
	global subSampling
	global elemId
	global hour
	global viewData
	global shouldRepaint

	hour = e.value
	if mapLoaded and hour!=None:
		viewData = archeometre.getStep(hour, elemId)
		shouldRepaint = True

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

objSelectMap = gui.addSelect(10, 40, [], loadMapOnClick)
objButtonLoad = gui.addButton(10, 10, "Load map", loadMapOnClick, objSelectMap)


objInputpixUrl = gui.addLabel(10, 80, "1 pixel = ? m")
objInputDateUrl = gui.addLabel(10, 110, "Start date : ?")


objSelectElem = gui.addSelect(170, 170, [], chooseElementOnClick)
objButtonElem = gui.addButton(10, 170, "Choose element", chooseElementOnClick, objSelectElem)

objSelectViewTime = gui.addSelect(170, 210, [], chooseViewTimeOnClick)
objButtonViewTime = gui.addButton(10, 210, "Choose view time", chooseViewTimeOnClick, objSelectViewTime)


objLabelBackground = gui.addLabel(10, 270, "Background transparency")
objProgressBarBackground = gui.addProgressbar(10, 310, 30, transparencyOnChange)


objLabelSensibility = gui.addLabel(10, 370, "Element sensibility")
objProgressBarSensibilityMin = gui.addProgressbar(10, 410, 30, sensibilityOnChangeMin)
objProgressBarSensibilityMax = gui.addProgressbar(10, 450, 30, sensibilityOnChangeMax)
objProgressBarSensibilityMax.value = 100

objLabelXMouse = gui.addLabel(10, 510, "Position X : ? m")
objLabelYMouse = gui.addLabel(10, 540, "Position Y : ? m")

objLabelMFV = gui.addLabel(10, 600,  "Presence elem : ?")
objLabelMFV2 = gui.addLabel(10, 630, "Puces : ?")

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
			gui.paintArray(viewData, margin/subSampling, margin/subSampling, subSampling, 1, objProgressBarSensibilityMin.value/10., objProgressBarSensibilityMax.value/10., transparency)
			shouldRepaint = False

		pos = pygame.mouse.get_pos()

		if pos[0]<sizeMenu:
			objLabelXMouse.value = "Position X : ? m"
			objLabelYMouse.value = "Position Y : ? m"
			objLabelMFV.value = "Presence elem : ?"
			objLabelMFV2.value = "Puces : ?"
		else:
			mapProp = archeometre.getMapProp()
			objLabelXMouse.value = "Position X : "+str(int(round((pos[0]-sizeMenu)*mapProp["pixelSize"]/1000., 0)))+" "+str(int(round(((pos[0]-sizeMenu)*mapProp["pixelSize"])%1000, 0)))+" m"
			objLabelYMouse.value = "Position Y : "+str(int(round(pos[1]*mapProp["pixelSize"]/1000., 0)))+" "+str(int(round((pos[1]*mapProp["pixelSize"])%1000, 0)))+" m"

			if viewData!=None:
				x = int((pos[0]-sizeMenu+margin)/subSampling)
				y = int((pos[1]+margin)/subSampling)
				val = viewData[x][y]/2.

				name = NumToNameElem[int(math.floor(val))]
				puces=math.floor((val%1)*11)

				objLabelMFV.value = "Presence elem : "+name
				objLabelMFV2.value = "Puces : "+str(int(puces))


	running = gui.update()
