#!/usr/bin/python

from PyQt4 import QtCore
from PyQt4 import QtGui
import sys
import WebServices
import DatabaseService

class CuteOrNot(QtGui.QDialog):

	def __init__(self):
		"""
		Initialize the window with a grid layout.
		"""
		QtGui.QDialog.__init__(self)
		self.petImgDispH = 300
		self.petSmImgDispH = 150
		self.webServ = WebServices.WebServices()
		self.dataServ = DatabaseService.DatabaseService()
		errors = self.dataServ.generateConnection()
		if(errors is not None):
			raise RuntimeError("Connection with database could not be "
							   "established")
		layout = QtGui.QGridLayout()
		self.setLayout(layout)
		self.showPets()
		self.setWindowTitle('Cute or Not?')


	def clearLayout(self,layout):
		"""
		Closes all children widgets of the current layout which will
			1- hide the widgets
			2- delete the widgets
		This prepares the layout for adding new widgets.
		(Base Grid layout is not removed.) 
		"""
		if(layout is not None):
			for i in range(layout.count()):
				item = layout.itemAt(i)
				if (item is not None):
					if(isinstance(item, QtGui.QWidgetItem)):
						item.widget().close()
					else:
						self.clearLayout(item.layout())


	def layoutLeaderboard(self, petsinfo):
		"""
		Creates and displays UI for the leaderboard view
		"""
		layout = self.layout()
		if (petsinfo != () and petsinfo != "" and petsinfo is not None):
			currRow = 0
			maxCols = 5
			for i in range(len(petsinfo)):
				currCol = i % maxCols
				petdata = petsinfo[i]
				label = QtGui.QLabel(str(petdata['name']))
				label.setFixedHeight(30)
				petimage = self.createPetImageLabel(petdata,
													self.petSmImgDispH)
				isColZero = i % maxCols
				if(isColZero==0):
					currRow=currRow+2
				#set the label to be above the pet image
				layout.addWidget(label, currRow, currCol)
				layout.addWidget(petimage, currRow+1, currCol)
		else:
			label = QtGui.QLabel("no pet data")
			label.addWidget(label, 0, 1)
			
		backButton = QtGui.QPushButton("Back to Pets")
		layout.addWidget(backButton, currRow+2, 0)
			
		backButton.clicked.connect(self.showPets)
		
		self.adjustSize()

	def createPetImageLabel(self, petData, imgHeight):
		"""
		Creates a QtGui QLabel with an image as the set pixmap. The
		image is obtained via a pet's url in petData and downloaded
		by the WebServices.
		
		Returns:
		QtGui.QLabel
		"""
		petpxmap = self.webServ.downloadPhoto(petData)
		petImage = QtGui.QLabel(self)
		imgPolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
									 QtGui.QSizePolicy.Fixed)
		petImage.setSizePolicy(imgPolicy)
		petImage.setFixedHeight(imgHeight)
		petImage.setPixmap(petpxmap.scaledToHeight(imgHeight))
		return petImage
		

	def layoutPets(self, pet1Data, pxmap1, pet2Data, pxmap2):
		"""
		Creates and displays UI for the Pet view. 
		"""
		layout = self.layout()
		
		label = QtGui.QLabel("Cute Or Not?")
		pet1Image = self.createPetImageLabel(pet1Data, self.petImgDispH)
		pet2Image = self.createPetImageLabel(pet2Data, self.petImgDispH)
		pet1Button = QtGui.QPushButton("I'm Cuter!")
		pet2Button = QtGui.QPushButton("I'm Cutest!")
		exitButton = QtGui.QPushButton("Close")
		leaderButton = QtGui.QPushButton("Leaderboard")
		
		layout.addWidget(label, 0, 0)
		layout.addWidget(pet1Image, 1, 0)
		layout.addWidget(pet2Image, 1, 1)
		layout.addWidget(pet1Button, 2, 0)
		layout.addWidget(pet2Button, 2, 1)
		layout.addWidget(exitButton, 3, 0)
		layout.addWidget(leaderButton, 3, 1)

		self.adjustSize()
		
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
		petsinfo = self.dataServ.queryTable()
		self.clearLayout(self.layout())
		self.layoutLeaderboard(petsinfo)
		
		
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
		

app = QtGui.QApplication(sys.argv)
dialog = CuteOrNot()
dialog.show()
app.exec_()
