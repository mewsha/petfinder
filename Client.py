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
		pxmap1 = QPixmap(pet1Data)
		print pxmap1
		pxmap2 = QPixmap(pet2Data)
		print pxmap2
		pet1Image = QLabel(self)
		pet2Image = QLabel(self)
		pet1Image.setPixmap(pxmap1)
		pet2Image.setPixmap(pxmap2)
		pet1Button = QPushButton("Cuter")
		pet2Button = QPushButton("Cutest")
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
		self.setWindowTitle('Cute or Not?')
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
		imagefile = QImage()
		#save_spot = '~/Downloads/'+ filename
		#response = urllib2.Request(url)
		urldata = urllib2.urlopen(url)
		imagedata = urldata.read()
		imagefile.loadFromData(imagedata)
		#urllib.urlretrieve(url, save_spot)
		#image = None
		return imagefile
		
app = QApplication(sys.argv)
dialog = CuteOrNot()
dialog.show()
app.exec_()
