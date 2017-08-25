#!/usr/bin/env python
# -*- coding: utf-8 -*

from multiprocessing import Process


class ThreadManager(object):
	def __init__(self):
		self.thread = []
		self.callbackFinished = []
		self.customCallback = []

	def __del__(self):
		for t in self.thread:
			t.join()

	def makeNewThread(self, threadfunction, callbackFinished, customCallback, data):
		self.callbackFinished.append(callbackFinished)
		self.customCallback.append(customCallback)
		self.thread.append(ThreadUser(self, len(self.thread), threadfunction, data))
		return self.thread[-1]

	def onThreadFinished(self, data, idThread):
		self.callbackFinished[idThread](data)

	def onThreadCustom(self, data, idThread):
		self.customCallback[idThread](data)

class ThreadUser(Process):
	def __init__(self, parent, idThread, threadfunction, dataStart):
		self.parent = parent
		self.threadfunction = threadfunction
		self.data = None
		self.dataStart = dataStart
		self.idThread = idThread
		super(ThreadUser, self).__init__()

	def run(self):
		self.data = self.threadfunction(self.customCallback, self.dataStart)
		self.parent and self.parent.onThreadFinished(self.data, self.idThread)

	def customCallback(self, data):
		self.parent and self.parent.onThreadCustom(data, self.idThread)

