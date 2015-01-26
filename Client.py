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
		Initialize the window with a grid layout.
		"""
		QDialog.__init__(self)
		self.webServ = WebServices.WebServices()	
		layout = QGridLayout()
		self.setLayout(layout)
		self.showPets()
		self.setWindowTitle('Cute or Not?')

	def hideLayout(self, alayout):
		"""
		Hides all children of the layout
		"""
		#Think about using a QStackedWidget instead
		try:
			if (alayout is not None):	
				for i in range(alayout.count(), 0):
					item = alayout.itemAt(i)
					if isinstance(item, QWidgetItem):
						item.hide()
					else:
						self.clearLayout(item.layout())
			print self.layout()
			
		except (Exception) as e:
			print("An exception occured while clearing layouts,"
				  "{0} {1}").format(type(e), e)


	def clearLayout(self,layout):
		#print layout, type(layout)
		if(layout is not None):
			for i in range(layout.count()):
				item = layout.itemAt(i)
				#print item, type(item)
				#item.widget().hide()
				if (item is not None):
					item.widget().close()
				#item.widget().setParent(None)
				#layout.removeItem(item)
				#del item
			print self.layout()


	def stupidLayout(self, layout):
		"""
		Clears all children of the layout.
		"""
		#Think about using a QStackedWidget instead
		try:
			if (layout is not None):	
				for i in range(layout.count(), 0):
					item = layout.itemAt(i)
					if isinstance(item, QWidgetItem):
						pass #item.widget().close()
					else:
						self.clearLayout(item.layout())
					#if(item is not None):
						#item.deleteLater()
					#print item, type(item)
					#item.widget().setParent(None)
					#layout.removeItem(item)
					#del item
					item.widget().hide()
			print self.layout()
			
		except (Exception) as e:
			print("An exception occured while clearing layouts,"
				  "{0} {1}").format(type(e), e)

	def layoutLeaderboard(self):
		"""
		Created and displays UI for the leaderboard view
		"""
		layout = self.layout()

		label = QLabel("images here")
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
		"""
		print layout, type(layout)
		for i in range(layout.count()):
				item = layout.itemAt(i)
				print item, type(item)
				item.widget().hide()
		"""
		exitButton.clicked.connect(self.close)
		leaderButton.clicked.connect(self.showLeaderBoard)
		pet1Button.clicked.connect(self.increaseScore)
		pet2Button.clicked.connect(self.increaseScore)


	def showLeaderBoard(self):
		""" Show the leader board view in the window """
		#Add some stuff here to gather information for getting SQL data
		self.clearLayout(self.layout())
		self.layoutLeaderboard()

		
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
		"""
		#Add some stuff here to increment a score in a database
		pass	
		

app = QApplication(sys.argv)
dialog = CuteOrNot()
dialog.show()
app.exec_()
