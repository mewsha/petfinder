#!/usr/bin/python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

class CuteOrNot(QDialog):
	def __init__(self):
		"""
		Initialize the window as a vertical layout.
		"""
		QDialog.__init__(self)
		layout = QVBoxLayout()
		
		label = QLabel("Cute Or Not?")
		pet1Button = QPushButton("Cuter")
		pet2Button = QPushButton("Cutest")
		
		layout.addWidget(label)
		layout.addWidget(button)
		
		self.setLayout(layout)


app = QApplication(sys.argv)
dialog = CuteOrNot()
dialog.show()
app.exec_()
