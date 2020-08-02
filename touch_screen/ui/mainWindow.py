# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QDate,  QTime,  QDateTime,  Qt
from gpiozero import LED
from time import sleep

from .Ui_mainWindow import Ui_MainWindow

led_red = LED(17)
led_green = LED(27)
led_blue = LED(22)

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
        led_red.on()
    
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
        led_red.off()
        sleep(1)
        led_green.on() 
        

    
