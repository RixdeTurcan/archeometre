#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

def initArcheometre(self):
	self.executeRequest("""
	CREATE TABLE IF NOT EXISTS Map(
		id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
		name TEXT,
		sizeX INTEGER,
		sizeY INTEGER,
		posXView INTEGER,
		posYView INTEGER,
		urlBackground TEXT,
		pixelSize REAL,
		startDate TEXT,
		viewTimes TEXT,
		magicFieldInit TEXT,
		deleted INTEGER
	)
	""")
	self.executeRequest("""
	CREATE TABLE IF NOT EXISTS MapData(
		id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
		x INTEGER,
		y INTEGER,
		time INTEGER,
		data TEXT
	)
	""")
	self.executeRequest("""
	CREATE TABLE IF NOT EXISTS Attractor(
		id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
		mapId INTEGER,
		data TEXT,
		x INTEGER,
		y INTEGER
	)
	""")
	self.executeRequest("""
	CREATE TABLE IF NOT EXISTS Nexus(
		id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
		mapId INTEGER,
		startTime INTEGER,
		peakTime INTEGER,
		endTime INTEGER,
		data TEXT
	)
	""")
	#self.executeRequest("""
	#CREATE TABLE IF NOT EXISTS Domain(
	#	id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	#	name TEXT,
	#	elementId INTEGER
	#)
	#""")
	self.executeRequest("""
	CREATE TABLE IF NOT EXISTS Element(
		id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
		name TEXT
	)
	""")

	self.executeRequest(""" INSERT INTO Element(name) VALUES("Feu") """)
	self.executeRequest(""" INSERT INTO Element(name) VALUES("Terre") """)
	self.executeRequest(""" INSERT INTO Element(name) VALUES("Lune") """)
	self.executeRequest(""" INSERT INTO Element(name) VALUES("Eau") """)
	self.executeRequest(""" INSERT INTO Element(name) VALUES("Air") """)

	idFeu = self.executeRequest(""" SELECT id FROM Element WHERE name="Feu" """)[0][0]
	idTerre = self.executeRequest(""" SELECT id FROM Element WHERE name="Terre" """)[0][0]
	idLune = self.executeRequest(""" SELECT id FROM Element WHERE name="Lune" """)[0][0]
	idEau = self.executeRequest(""" SELECT id FROM Element WHERE name="Eau" """)[0][0]
	idAir = self.executeRequest(""" SELECT id FROM Element WHERE name="Air" """)[0][0]

	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Conflit", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("décision", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Justice", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Progression", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Effort", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Foudre", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Lumière", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Volcan", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Désert", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Torche", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("armure", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Bûcher", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Forge", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Guerre", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Pouvoir", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Révolte", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Erotique", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Passionné", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Expansif", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Joyeux", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Colérique", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Hérétique", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Dévot", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Volonté", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Hâte", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Fanatisme", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Violence", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Audace", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Royauté", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Fer", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Bronze", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Rubis", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Rouge", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Orangé", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Gris centre", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Louve", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Salamandre", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Lion", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Taureau", """+str(idFeu)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Dragon", """+str(idFeu)+""") """)

	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Plénitude", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Primordial", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Forme", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Ordonnancement", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Renouveau", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Vie", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Printemps", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Grotte", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Séisme", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Fertilité", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Réceptable", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Corps", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Cenin", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Herbier", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Armes de jet", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Promesse", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Artisanat", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Médecine", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Paysannerie", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Architecture", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Exaltation", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Espoir", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Mélancolique", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Fatalisme", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Respect", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Sauvagerie", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Inaltérabilité", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Eternité", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Solidité", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Sensualité", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Boue", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Cuivre", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Lin", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Bois", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Pierre", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Vert", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Brun", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Safran", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Chien", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Rat", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Ours", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Taupe", """+str(idTerre)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Darfadet", """+str(idTerre)+""") """)

	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Chaos", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Sublimation", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Ambiguïté", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Subjectivité", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Subversion", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Folie", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Rêve", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Illusion", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Eclipse", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Drogue", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Bijou", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Miroir", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Masque", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Maquillage", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Piège", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Dissimulation", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Mensonge", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Provocation", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Séduction", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Théâtre", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Sorcellerie", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Incompréhension", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Trouble", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Peur", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Tentation", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Désir", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Beauté", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Chaos", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Monstruosité", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Incongruité", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Mystère", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Incohérent", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Argent", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Obsidienne", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Pierre de Lune", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Améthyste", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Noir", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Blanc", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Gris", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Insecte", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Corbeau", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Reptile", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Chat", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Caméléon", """+str(idLune)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Loup", """+str(idLune)+""") """)

	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Harmonie", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Changement", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Oubli", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Mémoire", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Equilibre", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Pluie", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Océan", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Raz de marée", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Akasha", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Erosion", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Calice", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Longue vue", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Ecaille", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Armes de mêlée", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Navigation", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Vol", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Diplomatie", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Espionnage", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Surveillance", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Réserve", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Tristesse", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Fantasie", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Douceur", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Fureur", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Précision", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Vitesse", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Discrétion", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Secret", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Imprévisibilité", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Mercure", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Turquoise", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Perle", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Corail", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Nacre", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Bleu", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Vert clair", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Violet", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Dauphin", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Baleine", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Pieuvre", """+str(idEau)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Sirène", """+str(idEau)+""") """)

	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Liberté", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Mouvement", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Transgression", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Connaissance", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Abstraction", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Souffle", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Son", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Ouragan", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Nuage", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Parfum", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Voix", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Grand édifice", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Arc", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Voile", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Arme de Trait", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Vol", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Voyage", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Musique", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Discours", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Ecriture", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Exploration", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Insouciance", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Flegme", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Sérénité", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Compréhension", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Légèreté", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Recueillement", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Insaisissable", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Intelligence", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Inspiration", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Sagesse", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Rigueur", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Héraut", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Sagesse", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Rigueur", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Héraut", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Etain", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Saphir", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Tulle", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Ether", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Bleu", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Blanc", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Jaune", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Cheval", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Aigle", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Colombe", """+str(idAir)+""") """)
	#self.executeRequest(""" INSERT INTO Domain(name, elementId) VALUES("Hibou", """+str(idAir)+""") """)

































