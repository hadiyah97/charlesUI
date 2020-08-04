from PyQt5.QtWidgets import QApplication
from ui.mainWindow import MainWindow
import RPi.GPIO as GPIO

sj2_arrive_pin = 18

def sj2_arrived(self):
    print("Signal Received")
    GPIO.cleanup()
    

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = MainWindow()
    
    #GPIO event 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17,  GPIO.IN)
    GPIO.add_event_detect(17,  GPIO.RISING,  sj2_arrived)
    
    ui.show()
    #ui.showFullScreen()

    sys.exit(app.exec_())

