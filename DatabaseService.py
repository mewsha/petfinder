#! /usr/lib/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb

class DatabaseService(object):
	
	def __init__(self):
		self.con = None
		pass
		
		
	def generateConnection(self):
		""" 
		Creates a connection with the local database 
		
		Returns:
		Success returns None. Failure returns an exception. 
		"""
		try:
			self.con = mdb.connect('localhost', 
								   'testuser', 
								   'test623', 
								   'petfinder')
			self.cur = self.con.cursor()
		except Exception as e:
			print "Cannot connect to db: {0} {1}".format(type(e), e)
			return e
		return None
			
			
	def createTable(self):
		"""
		Creates a cuteornot table if it doesn't exist.
		Table stores the Pet Id, Name, Image URL.
		There may be ways to make this better with QtSQL.	
		
		Table has three columns:
		Name, ImageURL and Id	
		"""
		#Need to add something to check to see if the database already
		#exists, until then, I'm assuming it does and not calling
		#this function
		self.cur.execute("CREATE DATABASE petfinder")
		self.cur.execute("USE petfinder")
		self.cur.execute("CREATE TABLE cuteornot(Id INT PRIMARY KEY " 
				          "AUTO_INCREMENT,"
				          "IdNum VARCHAR(25),"
				          "Name VARCHAR(50),"
				          "ImageURL VARCHAR(100)")
		
	def queryTable(self):
		"""
		Dumps the data from the petfinder database.
		
		Returns:
		Data encapsulated in (), python readable as tuples.
		"""
		#It would be nice if data was ret python formatted as [{} {}]
		self.cur.execute("USE petfinder")
		self.cur.execute("SELECT * FROM cuteornot")
		data = self.cur.fetchall()
		return data
		
	
	def increaseScore(self, pet):
		"""
		Increases the score for one pet or adds a new pet if the
		pet does not yet exist in the database
		"""
		#add something in here that searches the database to see if 
		#the pet already exists. If it does, increase the score. 
		#If the pet doesn't exist, insert a new pet into the database
		#For now, always inserting pet. It's unlikely to 
		#come across the same pet since the database is pretty large
		self.insertNewPet(pet)
			
	
	def insertNewPet(self, pet):
		"""Inserts a new pet into the database"""
		idNum = pet['id']
		name = pet['name']
		url = pet['photo']
		cols = "IdNum, Name, ImageURL"
		values = "'{0}', '{1}', '{2}'".format(idNum, name, url)
		
		executionStr = ("INSERT INTO cuteornot({0}) VALUES"
					    "({1})").format(cols, values)
		try:
			self.cur.execute("USE petfinder")
			self.cur.execute(executionStr)
		except Exception as e:
			print("Database Insert Exception {0} {1}\n"
				  "{2}").format(type(e), e, values)
		
	
	def close(self):
		"""Close the database connection if it exists"""
		if(self.con is not None):
			self.con.close()
