import pygame, sys, random, os, time, datetime
import RPi.GPIO as GPIO
import serial
import string

ser = serial.Serial ("/dev/ttyAMA0", timeout=1)
ser.baudrate = 57600
number = 1
data = number
#ser.write(data)
ser.open()
ser.write('\n')
ser.write("testing")
ser.write('\n')

time.sleep(1)
while(1):
	
	ser.write('\n')
	ser.write("testing")
	ser.write('\n')
	response = ser.readline()
	#print "hello"
	if response != "testing"+'\n' and response != '\n':
		print response
	#time.sleep(1)
	#print ser.readline()

ser.close()

'''#!/usr/bin/env python

import serial
import string

rot13 = string.maketrans( 
    "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz", 
    "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")

test=serial.Serial("/dev/ttyAMA0",9600)
test.open()

try:
    while True:
                line = test.readline()
                test.write(string.translate(line, rot13))
               
                
except KeyboardInterrupt:
    print "# do cleanup here"

test.close()'''


