#! /usr/lib/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb

class DatabaseService(object):
	
	def __init__(self):
		self.con = None
		pass
		
		
	def generateConnection(self):
		try:
			self.con = mdb.connect('localhost', 'testuser', 'test623', 'testdb')
			self.cur = self.con.cursor()
		except Exception as e:
			print "Exception {0} {1}".format(type(e), e)
			return e
		return None
			
			
	def createTable(self):
		"""
		*** Need to add something to check to see if the database already
		exists, until then, I'm assuming it does and not calling
		this function ***
		Creates a cuteornot database if it doesn't exist.
		Table stores the Pet Id, Name, Image URL.
		There may be ways to make this better with QtSQL.		
		"""
		self.cur.execute("CREATE DATABASE petfinder")
		self.cur.execute("USE petfinder")
		self.cur.execute("CREATE TABLE cuteornot(Id INT PRIMARY KEY\
				          AUTO_INCREMENT, Name VARCHAR(25), ImageURL\
						  VARCHAR(50)")
		
	def queryTable(self):
		"""Dumps the data from the petfinder database"""
		self.cur.execute("USE petfinder")
		self.cur.execute("SELECT * FROM cuteornot")
		data = self.cur.fetchall()
		return data
		
	
	def increaseScore(self, pet):
		"""Increases the score for one pet"""
		#add something in here that searches the database to see if 
		#the pet already exists. If it does, increase the score. 
		#If the pet doesn't exist, insert a new pet into the database
		#For now, always inserting a New pet, plus it's unlikely to 
		#come across a new pet since the database is pretty large
		self.insertNewPet(pet)
		pass
	
	def insertNewPet(self, pet):
		"""Inserts a new pet into the database"""
		name = pet['name']
		idNum = pet['id']
		url = pet['photo']
		
		self.cur.execute("USE petfinder")
		executionStr = ("INSERT INTO cuteornot(Name) VALUES"
					   "('{0}')").format(name)
		self.cur.execute(executionStr)
		
	
	def close(self):
		"""Close the database connection if it exists"""
		if(self.con is not None):
			self.con.close()
