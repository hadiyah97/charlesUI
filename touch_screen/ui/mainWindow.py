# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QDate,  QTime,  QDateTime,  Qt
#from gpiozero import LED
from time import sleep
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton



from .Ui_mainWindow import Ui_MainWindow

#led_red = LED(17)
#led_green = LED(27)
#led_blue = LED(22)

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        #led_red.on()
        self.progressBar.setValue(0)
        self.time.setText("Hi! Please select a room and press GO")
    
    @pyqtSlot()
    def on_openBox_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        print("Box opened")
        #date = QDate.currentDate()
        #time = QTime.currentTime()
        self.time.setText("Box opened")

        #led_red.off()
        #sleep(1)
        #led_green.on() 
    
    @pyqtSlot()
    def on_go_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        #raise NotImplementedError
        self.progressBar.setValue(0)
        self.time.setText("Please put your items in the box")
        self.time.repaint()
        sleep(1)
        # Message Box for item
        QMessageBox.question(self,  "Put Item",  "<FONT COLOR = 'White'> Did you put items in the box? </FONT>",  
        QMessageBox.No | QMessageBox.Yes)
        
        self.time.setText("Finding the room...")
        self.time.repaint()
        self.progressBar.setValue(5)
        sleep(1.5)
        self.progressBar.setValue(23)
        self.time.setText("Planning the route...")
        self.time.repaint()
        sleep(1)
        self.progressBar.setValue(38)
        sleep(3)
        self.progressBar.setValue(75)
        self.time.setText("Charles is ready! Heading to Room 226")
        sleep(1.7)
        self.progressBar.setValue(100)
        #Set GPIO to high to trigger SJ2 
    
    @pyqtSlot(str)
    def on_comboBox_activated(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type str
        """
        # TODO: not implemented yet
        #raise NotImplementedError

    @pyqtSlot()
    def on_progressBar_customContextMenuRequested(self, pos):
        """
        Slot documentation goes here.
        
        @param pos DESCRIPTION
        @type QPoint
        """
        # TODO: not implemented yet
        #raise NotImplementedError
    
    @pyqtSlot()
    def show_dialog(self):
        msgBox = QMessageBox() 
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Have you put itmes in Box? ")
        msgBox.setWindowTitle("Check Item!")
        msgBox.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        
        
        
    
