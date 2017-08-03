#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import os.path
from archeometre_init import *

class Archeometre:
	def __init__(self):
		if not os.path.isfile("archeometre.db"):
			self.db = sqlite3.connect("archeometre.db")

			initArcheometre(self)
			self.createMap("carte", "fond/carte.png", 200000./1000., "[535, 12, 20, 0]")
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
		SELECT sizeX, sizeY, posXView, posYView, urlBackground, pixelSize, startDate, viewtimes, magicFieldInit FROM Map
		WHERE name=\""""+name+"""\" AND deleted==0
		""")[0]
		self.map["sizeX"] = map[0]
		self.map["sizeY"] = map[1]
		self.map["posXView"] = map[2]
		self.map["posYView"] = map[3]
		self.map["urlBackground"] = map[4]
		self.map["pixelSize"] = map[5]
		self.map["startDate"] = map[6]
		self.map["viewtimes"] = map[7]
		self.map["magicFieldInit"] = map[8]

	def deleteMap(self, name):
		self.executeRequest("""
		UPDATE Map SET deleted=1 WHERE name=\""""+name+"""\"
		""")


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
