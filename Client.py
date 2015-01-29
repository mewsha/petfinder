#!/usr/bin/python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import urllib
import urllib2
import WebServices
import DatabaseService

class CuteOrNot(QDialog):

	def __init__(self):
		"""
		Initialize the window with a grid layout.
		"""
		QDialog.__init__(self)
		self.petImageDisplayHeight = 300
		self.webServ = WebServices.WebServices()
		self.dataServ = DatabaseService.DatabaseService()
		errors = self.dataServ.generateConnection()
		if(errors is not None):
			raise RuntimeError("Connection with database could not be "
							   "established")
		layout = QGridLayout()
		self.setLayout(layout)
		self.showPets()
		self.setWindowTitle('Cute or Not?')


	def clearLayout(self,layout):
		"""
		Closes all children widgets of the current layout which will
			1- hide the widgets
			2- delete the widgets
		This prepares the layout for adding new widgets.
		(Grid layout is not removed.) 
		"""
		if(layout is not None):
			for i in range(layout.count()):
				item = layout.itemAt(i)
				if (item is not None):
					if(isinstance(item, QWidgetItem)):
						item.widget().close()
					else:
						self.clearLayout(item.layout())


	def layoutLeaderboard(self, petinfo):
		"""
		Creates and displays UI for the leaderboard view
		"""
		layout = self.layout()
		if (petinfo != () and petinfo != "" and petinfo is not None):
			label = QLabel(str(petinfo))
		else:
			label = QLabel("pet data")
		label2 = QLabel("scroll here")
		backButton = QPushButton("Back to Pets")

		layout.addWidget(label, 0, 1)
		layout.addWidget(label2, 0 , 2)
		layout.addWidget(backButton, 1, 0)
					
		backButton.clicked.connect(self.showPets)


	def layoutPets(self, pet1Data, pxmap1, pet2Data, pxmap2):
		"""
		Creates and displays UI for the Pet view. 
		"""
		layout = self.layout()

		label = QLabel("Cute Or Not?")
		pet1Image = QLabel(self)
		pet2Image = QLabel(self)
		imgpolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		pet1Image.setSizePolicy(imgpolicy)
		pet2Image.setSizePolicy(imgpolicy)
		pet1Image.setFixedHeight(self.petImageDisplayHeight)
		pet2Image.setFixedHeight(self.petImageDisplayHeight)
		pet1Image.setPixmap(pxmap1.scaledToHeight(pet1Image.height()))
		pet2Image.setPixmap(pxmap2.scaledToHeight(pet2Image.height()))
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

		exitButton.clicked.connect(self.closeWindow)
		leaderButton.clicked.connect(self.showLeaderBoard)
		pet1Button.clicked.connect(lambda: self.increaseScore(pet1Data))
		pet2Button.clicked.connect(lambda: self.increaseScore(pet2Data))


	def closeWindow(self):
		"""
		Allows the database service to close it's connection 
		with the MySQL server before closing the window and application.
		"""
		self.dataServ.close()
		self.close()


	def showLeaderBoard(self):
		""" Show the leader board view in the window """
		tabledata = self.dataServ.queryTable()
		self.clearLayout(self.layout())
		self.layoutLeaderboard(tabledata)

		
	def showPets(self):
		""" Show the pet view in the window """
		pet1Data, pet2Data = self.webServ.getAPet(), self.webServ.getAPet()
		pet1Image = self.webServ.downloadPhoto(pet1Data)
		pet2Image = self.webServ.downloadPhoto(pet2Data)
		self.clearLayout(self.layout())
		self.layoutPets(pet1Data, pet1Image, pet2Data, pet2Image)


	def increaseScore(self, pet):
		"""
		Increment the score for the pet on the leaderboard.
		This will add a new pet if the pet doesn't exist.
		This also refreshes the two pets currently shown.
		"""
		self.dataServ.increaseScore(pet)
		self.showPets()
		pass	
		

app = QApplication(sys.argv)
dialog = CuteOrNot()
dialog.show()
app.exec_()
