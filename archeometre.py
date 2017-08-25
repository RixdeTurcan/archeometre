#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import os.path
from archeometre_init import *
from archeometre_simulation import *
from archeometre_data import *
import json

def doNothing(val):
	pass

def sign(x): return 1 if x >= 0 else -1

class Archeometre:
	def __init__(self, sizeX, sizeY, marginX, marginY, subSampling):
		self.sizeX = sizeX
		self.sizeY = sizeY
		self.marginX = marginX
		self.marginY = marginY
		self.subSampling = subSampling

		if not os.path.isfile("archeometre.db"):
			self.db = sqlite3.connect("archeometre.db")

			initArcheometre(self)
			self.createMap("espagne_test", "fond/espagne_test.png", 1., "")
		else:
			self.db = sqlite3.connect("archeometre.db")

		self.map = {}

	def __del__(self):
		self.db.close()

	def executeRequest(self, request, db=None):
		if db==None:
			db = self.db
		cursor = db.cursor()
		cursor.execute(request)
		db.commit()
		if request.find("SELECT")!=-1:
			return cursor.fetchall()

	def createMap(self, name, url, pixelSize, startDate):
		sizeX = self.sizeX+2*self.marginX
		sizeY = self.sizeY+2*self.marginY
		posXView = self.marginX
		posYView = self.marginY
		viewtimes = "[]"
		magicFieldInit = "[]"
		self.executeRequest("""
		INSERT INTO Map(name, sizeX, sizeY, posXView, posYView, urlBackground, pixelSize, startDate, viewtimes, magicFieldInit, deleted)
		VALUES(\""""+name+"""\", \""""+str(sizeX)+"""\", """+str(sizeY)+""", """+str(posXView)+""", """+str(posYView)+""",
		       \""""+url+"""\", """+str(pixelSize)+""", \""""+startDate+"""\", \""""+viewtimes+"""\", \""""+magicFieldInit+"""\", 0)
		""")

	def loadMap(self, name):
		map = self.executeRequest("""
		SELECT id, sizeX, sizeY, posXView, posYView, urlBackground, pixelSize, startDate, viewtimes, magicFieldInit FROM Map
		WHERE name=\""""+name+"""\" AND deleted==0
		""")[0]
		self.map["name"] = name
		self.map["id"] = map[0]
		self.map["sizeX"] = map[1]
		self.map["sizeY"] = map[2]
		self.map["posXView"] = map[3]
		self.map["posYView"] = map[4]
		self.map["urlBackground"] = map[5]
		self.map["pixelSize"] = map[6]
		self.map["startDate"] = map[7]
		self.map["viewtimes"] = map[8]
		self.map["magicFieldInit"] = json.loads(map[9])

	def deleteMap(self, name):
		self.executeRequest("""
		UPDATE Map SET deleted=1 WHERE name=\""""+name+"""\"
		""")

	def setMapUrl(self, url):
		self.executeRequest("""
		UPDATE Map SET urlBackground=\""""+url+"""\" WHERE name=\""""+self.map["name"]+"""\" AND deleted=0
		""")

	def setPixelSampling(self, size):
		self.executeRequest("""
		UPDATE Map SET pixelSize=\""""+size+"""\" WHERE name=\""""+self.map["name"]+"""\" AND deleted=0
		""")

	def setStartDate(self, date):
		self.executeRequest("""
		UPDATE Map SET startDate=\""""+date+"""\" WHERE name=\""""+self.map["name"]+"""\" AND deleted=0
		""")

	def setViewTimes(self, times):
		self.executeRequest("""
		UPDATE Map SET viewtimes=\""""+times+"""\" WHERE name=\""""+self.map["name"]+"""\" AND deleted=0
		""")

	def setMagicFieldInit(self, idElem, valueElem):
		elemFound = False
		for elem in self.map["magicFieldInit"]:
			if elem[0] == idElem:
				elem[1] = valueElem
				elemFound = True
				break

		if not elemFound:
			self.map["magicFieldInit"].append([idElem, valueElem])

		self.executeRequest("""
		UPDATE Map SET magicFieldInit=\""""+json.dumps(self.map["magicFieldInit"])+"""\" WHERE name=\""""+self.map["name"]+"""\" AND deleted=0
		""")

	def addAttractor(self, data, x, y):
		attractor = self.executeRequest("""
		SELECT id FROM Attractor WHERE mapId="""+str(self.map["id"])+""" and x="""+str(x)+""" and y="""+str(y)+"""
		""")

		if len(attractor)==0:
			self.executeRequest("""
			INSERT INTO Attractor(mapId, data, x, y)
			VALUES("""+str(self.map["id"])+""", \""""+json.dumps(data)+"""\", """+str(x)+""", """+str(y)+""")
			""")
		else:
			self.executeRequest("""
			UPDATE Attractor SET data=\""""+json.dumps(data)+"""\" WHERE id="""+str(attractor[0][0])+"""
			""")

	def removeAttractor(self, x, y):
		self.executeRequest("""
		DELETE FROM Attractor
		WHERE mapId="""+str(self.map["id"])+""" and x="""+str(x)+""" and y="""+str(y)+"""
		""")

	def addNexus(self, nexusId, nexusName, nexusX, nexusY, nexusTime, nexusPower):
		data = [nexusName, nexusX, nexusY, json.loads(nexusTime), nexusPower]
		if nexusId == -1:
			self.executeRequest("""
			INSERT INTO Nexus(mapId, data)
			VALUES("""+str(self.map["id"])+""", '"""+json.dumps(data)+"""')
			""")
			elem = self.executeRequest("""
			SELECT max(id) FROM Nexus
			""")
			nexusId = int(elem[0][0])
		else:
			self.executeRequest("""
			UPDATE Nexus SET data='"""+json.dumps(data)+"""' WHERE id="""+str(nexusId)+"""
			""")

		return nexusId

	def deleteNexus(self, nexusId):
		self.executeRequest("""
		DELETE FROM Nexus
		WHERE id="""+str(nexusId)+"""
		""")

	def getAttractorList(self):
		elem = self.executeRequest("""
		SELECT data, x, y FROM Attractor
		WHERE mapId="""+str(self.map["id"])+"""
		""")
		elemList = []
		for m in elem:
			elemList.append([json.loads(m[0]), m[1], m[2]])

		return elemList

	def getNexusList(self):
		elem = self.executeRequest("""
		SELECT id, data FROM Nexus
		WHERE mapId="""+str(self.map["id"])+"""
		""")
		elemList = []
		for m in elem:
			data = json.loads(m[1])
			elemList.append([m[0], data])

		return elemList

	def getElemList(self):
		elem = self.executeRequest("""
		SELECT id, name FROM Element
		""")
		elemList = []
		for m in elem:
			elemList.append([m[0], str(m[1])])

		return elemList

	def getMapList(self):
		map = self.executeRequest("""
		SELECT name FROM Map WHERE deleted==0
		""")
		mapList = []
		for m in map:
			mapList.append(str(m[0]))

		return mapList

	def getMapProp(self):
		return self.map

	def getStep(self, timeStep, elemId):
			mapData = self.executeRequest("""
			SELECT data FROM MapData WHERE mapId="""+str(self.map["id"])+""" and time="""+str(timeStep)+""" and elemId="""+str(elemId)+"""
			""")
			if len(mapData)>0:
				data = json.loads(mapData[0][0])
				return data
			else:
				return None

	def simulate(self, elemId, timeStep = 1, onProgressfunc=doNothing, onFinalfunc=doNothing):

		attractorList = self.getAttractorList()
		nexusList = self.getNexusList()
		elemList = self.getElemList()

		for i in range(len(elemList)):
			if elemList[i][0] != elemId:
				continue

			lx = self.sizeX+2*self.marginX
			ly = self.sizeY+2*self.marginY

			data = None
			if timeStep==1:
				mgi = 0
				while self.map["magicFieldInit"][mgi][0] != elemList[i][0]:
					mgi += 1
				valInit = self.map["magicFieldInit"][mgi][1]

				data = [None]*lx
				for x in range(len(data)):
					data[x] = [valInit]*ly
			else:
				mapData = self.executeRequest("""
				SELECT data FROM MapData WHERE mapId="""+str(self.map["id"])+""" and time="""+str(timeStep-1)+""" and elemId="""+str(elemList[i][0])+"""
				""")
				data = json.loads(mapData[0][0])

			dataInput = []
			dataInput.append(self.sizeX)
			dataInput.append(self.sizeY)
			dataInput.append(self.marginX)
			dataInput.append(self.marginY)
			dataInput.append(timeStep)
			dataInput.append(data)
			dataInput.append(attractorList)
			dataInput.append(nexusList)
			dataInput.append(self.subSampling)
			dataInput.append(getElementData(elemList[i][1]))
			dataInput.append(elemList[i][0])

			data = simulateArcheometre(onProgressfunc, dataInput)

			mapData = self.executeRequest("""
			SELECT id FROM MapData WHERE mapId="""+str(self.map["id"])+""" and time="""+str(data[2])+""" and elemId="""+str(data[1])+"""
			""")

			if len(mapData)==0:
				self.executeRequest("""
				INSERT INTO MapData(time, data, mapId, elemId)
				VALUES("""+str(data[2])+""", '"""+json.dumps(data[0])+"""', """+str(self.map["id"])+""", '"""+str(data[1])+"""')
				""")
			else:
				self.executeRequest("""
				UPDATE MapData SET data='"""+json.dumps(data[0])+"""' WHERE id="""+str(mapData[0][0])+""" and elemId="""+str(data[1])+"""
				""")

			onProgressfunc(0.0)

			onFinalfunc(data[0])
			break


































