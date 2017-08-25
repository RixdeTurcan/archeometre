#!/usr/bin/env python
# -*- coding: utf-8 -*
from threadmanager import ThreadManager
import random
import math

def simulateArcheometre(customCallback, dataInput):
	sizeX = dataInput[0]
	sizeY = dataInput[1]
	marginX = dataInput[2]
	marginY = dataInput[3]
	timeStep = dataInput[4]
	data = dataInput[5]
	attractorList = dataInput[6]
	nexusList = dataInput[7]
	subSampling = dataInput[8]
	spreadMat = dataInput[9][0]
	rngMeanAttractor = dataInput[9][1]
	rngVarAttractor = dataInput[9][2]
	powerAttractor = dataInput[9][3]
	rngMeanNexus = dataInput[9][4]
	rngVarNexus = dataInput[9][5]
	powerNexus = dataInput[9][6]
	elemId = dataInput[10]

	lx = sizeX+2*marginX
	ly = sizeY+2*marginY

	data2 = [None]*lx
	for x in range(len(data)):
		data2[x] = [0.]*ly

	spreadMatSize = len(spreadMat)
	spreadMatMid = (spreadMatSize-1)/2
	sumSpread = 0.
	for x in range(spreadMatSize):
		for y in range(spreadMatSize):
			sumSpread += spreadMat[x][y]
	for x in range(spreadMatSize):
		for y in range(spreadMatSize):
			spreadMat[x][y] /= sumSpread

	for x in range(lx):
		if x%2==0:
			customCallback(round(100.*x/float(lx), 1))

		for y in range(ly):
			val = data[x][y]
			dx = 0
			dy = 0
			for a in attractorList:
				aId = 0
				while  a[0][aId][0] != elemId:
					aId+=1
				p = a[0][aId][1]

				if p>0.000001:

					rx = a[1]-x
					ry = a[2]-y
					r = math.sqrt(rx*rx+ry*ry) + 80./subSampling
					r = r*subSampling/600.
					alpha = math.atan2(ry, rx) + (random.random()*2.-1.)*rngVarAttractor + rngMeanAttractor

					a = powerAttractor*max(4.*(r-r*r)*2.-1., 0.)*p*0.05/max(1., pow(val/3., 1.))

					dx += a*math.cos(alpha)
					dy += a*math.sin(alpha)

			for n in nexusList:
				timings = n[1][3]
				if timeStep>=timings[0] and timeStep<timings[2]:
					rx = n[1][1]-x
					ry = n[1][2]-y

					nId = 0
					while  n[1][4][nId][0] != elemId:
						nId+=1
					p = n[1][4][nId][1]

					if p>0.000001:

						r = max(1., math.sqrt(rx*rx+ry*ry))*subSampling/600.
						alpha = math.atan2(ry, rx) + (random.random()*2.-1.)*rngVarNexus + rngMeanNexus

						factor = (timeStep-timings[0])/float(timings[1]-timings[0])
						if timeStep>timings[1]:
							factor = -(timings[2]-timeStep)/float(timings[2]-timings[1])
							alpha = math.atan2(ry, rx) + (random.random()*2.-1.)*rngVarNexus - rngMeanNexus
						a = powerNexus*min(max(4.*factor*p*(r-r*r), -10.), 10.)

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
				data2[x][y] -= random.random()*0.2*(data2[x][y]-6.)
			data2[x][y] = round(data2[x][y], 3)

	customCallback(0.0)

	return [data2, elemId, timeStep]














