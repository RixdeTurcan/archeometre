#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

def getElementData(name):
	spreadMat = [
	[0.0, 0.0, 0.0],
	[0.0, 1.0, 0.0],
	[0.0, 0.0, 0.0]
	]
	attractorMean = 0.0
	attractorVar = 0.0
	powerAttractor = 1.0
	nexusMean = 0.0
	nexusVar = 0.0
	powerNexus = 1.0

	if name=="Eau":
		spreadMat = [
		[2.0, 2.5, 2.0],
		[2.5, 3.0, 2.5],
		[2.0, 2.5, 2.0]
		]
		attractorMean = 0.8
		attractorVar = 0.4
		nexusMean = 1.0
		nexusVar = 0.2
		powerAttractor = 1.0
		powerNexus = 1.0

	elif name=="Terre":
		spreadMat = [
		[2.0, 3.5, 2.0],
		[3.5, 5.5, 3.5],
		[2.0, 3.5, 2.0]
		]
		attractorMean = 0.0
		attractorVar = 0.8
		nexusMean = 0.0
		nexusVar = 0.5
		powerAttractor = 0.8
		powerNexus = 0.8

	elif name=="Lune":
		spreadMat = [
		[random.random(), 0.1*random.random(), random.random()],
		[0.1*random.random(), 0.02*random.random(), 0.1*random.random()],
		[random.random(), 0.1*random.random(), random.random()]
		]
		attractorMean = (random.random()*2.-1.)*1.5
		attractorVar = random.random()
		nexusMean = (random.random()*2.-1.)*1.5
		nexusVar = random.random()
		powerAttractor = random.random()*2.5
		powerNexus = random.random()*0.5+0.5

	elif name=="Air":
		spreadMat = [
		[5.0, 1.0, 5.0],
		[1.0, 2.0, 1.0],
		[5.0, 1.0, 5.0]
		]
		attractorMean = (random.random()*2.-1.)*0.3
		attractorVar = 0.6
		nexusMean = 1.2
		nexusVar = 0.6
		powerAttractor = 1.2
		powerNexus = 1.2

	elif name=="Feu":
		spreadMat = [
		[2.0, 1.0, 2.0],
		[1.0, 0.0, 1.0],
		[2.0, 1.0, 2.0]
		]
		attractorMean = (random.random()*2.-1.)*1.5
		attractorVar = 0.1
		nexusMean = (random.random()*2.-1.)*1.5
		nexusVar = 0.1
		powerAttractor = 2.0
		powerNexus = 2.0

	return [spreadMat, attractorMean, attractorVar, powerAttractor, nexusMean, nexusVar, powerNexus]
