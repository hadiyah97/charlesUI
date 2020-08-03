#!/usr/bin/python3
import time
import serial

class Uart:

    serial_port = None

    def __init__(self, baud):
        self.serial_port=serial.Serial(
        port="/dev/ttyTHS1",
        baudrate=baud,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        )
        # wait 1 second for serial port to initialize
        time.sleep(1)

    def send(self, message):
        try:
            self.serial_port.write(message.encode())
            print("sent message: ", message, "\n")
        
        except Exception as exception_error:
            print("Error occured\n")


    def read(self):
        return("chyez")

    def cleanup(self):
        self.serial_port.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cleanup()



