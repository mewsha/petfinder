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
		except Exception as e:
			print "Exception {0} {1}".format(type(e), e)
			return e
		return None
			
			
	def createTable(self):
		"""
		*** Need to add something to check to see if the database already
		exists, otherwise, for now, I'm assuming it does and not caling
		this function ***
		Creates a cuteornot database if it doesn't exist.
		Table stores the Pet Id, Name, Image URL.
		There may be ways to make this better with QtSQL.		
		"""
		self.con.execute("CREATE DATABASE petfinder")
		self.con.execute("USE petfinder")
		self.con.execute("CREATE TABLE cuteornot(Id INT PRIMARY KEY\
				          AUTO_INCREMENT, Name VARCHAR(25), ImageURL\
						  VARCHAR(50)")
		
	def queryTable(self):
		"""Dumps the data from the petfinder database"""
		self.con.execute("USE petfinder")
		self.con.execute("SHOW TABLE cuteornot")
		
	
	def increaseScore(self, pet):
		"""Increases the score for one pet"""
		pass
	
	def insertNewPet(self, pet):
		"""Inserts a new pet into the database"""
		pass
	
	def close(self):
		"""Close the database connection if it exists"""
		if(self.con is not None):
			self.con.close()
