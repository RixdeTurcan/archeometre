#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import os.path
from archeometre_init import *
import json

class Archeometre:
	def __init__(self):
		if not os.path.isfile("archeometre.db"):
			self.db = sqlite3.connect("archeometre.db")

			initArcheometre(self)
			self.createMap("default", "fond/default.png", 20000./1000., "")
		else:
			self.db = sqlite3.connect("archeometre.db")

		self.map = {}

	def __del__(self):
		self.db.close()

	def executeRequest(self, request):
		cursor = self.db.cursor()
		cursor.execute(request)
		self.db.commit()
		if request.find("SELECT")!=-1:
			return cursor.fetchall()

	def createMap(self, name, url, pixelSize, startDate):
		sizeX = 250+1000+250
		sizeY = 250+1000+250
		posXView = 250
		posYView = 250
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

	def getAttractorList(self):
		elem = self.executeRequest("""
		SELECT data, x, y FROM Attractor
		WHERE mapId="""+str(self.map["id"])+"""
		""")
		elemList = []
		for m in elem:
			elemList.append([m[0], m[1], m[2]])

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
