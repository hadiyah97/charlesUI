#!/usr/bin/python3
import uart
import enum

value = '-1'

STOP = '0'
FORWARD = '1'
BACKWARD = '2'
LEFT = '3'
RIGHT = '4'
F_LEFT = '5'
B_LEFT = '6'
F_RIGHT = '7'
B_RIGHT = '8'
CLOCKWISE = '9'
ANTICLOCKWISE = '10'


with uart.Uart(115200) as stateManager:
    while value != '0':
        print("Please choose an option:")
        print("1. Send message")
        print("0. exit")
        value = input()

        if(value == '1'):
            mssg = input("enter message: ")
            stateManager.send(mssg)
        

