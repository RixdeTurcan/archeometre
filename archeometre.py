#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import os.path
from archeometre_init import *

class Archeometre:
	def __init__(self): 
		self.db = sqlite3.connect("archeometre.db")
		
		if not os.path.isfile("archeometre.db"):
			initArcheometre(self)
		
	def __del__(self):
		self.db.close()
		
	def executeRequest(self, request):
		cursor = self.db.cursor()
		cursor.execute(request)
		self.db.commit()
		if request.find("SELECT")!=-1:
			return cursor.fetchall()