#!/usr/bin/python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import urllib2
import WebServices

class CuteOrNot(QDialog):
	def __init__(self):
		"""
		Initialize the window as a vertical layout.
		"""
		QDialog.__init__(self)
		self.webServ = WebServices.WebServices()
		self.showPets()

	def layoutLeaderboard(self):
		layout = QGridLayout()
		
		label = QLabel("images here")
		label2 = QLabel("scroll here")

		layout.addWidget(label)
		layout.addWidget(label2)
		
		self.setLayout(layout)

	def layoutPets(self, pet1Data, pet2Data):
		layout = QGridLayout()
		
		label = QLabel("Cute Or Not?")
		pet1Image = QImage(pet1Data)
		pet2Image = QImage(pet2Data)
		pet1Button = QPushButton("Cuter")
		pet2Button = QPushButton("Cutest")
		exitButton = QPushButton("Close")
		leaderButton = QPushButton("Leaderboard")
		
		layout.addWidget(label)
		layout.addWidget(pet1Image, 0, 0)
		layouy.addWidget(pet2Image, 0, 1)
		layout.addWidget(pet1Button, 1, 0)
		layout.addWidget(pet2Button, 1, 1)
		layout.addWidget(exitButton, 2, 0)
		layout.addWidget(leaderButton, 2, 1)		
		
		self.setLayout(layout)
		
		exitButton.clicked.connect(self.close)
		

	def showPets(self):
		pet1Data = self.webServ.getAPet()
		pet2Data = self.webServ.getAPet()
		pet1ImgURL = pet1Data['photo']['$t']
		pet2ImgURL = pet2Data['photo']['$t']
		pet1ImgData = self.downloadImage(pet1ImgURL, "pet1.jpg")
		pet2ImgData = self.downloadImage(pet2ImgURL, "pet2.jpg")
		self.layoutPets(pet1ImgData, pet2ImgData)
		
	def downloadImage(self, url, filename):
		save_location = '~/Downloads/PetFinder/'+ filename
		response = urllib2.Request(url)
		imageData = urllib2.urlopen(response)
		image = imageData.read()
		return image
		
		
app = QApplication(sys.argv)
dialog = CuteOrNot()
dialog.show()
app.exec_()
