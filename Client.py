#!/usr/bin/python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import urllib
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
		self.setWindowTitle('Cute or Not?')

	def layoutLeaderboard(self):
		"""
		Created and displays UI for the leaderboard view
		"""
		layout = QGridLayout()
		label = QLabel("images here")
		label2 = QLabel("scroll here")
		backButton = QPushButton("Back to Pets")

		layout.addWidget(label, 0, 1)
		layout.addWidget(label2, 0 , 2)
		layout.addWidget(backButton, 1, 0)
				
		self.setLayout(layout)
		
		backbButton.clicked.connect(self.showPets)

	def layoutPets(self, pet1Data, pet2Data):
		"""
		Creates and displays UI for the Pet view. 
		"""
		pet1Image = QLabel(self)
		pet2Image = QLabel(self)
		imgpolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		pet1Image.setSizePolicy(imgpolicy)
		pet2Image.setSizePolicy(imgpolicy)
			
		layout = QGridLayout()
		
		label = QLabel("Cute Or Not?")
		pxmap1 = QPixmap(pet1Data)
		pxmap2 = QPixmap(pet2Data)
		pet1Image.setPixmap(pxmap1)
		pet2Image.setPixmap(pxmap2)
		pet1Image.setFixedHeight(300)
		pet2Image.setFixedHeight(300)
		pet1Button = QPushButton("I'm Cuter!")
		pet2Button = QPushButton("I'm Cutest!")
		exitButton = QPushButton("Close")
		leaderButton = QPushButton("Leaderboard")
		
		layout.addWidget(label, 0, 0)
		layout.addWidget(pet1Image, 1, 0)
		layout.addWidget(pet2Image, 1, 1)
		layout.addWidget(pet1Button, 2, 0)
		layout.addWidget(pet2Button, 2, 1)
		layout.addWidget(exitButton, 3, 0)
		layout.addWidget(leaderButton, 3, 1)		
		
		self.setLayout(layout)
		
		exitButton.clicked.connect(self.close)
		
		
	def showPets(self):
		"""
		Show the pet view in the window
		"""
		pet1Data = self.webServ.getAPet()
		pet2Data = self.webServ.getAPet()
		pet1ImgURL = pet1Data['photo']['$t']
		pet2ImgURL = pet2Data['photo']['$t']
		pet1ImgData = self.downloadImage(pet1ImgURL)
		pet2ImgData = self.downloadImage(pet2ImgURL)
		self.layoutPets(pet1ImgData, pet2ImgData)
		
	def downloadImage(self, url):
		"""
		Download the pet image from a given url.
		
		Returns:
		QImage object with the pet's image
		"""
		imagefile = QImage()
		urldata = urllib2.urlopen(url)
		imagedata = urldata.read()
		imagefile.loadFromData(imagedata)
		return imagefile
		
app = QApplication(sys.argv)
dialog = CuteOrNot()
dialog.show()
app.exec_()
