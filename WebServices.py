#!/usr/bin/python

from PyQt4 import QtGui
import urllib2
import json


class WebServices(object):
	apiURL = "http://api.petfinder.com/"
	apiModule = "pet.getRandom"
	apiKey = "?key=33faa4e89fd6859ab68709e31dd139b5"
	apiFormat = "&format=json"
	apiOutput = "&output=basic"
	apiURI = apiURL+apiModule+apiKey+apiFormat+apiOutput
	
	
	def __init__(self):
		self.apiURI = WebServices.apiURI
		pass


	def requestPetData(self):
		"""
		Obtain pet data for a random pet through petfinder.com
		
		Returns:
		JSON object with petfinder data
		"""
		
		jsonInfo = None
		try:
			response = urllib2.Request(self.apiURI)
			petData = urllib2.urlopen(response)
			jsonInfo = petData.read()
		except (urllib2.HTTPError, IOError, Exception) as e:
			print "An Exception occured: {0}, {1}".format(type(e), e)
		return jsonInfo		
	
	
	def interpretJSONData(self, jsonData):
		"""
		Given JSON data, this function returns a python dictionary
		
		Retuns:
		Dict equivalent to JSON data
		"""
		
		data = ""
		try:
			if(jsonData is None or jsonData == ""):
				raise RuntimeError("There is no json data to decode")
			else:
				data = json.loads(jsonData)
		except Exception as e:
			print("An exception occured while formatting JSON:"
				  "{0} {1}").format(type(e), e)
		return data
		
		
	def pickPhoto(self, petData):
		"""
		Given a dictionary of pet data from petfinder.com's randompet
		module, this will return a dictionary of pet information.
		
		Returns:
		Dict {id:"petid", name:"petname", photo:"photoURL"}
		"""
		
		data = ""
		if(petData is None or petData == ""):
			raise RuntimeError("There is no pet data to pick a photo")
		else:
			media = petData['media']
			photo = media['photos']['photo'][2]
			
			data = {'id':petData['id'], 
					'name':petData['name'],
					'photo':photo}
		return data
		

	def downloadPhoto(self, pet):
		"""
		Download the pet image from a given url.
		
		Returns:
		QPixmap object with the pet's image
		"""
		url = pet['url']
		imagefile = QtGui.QImage()
		displayImage = None
		urldata = urllib2.urlopen(url)
		imagedata = urldata.read()
		imagefile.loadFromData(imagedata)
		displayImage = QtGui.QPixmap(imagefile)
		return displayImage
		

	def getAPet(self):
		"""
		Gets pet data from the petfinder.com api and returns photo info.
		
		Returns:
		Dict {id:"petid", name:"petname", photo:"photoURL"}
		"""
		try:
			jsonData = self.requestPetData()
			finderData = self.interpretJSONData(jsonData)
			
			petData = finderData['petfinder']['pet']
			name = petData['name']['$t']
			idNum = petData['id']['$t']
			media = petData['media']
			photo = media['photos']['photo'][2]['$t']
			
			pet =  {'id':idNum, 
					'name':name,
					'url':photo}
			return pet
		except (TypeError, KeyError):
			#AFAP: Pet does not contain data needed, pick again
			return self.getAPet()
		except Exception as e:
			print("An exception occured while getting a pet"
				  "{0} {1}").format(type(e), e)
		
		
	if(__name__ == '__main__'):
		petData = getAPet()
		print petData
