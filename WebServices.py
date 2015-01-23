#!/usr/lib/python

import urllib2
import JSON

class WebServices(object):
	URL = "http://api.petfinder.com/"
	apiModule = "pet.getRandom"
	apiKey = "?key=33faa4e89fd6859ab68709e31dd139b5"
	apiFormat = "&format=json"
	apiOutput = "&output=basic"
	
	URI = URL+apiModule+apiKey+apiFormat+apiOutput
	
	def __init__(self):
		pass
		
	def requestPetData(self):
		pass
	
	def interpretJSONData(self, data):
		pass
		
	def getPet():
		pass
		
