#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import os.path
from archeometre_init import *
import json
import random
import math

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

	def executeRequest(self, request):
		cursor = self.db.cursor()
		cursor.execute(request)
		self.db.commit()
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

	def getStep(self, timeStep):
			mapData = self.executeRequest("""
			SELECT data FROM MapData WHERE mapId="""+str(self.map["id"])+""" and time="""+str(timeStep)+"""
			""")
			if len(mapData)>0:
				data = json.loads(mapData[0][0])
				return data
			else:
				return None

	def simulate(self, timeStep = 1, onProgressfunc=doNothing):
		lx = self.sizeX+2*self.marginX
		ly = self.sizeY+2*self.marginY

		data = None
		if timeStep==1:
			valInit = self.map["magicFieldInit"][1][1] #eau
			data = [None]*lx
			for x in range(len(data)):
				data[x] = [valInit]*ly
		else:
			mapData = self.executeRequest("""
			SELECT data FROM MapData WHERE mapId="""+str(self.map["id"])+""" and time="""+str(timeStep-1)+"""
			""")
			data = json.loads(mapData[0][0])


		data2 = [None]*lx
		for x in range(len(data)):
			data2[x] = [0.]*ly


		spreadMat = [
		[2.0, 2.5, 2.0],
		[2.5, 3.0, 2.5],
		[2.0, 2.5, 2.0]
		] #eau
		spreadMatSize = len(spreadMat)
		spreadMatMid = (spreadMatSize-1)/2
		sumSpread = 0.
		for x in range(spreadMatSize):
			for y in range(spreadMatSize):
				sumSpread += spreadMat[x][y]
		for x in range(spreadMatSize):
			for y in range(spreadMatSize):
				spreadMat[x][y] /= sumSpread

		attractorList = self.getAttractorList()
		nexusList = self.getNexusList()


		for x in range(lx):
			if x%2==0:
				onProgressfunc(round(100.*x/float(lx), 1))

			for y in range(ly):
				val = data[x][y]
				dx = 0
				dy = 0
				for a in attractorList:
					p = a[0][3][1] #eau

					rx = a[1]-x
					ry = a[2]-y
					r = math.sqrt(rx*rx+ry*ry)*self.subSampling/600.
					alpha = math.atan2(ry, rx) + (random.random()*2.-1.)*0.5

					a = max(4.*(r-r*r)*2.-1., 0.)*p*0.05/max(1., pow(val/3., 1.)) #TODO BUG

					dx += a*math.cos(alpha)
					dy += a*math.sin(alpha)

				for n in nexusList:
					timings = n[1][3]
					if timeStep>=timings[0] and timeStep<timings[2]:
						rx = n[1][1]-x
						ry = n[1][2]-y
						p = n[1][4][3][1] #eau

						r = max(1., math.sqrt(rx*rx+ry*ry))*self.subSampling/600.
						alpha = math.atan2(ry, rx) + (random.random()*2.-1.)*0.5

						factor = (timeStep-timings[0])/float(timings[1]-timings[0])
						if timeStep>timings[1]:
							factor = -(timings[2]-timeStep)/float(timings[2]-timings[1])
						a = min(max(4.*factor*p*(r-r*r), -10.), 10.)

						dx += a*math.cos(alpha)
						dy += a*math.sin(alpha)

				dxi = int(math.floor(dx))
				dyi = int(math.floor(dy))

				for j in range(spreadMatSize):
					for k in range(spreadMatSize):
						val2 = val*spreadMat[j][k]

						factorX = dx-dxi
						factorY = dy-dyi
						for l in range(2):
							for m in range(2):
								x2 = x+dxi+j+l-spreadMatMid
								y2 = y+dyi+k+m-spreadMatMid
								if x2>=0 and y2>=0 and x2<lx and y2<ly:
									factor = (1.-abs(l-factorX)) * (1.-abs(m-factorY))
									data2[x2][y2] += val2*factor

		for x in range(lx):
			for y in range(ly):
				if data2[x][y]<1.:
					data2[x][y] += random.random()*0.1
				if data2[x][y]>6.:
					data2[x][y] -= random.random()*0.1
				data2[x][y] = round(data2[x][y], 3)


		mapData = self.executeRequest("""
		SELECT id FROM MapData WHERE mapId="""+str(self.map["id"])+""" and time="""+str(timeStep)+"""
		""")

		if len(mapData)==0:
			self.executeRequest("""
			INSERT INTO MapData(time, data, mapId)
			VALUES("""+str(timeStep)+""", '"""+json.dumps(data2)+"""', """+str(self.map["id"])+""")
			""")
		else:
			self.executeRequest("""
			UPDATE MapData SET data='"""+json.dumps(data2)+"""' WHERE id="""+str(mapData[0][0])+"""
			""")

		onProgressfunc(0.0)

		return data2




































