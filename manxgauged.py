#!/usr/bin/env python
# -*- coding: utf-8 -*-



'''
Import pygame for graphics, import sys for exit function, random for random numbers
os is used for environment variables to set the position to centre
'''
import pygame, sys, random, os, time, datetime
import RPi.GPIO as GPIO
import math
import subprocess
import commands
import serial
import string

#ctypes.CDLL('librt.so', mode=ctypes.RTLD_GLOBAL)
size=(800,480)
GPIO.setmode(GPIO.BCM)

'''import constants used by pygame such as event type = QUIT'''
from pygame.locals import * 
from wm_ext.appwnd import AppWnd
#from wmctrl import *


'''Dune Buggy Information'''
dune_buggy_owner = "Bernie"
number_points_cvjoint_speedsensor = 6
wheelcircumference = 0.0014379




'''Initialize pygame components'''
pygame.init()
screen=pygame.display.set_mode(size, DOUBLEBUF)
flags=screen.get_flags()  

'''
Centres the pygame window. Note that the environment variable is called 
SDL_VIDEO_WINDOW_POS because pygame uses SDL (standard direct media layer)
for it's graphics, and other functions
'''
os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'

'''Set the window title'''
pygame.display.set_caption("manxgauged")

'''Initialize a display with width 370 and height 542 with 32 bit colour'''
screen = pygame.display.set_mode((800, 480), 0, 32)

'''Create variables with image names we will use'''
backgroundfile = "dashbackground.png"
crosshairsfile = "crosshairsmouse.png"
pifile = "pi.png"
needlefile = "needle.png"
headlightsoff = "headlightsoff.png"
headlightson = "headlightson.png"
highbeamon = "highbeamon.png"
highbeamoff = "highbeamoff.png"
lightbaron = "lightbaron.png"
lightbaroff = "lightbaroff.png"
wiperon = "wiperon.png"
wiperoff = "wiperoff.png"
wiperpluson = "wiperpluson.png"
wiperplusoff = "wiperplusoff.png"
wiperminuson = "wiperminuson.png"
wiperminusoff = "wiperminusoff.png"
hornon = "hornon.png"
hornoff = "hornoff.png"
musicbutton = "musicbutton.png"
gpsbutton = "gpsbutton.png"
oillighton = "oil_light.png"
alternatorlighton = "alternator_light.png"
enginetemperature_lighton = "enginetemperature_light.png"
lowfuel_lighton = "lowfuel_lighton.png"

turn_left_lighton = "turn_left_light.png" 
turn_right_lighton = "turn_right_light.png"
traction_left_lighton = "traction_left_light.png"
traction_right_lighton = "traction_right_light.png"
highbeam_lighton = "highbeam_lighton.png"
#Fuel Gauge
xfuel1 = "fuel1.png"
xfuel2 = "fuel2.png"
xfuel3 = "fuel3.png"
xfuel4 = "fuel4.png"
xfuel5 = "fuel5.png"
xfuel6 = "fuel6.png"
xfuel7 = "fuel7.png"
xfuel8 = "fuel8.png"
xfuel9 = "fuel9.png"
xfuel10 = "fuel10.png"
xfuel11 = "fuel11.png"
xfuel12 = "fuel12.png"
xfuel13 = "fuel13.png"
xfuel14 = "fuel14.png"
xfuel15 = "fuel15.png"
xfuel16 = "fuel16.png"
#Engine Temperature
xtemp1 = "temp1.png"
xtemp2 = "temp2.png"
xtemp3 = "temp3.png"
xtemp4 = "temp4.png"
xtemp5 = "temp5.png"
xtemp6 = "temp6.png"
xtemp7 = "temp7.png"
xtemp8 = "temp8.png"
xtemp9 = "temp9.png"
xtemp10 = "temp10.png"
xtemp11 = "temp11.png"
xtemp12 = "temp12.png"
xtemp13 = "temp13.png"
xtemp14 = "temp14.png"
xtemp15 = "temp15.png"
xtemp16 = "temp16.png"


'''Variables'''
needleangle = 0
angle = 0
count_speed = 0
previous_fallingedge = 0
previous_risingedge = 0
time_start = 0
time_end = 0
previous_mouse_click = 0


'''GPIO State Variables'''
headlightsstate = 0
highbeamstate = 0
lightbarstate = 0
wiperstate = 0
wiperplusstate = 0
wiperminusstate = 0
hornstate = 0
fuelstate = 12
engine_tempstate = 8

'''Flags'''
kmh = 0  #1 = km/h, 0 = mph
degC = 1 #1 = degrees in celcius, 0 = degress Fahrenheit

'''GPIO Pin Definitions'''
headlightpin = 23
highbeampin = 24
lightbarpin = 25
wiperpin = 21
wiperpluspin = 21
wiperminuspin = 21
hornpin = 12

'''Variables from Arduino'''
leftspeed_arduino = "11"
rightspeed_arduino = "19"
displayed_speed = "11"
airtemperature_arduino = "1"
enginetemperature_arduino = "1"
oil_light_arduino = "0"
alternator_light_arduino = "0"
highbeam_light_arduino = "0"
left_turn_light_arduino = "0"
right_turn_light_arduino = "0"
odometer_arduino = "0"
odometer_error_flag_from_arduino = 1  # 1 = Error, 0 = No error (odometer reading from arduino is correct)

#enginetemp_light_arduino = "1"
#fuel_light_arduino = "1"


'''Initalize Serial Port'''
ser = serial.Serial ("/dev/ttyAMA0", timeout=0.6)
ser.baudrate = 57600

'''Convert images to a format that pygame understands'''
background = pygame.image.load(backgroundfile).convert()

'''Convert alpha means we use the transparency in the pictures that support it'''
mouse = pygame.image.load(crosshairsfile).convert_alpha()
pi = pygame.image.load(pifile).convert_alpha()

needle_orig = pygame.image.load(needlefile).convert_alpha()
needle = needle_orig.copy()
needle_rect = needle_orig.get_rect(center=(400, 240))

#Load pictures for buttons
headlightson = pygame.image.load(headlightson).convert_alpha()
headlightsoff = pygame.image.load(headlightsoff).convert_alpha()
highbeamon = pygame.image.load(highbeamon).convert_alpha()
highbeamoff = pygame.image.load(highbeamoff).convert_alpha()
lightbaron = pygame.image.load(lightbaron).convert_alpha()
lightbaroff = pygame.image.load(lightbaroff).convert_alpha()
wiperon = pygame.image.load(wiperon).convert_alpha()
wiperoff = pygame.image.load(wiperoff).convert_alpha()
wiperpluson = pygame.image.load(wiperpluson).convert_alpha()
wiperplusoff = pygame.image.load(wiperplusoff).convert_alpha()
wiperminuson = pygame.image.load(wiperminuson).convert_alpha()
wiperminusoff = pygame.image.load(wiperminusoff).convert_alpha()
hornon = pygame.image.load(hornon).convert_alpha()
hornoff = pygame.image.load(hornoff).convert_alpha()
musicbutton = pygame.image.load(musicbutton).convert_alpha()
gpsbutton = pygame.image.load(gpsbutton).convert_alpha()
#Load Pictures for Fuel Gauge 
fuel1 = pygame.image.load(xfuel1).convert_alpha()
fuel2 = pygame.image.load(xfuel2).convert_alpha()
fuel3 = pygame.image.load(xfuel3).convert_alpha()
fuel4 = pygame.image.load(xfuel4).convert_alpha()
fuel5 = pygame.image.load(xfuel5).convert_alpha()
fuel6 = pygame.image.load(xfuel6).convert_alpha()
fuel7 = pygame.image.load(xfuel7).convert_alpha()
fuel8 = pygame.image.load(xfuel8).convert_alpha()
fuel9 = pygame.image.load(xfuel9).convert_alpha()
fuel10 = pygame.image.load(xfuel10).convert_alpha()
fuel11 = pygame.image.load(xfuel11).convert_alpha()
fuel12 = pygame.image.load(xfuel12).convert_alpha()
fuel13 = pygame.image.load(xfuel13).convert_alpha()
fuel14 = pygame.image.load(xfuel14).convert_alpha()
fuel15 = pygame.image.load(xfuel15).convert_alpha()
fuel16 = pygame.image.load(xfuel16).convert_alpha()

#Load Pictures for Engine Temperature
temp1 = pygame.image.load(xtemp1).convert_alpha()
temp2 = pygame.image.load(xtemp2).convert_alpha()
temp3 = pygame.image.load(xtemp3).convert_alpha()
temp4 = pygame.image.load(xtemp4).convert_alpha()
temp5 = pygame.image.load(xtemp5).convert_alpha()
temp6 = pygame.image.load(xtemp6).convert_alpha()
temp7 = pygame.image.load(xtemp7).convert_alpha()
temp8 = pygame.image.load(xtemp8).convert_alpha()
temp9 = pygame.image.load(xtemp9).convert_alpha()
temp10 = pygame.image.load(xtemp10).convert_alpha()
temp11 = pygame.image.load(xtemp11).convert_alpha()
temp12 = pygame.image.load(xtemp12).convert_alpha()
temp13 = pygame.image.load(xtemp13).convert_alpha()
temp14 = pygame.image.load(xtemp14).convert_alpha()
temp15 = pygame.image.load(xtemp15).convert_alpha()
temp16 = pygame.image.load(xtemp16).convert_alpha()

#load idiot light, turn signal and traction indicator pictures
oillighton = pygame.image.load(oillighton).convert_alpha()
alternatorlighton = pygame.image.load(alternatorlighton).convert_alpha()
traction_left_lighton = pygame.image.load(traction_left_lighton).convert_alpha()
traction_right_lighton = pygame.image.load(traction_right_lighton).convert_alpha()
turn_left_lighton = pygame.image.load(turn_left_lighton).convert_alpha()
turn_right_lighton = pygame.image.load(turn_right_lighton).convert_alpha()
highbeam_lighton = pygame.image.load(highbeam_lighton).convert_alpha()
enginetemperature_lighton = pygame.image.load(enginetemperature_lighton).convert_alpha()
lowfuel_lighton = pygame.image.load(lowfuel_lighton).convert_alpha()


'''Used to manage how fast the screen updates'''
clock = pygame.time.Clock()

'''before we start the main section, hide the mouse cursor'''
#pygame.mouse.set_visible(False)

'''create variables to hold where the Pi logo is'''
pix = -50
piy = 60

'''How many pixels to move the pi image across the screen'''
pispeed = 3

'''Display Font'''
font_path = "./Myriad Pro Regular.ttf"
font_size = 70   #55 is the original font size for the backgroup image
fontObj = pygame.font.Font(font_path, font_size)
fontObj.set_bold(True)

font_airtemp = pygame.font.Font(font_path, 21)
font_speedunits = pygame.font.Font(font_path, 21)
font_speedunits.set_bold(True)
#myfont = pygame.font.SysFont("monospace", 15)
font_traction = pygame.font.Font(font_path, 21)
font_traction.set_bold(True)


'''Set up GPIO pins'''
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)

'''Text File or Odometer and Tripometer Infroamtion'''
odometer = 0
tripometer = 0
odofile = open("odo.txt", "r+")
odo_from_file_text_line1 = odofile.readline()
response = odo_from_file_text_line1.replace('\n',"")
response2 = response.replace('\r',"")
response3 = response2.replace("odo:","")
odometer = int(response3)

odo_from_file_text_line2 = odofile.readline()
response = odo_from_file_text_line2.replace('\n',"")
response2 = response.replace('\r',"")
response3 = response2.replace("trip:","")
tripometer = int(response3)
odofile.close()

odometer_update_index_time = 0        
odometer_update_index_distance = 0

''' Decalre Functions'''
def rot_center(image, angle):
    """rotate a Surface, maintaining position."""

    loc = rot_image.get_rect().center
    rot_sprite = pygame.transform.rotate(image, angle)
    rot_sprite.get_rect().center = loc
     
    return rot_sprite

    # or return tuple: (Surface, Rect)
        # return rot_sprite, rot_sprite.get_rect()
        
''' Declare Thread'''
'''def callback_fallingedge(channel):
	print "falling edge detected on 17"
	if previous_fallingedge == 0:
		previous_fallingedge = 1'''
	
def leftmousebutton_up(currentmousebutton):
	global previous_mouse_click
	if previous_mouse_click == 1:
		if currentmousebutton == 0:
			previous_mouse_click = currentmousebutton
			return 1;
		previous_mouse_click = currentmousebutton
		return 0
		
def read_from_arduino():
	global leftspeed_arduino
	global rightspeed_arduino
	global airtemperature_arduino
	global ser
	global enginetemperature_arduino
	global oil_light_arduino
	global alternator_light_arduino
	global highbeam_light_arduino
	global left_turn_light_arduino
	global right_turn_light_arduino
	global odometer_arduino
	#ser.write('\n')
	ser.write("testing")
	ser.write('\n')
	
	#Left Speed
	response = ser.readline()
	response2 = response.replace('\n',"")
	leftspeed_arduino = response2.replace('\r',"")
	
	#Right Speed
	response = ser.readline()
	response2 = response.replace('\n',"")
	rightspeed_arduino = response2.replace('\r',"")
	
	#Air Temperature
	response = ser.readline()
	response2 = response.replace('\n',"")
	airtemperature_arduino = response2.replace('\r',"")
	#print leftspeed_arduino
	#response = ser.readline()
	#leftspeed_arduino.rstrip()
	
	#Engine Temperature
	response = ser.readline()
	response2 = response.replace('\n',"")
	enginetemperature_arduino = response2.replace('\r',"")
	
	#Oil Light
	response = ser.readline()
	response2 = response.replace('\n',"")
	oil_light_arduino = response2.replace('\r',"")
	
	#Alternator Light
	response = ser.readline()
	response2 = response.replace('\n',"")
	alternator_light_arduino = response2.replace('\r',"")
	
	#HighBeam Light
	response = ser.readline()
	response2 = response.replace('\n',"")
	highbeam_light_arduino = response2.replace('\r',"")
	
	#Left Turn signal Light
	response = ser.readline()
	response2 = response.replace('\n',"")
	left_turn_light_arduino = response2.replace('\r',"")
	
	#Right turn signal Light
	response = ser.readline()
	response2 = response.replace('\n',"")
	right_turn_light_arduino = response2.replace('\r',"")
	
	#Odometer
	response = ser.readline()
	response2 = response.replace('\n',"")
	odometer_arduino = response2.replace('\r',"")


	return
	
def init_send_arduino_odometer():
	global odometer
	global odometer_error_flag_from_arduino
	index = 0

	#ser.write('\n')
	ser.write("odometer")
	ser.write('\n')
	ser.write(str(odometer))
	ser.write('\n')
	
	#send odometer value to arduino
	response = ser.readline()
	response2 = response.replace('\n',"")
	response3 = response2.replace('\r',"")
	print response3
	while response3 != "odoupdated" and index < 30:
		response = ser.readline()
		response2 = response.replace('\n',"")
		response3 = response2.replace('\r',"")
		index = index + 1
		print response3
	if index > 29:
		print "Error: Could not receive any confimation back form arduino regarding odometer transfer"
	index = 0
	#check to make sure arduino sends the exact same odometer value back, if it doesthen we know arduino has the correct odometer value 
	response = ser.readline()
	response2 = response.replace('\n',"")
	response3 = response2.replace('\r',"")
	print response3
	try:
		while int(response3) != odometer and index < 30:
			response = ser.readline()
			response2 = response.replace('\n',"")
			response3 = response2.replace('\r',"")
			index = index + 1
			print response3
		if index > 29:
			odometer_error_flag_from_arduino = 1
			print "Error: Odometer value sent back from Arduino does not match odometer reading from file."
		else:
			print "Success: Odometer value read back correcly from arduino!!!!"
			odometer_error_flag_from_arduino = 0
	except:
		print "Error: Odometer value read from arduino is not an int"
		odometer_error_flag_from_arduino = 1
		
	print "Done Init"
	return
	
def update_odometer_trip_txtfile():
	global odometer_arduino
	odofile = open("odo.txt", "r+")
	odofile.write("odo:" + str(odometer_arduino + '\n'))
	odofile.write("trip:" + str(tripometer) + '\n')
	odofile.close()
	return

	
'''def callback_risingedge(channel):
	global count_speed
	global previous_risingedge
	global time_start
	global time_end
	print "raising edge detected on 17"
	if previous_risingedge == 0:
		previous_risingedge = 1
		count_speed = 0
		time_start = '%0.7f' % (time.time())
	else:
		#print count_speed
		count_speed = 0
		previous_risingedge = 0
		time_end = '%0.7f' % (time.time())
		print float(time_end) - float(time_start)'''
	
'''Start thread in main '''
#GPIO.add_event_detect(17, GPIO.FALLING, callback=callback_fallingedge)
#GPIO.add_event_detect(17, GPIO.RISING, callback=callback_risingedge)

#pygame.display.toggle_fullscreen
#init GPIO pins
GPIO.output(headlightpin, True)
GPIO.output(highbeampin, True)
GPIO.output(lightbarpin, True)
GPIO.output(hornpin, True)


'''Initilize Odometer: Send Odometer to Arduino to continue incrementing'''
init_send_arduino_odometer() 

while True:
	
	'''The code below quits the program if the X button is pressed'''
	for event in pygame.event.get():
		if event.type == QUIT:
			ser.close()
			pygame.quit()
			sys.exit()
						
	'''Now we have initialized everything, lets start with the main part'''
	
	'''CHech for fullscreen toogle, press "F" to toggle fullscreen and Esc to exit'''
	event1 = pygame.event.poll()
	if event.type == KEYDOWN:
		if event.key == K_ESCAPE:
			odofile.close()
			break    
		elif event.key ==K_f:
			pygame.display.toggle_fullscreen()
			print "Go full screen"
	
	
	'''Receive Variables form Arduino (leftspeed, rightspeed, engine temp, fuel level, add to odo, ambient air temp'''
	read_from_arduino()
	
	'''Draw the background image on the screen'''
	screen.blit(background, (0,0))
	
	'''Code to move the RaspberryPi logo across the screen'''
	
	'''Get the co ordinate for the edges of the screen'''
	screenboundx, screenboundy = screen.get_size()
	
	'''Add pispeed to current value so it moves horizontaly across the screen'''
	pix += pispeed
	
	'''
	if pi x co ordinate is more than or equal to screen bounds then
	add reset it to -50 so it starts half visible on the left side
	'''
	if pix >= screenboundx:
		pix = -50
		
		'''
		Set piy to a random number in the range of the screen bounds
		So it moves across a different Y value each time
		'''
		piy = 50 + random.randrange(screenboundy - 100)
		'''
		Note: piy starts at 50 so it's not drawn half off the screen
		- 100 off so it's not drawn half off the bottom of the screen
		experiment further and you'll see why
		'''
	
	'''draw pi to the screen with co ordinates we worked out'''
	#screen.blit(pi, (pix, piy))
	
	'''Get the X and Y mouse positions to variables called x and y'''
	mousex,mousey = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	'''
	x -= mousewidth  x = x - mousewidth
	Take half of the width of the limage from the mouse co-ordinate
	So the mouse is in the middle of the image
	'''
	#mousex -= mouse.get_width()/2
	#mousey -= mouse.get_height()/2
	
	'''Draw the crosshairs to the screen at the co ordinates we just worked out'''
	#screen.blit(mouse, (mousex,mousey))
	
	'''Limit screen updates to 20 frames per second so we dont use 100% cpu time'''
	clock.tick(30)
	
	
	odometer_update_index_time = odometer_update_index_time + 1
	#Figure out if we need to update odometer text file
	if odometer_update_index_time > 60:
		odometer_update_index_time = 0
		update_odometer_trip_txtfile()
	
	#Find faster speed left or right to display as main speed on interface
	try: 
		int(rightspeed_arduino)
		try: 
			int(leftspeed_arduino)
			if int(leftspeed_arduino) > int(rightspeed_arduino):
				displayed_speed = leftspeed_arduino
			else:
				displayed_speed = rightspeed_arduino
		except:
			print "Error Converting right speed"
	except:
		print "Error Converting left speed"
		
		
	'''Display Speed'''
	if kmh == 0:
		speedtext = fontObj.render(displayed_speed, 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(right = 450, top = 130) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
		
		speedtext = font_speedunits.render("MPH", 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(centerx = 400, top = 190) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect)
	else:
		try:
			speedtext = fontObj.render(str(int(int(displayed_speed)*(1.60934))), 1, (255, 255, 255))
			speedtext_rect = speedtext.get_rect(right = 440, top = 130) #(right = 440, top = 148)
			#speedtext_rect.
			screen.blit(speedtext, speedtext_rect) 
			speedtext = font_speedunits.render("KM/H", 1, (255, 255, 255))
			speedtext_rect = speedtext.get_rect(centerx = 400, top = 190) #(right = 440, top = 148)
			screen.blit(speedtext, speedtext_rect)
		except:
			print "Error displaying main speed"	

		
	'''Display Traction Lights and Speed'''
	try:
		if int(leftspeed_arduino) > 9+int(rightspeed_arduino):
			tractiontext = font_traction.render(leftspeed_arduino, 1, (255, 195, 0))
			tractiontext_rect = tractiontext.get_rect(right = 317, top = 270) #(right = 440, top = 148)
			screen.blit(tractiontext, tractiontext_rect) 
			tractiontext = font_traction.render(rightspeed_arduino, 1, (255, 195, 0))
			tractiontext_rect = tractiontext.get_rect(right = 510, top = 270) #(right = 440, top = 148)
			screen.blit(tractiontext, tractiontext_rect) 
			screen.blit(traction_left_lighton, (0,0))
		elif int(rightspeed_arduino) > 9+int(leftspeed_arduino):
			tractiontext = font_traction.render(leftspeed_arduino, 1, (255, 195, 0))
			tractiontext_rect = tractiontext.get_rect(right = 317, top = 270) #(right = 440, top = 148)
			screen.blit(tractiontext, tractiontext_rect) 
			tractiontext = font_traction.render(rightspeed_arduino, 1, (255, 195, 0))
			tractiontext_rect = tractiontext.get_rect(right = 510, top = 270) #(right = 440, top = 148)
			screen.blit(tractiontext, tractiontext_rect) 
			screen.blit(traction_right_lighton, (0,0))
	except:
		print "Error displaying traction information"
				
		
	'''Display Air Temperature'''
	if degC == 1:
		try:
			speedtext = font_airtemp.render(airtemperature_arduino + unichr(176)+"c", 1, (255, 255, 255))
			speedtext_rect = speedtext.get_rect(right = 165, top = 331) #(right = 440, top = 148)
			#speedtext_rect.
			screen.blit(speedtext, speedtext_rect) 
			#screen.blit(speedtext, (400,148))
		except:
			print "Error displaying air temp celsius"
	else:
		try:
			speedtext = font_airtemp.render(str(int(airtemperature_arduino)*1.8+32)+unichr(176)+"F", 1, (255, 255, 255))
			speedtext_rect = speedtext.get_rect(right = 179, top = 331) #(right = 440, top = 148)
			#speedtext_rect.
			screen.blit(speedtext, speedtext_rect) 
			#screen.blit(speedtext, (400,148))
		except:
			print "Error Converting air temp to Farenheit"
			
	'''Display Odometer (depedning on if Km/h or mph is selected.'''
	print odometer_arduino
	
	'''Display idiot lights/turn signals if needed'''
	if oil_light_arduino == "1":
		screen.blit(oillighton, (0,0))
		
	if alternator_light_arduino == "1":
		screen.blit(alternatorlighton, (0,0))
		
	if highbeam_light_arduino == "1":
		screen.blit(highbeam_lighton, (0,0))
		
	if left_turn_light_arduino == "1":
		screen.blit(turn_left_lighton, (0,0))
		
	if right_turn_light_arduino == "1":
		screen.blit(turn_right_lighton, (0,0))
		
	'''Display Time'''
	speedtext = font_airtemp.render(time.strftime("%I:%M"), 1, (255, 255, 255))
	speedtext_rect = speedtext.get_rect(right = 500, top = 460) #(right = 440, top = 148)
	#speedtext_rect.
	screen.blit(speedtext, speedtext_rect) 
	#screen.blit(speedtext, (400,148))
	
	
	'''Needle rotate'''
	'''Calcualte needle form speed to make it spin!!! just a test lolz'''
	#angle = (float(leftspeed_arduino)/120.0)*(-360.0)
	#print angle
	needle = pygame.transform.rotate(needle_orig, angle)
	needle_rect = needle.get_rect(center=needle_rect.center)
	needleangle = needleangle - 1
	angle = angle - 1
	#print needleangle
	screen.blit(needle, needle_rect)
	
	
	'''GPIO Read/Write'''
	#print GPIO.input(17)
	count_speed = count_speed + 1
	#print '%0.7f' % (time.time())
	#g = float("{0:.7f}".format(time.time()))
	#print g
	


	
	'''Create Head Light Button'''
	#screen.blit(headlightsoff, (0,0))
	#print mousex, mousey
	#leftmousebutton_up(currentmousebutton)
	
	if 104 > mousex > 34 and 80 > mousey > 13 and leftmousebutton_up(click[0]): #head lights
		if headlightsstate == 1:
			headlightsstate = 0
			highbeamstate = 0
			#screen.blit(headlightsoff, (0,0))
		else:
			headlightsstate = 1
			highbeamstate = 0
			
			#screen.blit(headlightson, (0,0))
			
	if  197 > mousex > 127 and 80 > mousey > 13 and leftmousebutton_up(click[0]) and headlightsstate == 1: # high beams
		if highbeamstate == 1:
			highbeamstate = 0
		else:
			highbeamstate = 1
			
	if  727 > mousex > 660 and 80 > mousey > 13 and leftmousebutton_up(click[0]): # wiper
		if wiperstate == 1:
			wiperstate = 0
			wiperplusstate = 0
			wiperminusstate = 0
		else:
			wiperstate = 1
			wiperplusstate = 0
			wiperminusstate = 1
			
	if  659 > mousex > 613 and 80 > mousey > 13 and leftmousebutton_up(click[0]): # wiper plus
		if wiperminusstate == 0 and wiperstate == 1:
			wiperminusstate = 1
			wiperplusstate = 0
		#else:
			#wiperminusstate = 1
			
	if  772 > mousex > 728 and 80 > mousey > 13 and leftmousebutton_up(click[0]): # wiper minus
		if wiperplusstate == 0 and wiperstate == 1:
			wiperplusstate = 1
			wiperminusstate = 0
		#else:
			#wiperplusstate = 1
			
	if  87 > mousex > 7 and 471 > mousey > 406 and leftmousebutton_up(click[0]): # lightbar
		if lightbarstate == 1:
			lightbarstate = 0
		else:
			lightbarstate = 1
			
	if  173 > mousex > 111 and 366 > mousey > 318 and leftmousebutton_up(click[0]): # temp toggle Celcius and fahrenheit
		if degC == 1:
			degC = 0
		else:
			degC = 1
			
	if  475 > mousex > 328 and 211 > mousey > 120 and leftmousebutton_up(click[0]): # Speed toggle KM/H and MPH
		if kmh == 1:
			kmh = 0
		else:
			kmh = 1
			
	if  241 > mousex > 175 and 470 > mousey > 400 and leftmousebutton_up(click[0]): # music button
		#code for switching to music application
		print "Switch to music app"
		ps = subprocess.Popen(['wmctrl','-a','audacious'], stdout=subprocess.PIPE)
		
	if  603 > mousex > 553 and 470 > mousey > 404 and leftmousebutton_up(click[0]): #gps button
		#code for switching to navit
		print "Switich to Navit"
		ps = subprocess.Popen(['wmctrl','-a','Navit'], stdout=subprocess.PIPE)
		
	hornstate = 0	
	if  792 > mousex > 723 and 471 > mousey > 406 and click[0]: # horn
		hornstate = 1
		
	if  718 > mousex > 627 and 244 > mousey > 110 and leftmousebutton_up(click[0]): # Increase Fuel Gauge display
		if fuelstate >= 16 :
			fuelstate = 0
		else:
			fuelstate = fuelstate + 1
			
	if  149 > mousex > 75 and 242 > mousey > 104 and leftmousebutton_up(click[0]): # Increase Engine Temperature Gauge display
		if engine_tempstate >= 16 :
			engine_tempstate = 0
		else:
			engine_tempstate = engine_tempstate + 1
			
	'''if 104 > mousex > 34 and 80 > mousey > 13 and click[0] == 0:
		if previous_mouse_click == 1:
			previous_mouse_click = 0
			if headlightsstate == 1:
				headlightsstate = 0
				screen.blit(headlightsoff, (0,0))
			else:
				headlightsstate = 1
				screen.blit(headlightson, (0,0))
		else:
			previous_mouse_click = 1
			if headlightsstate == 1:
				screen.blit(headlightson, (0,0))
			else:
				screen.blit(headlightsoff, (0,0))
			
	else:
		previous_mouse_click = 0
		if headlightsstate == 1:
			screen.blit(headlightson, (0,0))
		else:
			screen.blit(headlightsoff, (0,0))'''
		
	
		
	#print previous_mouse_click
	previous_mouse_click = 0
	if click[0]:
		previous_mouse_click = 1
		
	'''Finish off by update the full display surface to the screen'''
	'''Update buttons'''
	if headlightsstate == 1:
		screen.blit(headlightson, (0,0))
		GPIO.output(headlightpin, False)
	else:
		screen.blit(headlightsoff, (0,0))
		GPIO.output(headlightpin, True)
		
	if highbeamstate == 1:
		screen.blit(highbeamon, (0,0))
		GPIO.output(highbeampin, False)
	else:
		screen.blit(highbeamoff, (0,0))
		GPIO.output(highbeampin, True)
		
	if wiperstate == 1:
		screen.blit(wiperon, (0,0))
	else:
		screen.blit(wiperoff, (0,0))
		
	if wiperplusstate == 1:
		screen.blit(wiperpluson, (0,0))
	else:
		screen.blit(wiperplusoff, (0,0))
		
	if wiperminusstate == 1:
		screen.blit(wiperminuson, (0,0))
	else:
		screen.blit(wiperminusoff, (0,0))
		
	if lightbarstate == 1:
		screen.blit(lightbaron, (0,0))
		GPIO.output(lightbarpin, False)
	else:
		screen.blit(lightbaroff, (0,0))
		GPIO.output(lightbarpin, True)
		
	if hornstate == 1:
		screen.blit(hornon, (0,0))
		GPIO.output(hornpin, False)
	else:
		screen.blit(hornoff, (0,0))
		GPIO.output(hornpin, True)
		
	if fuelstate == 16:
		screen.blit(fuel16, (0,0))
	elif fuelstate == 15:
		screen.blit(fuel15, (0,0))
	elif fuelstate == 14:
		screen.blit(fuel14, (0,0))
	elif fuelstate == 13:
		screen.blit(fuel13, (0,0))
	elif fuelstate == 12:
		screen.blit(fuel12, (0,0))
	elif fuelstate == 11:
		screen.blit(fuel11, (0,0))
	elif fuelstate == 10:
		screen.blit(fuel10, (0,0))
	elif fuelstate == 9:
		screen.blit(fuel9, (0,0))
	elif fuelstate == 8:
		screen.blit(fuel8, (0,0))
	elif fuelstate == 7:
		screen.blit(fuel7, (0,0))
	elif fuelstate == 6:
		screen.blit(fuel6, (0,0))
	elif fuelstate == 5:
		screen.blit(fuel5, (0,0))
	elif fuelstate == 4:
		screen.blit(fuel4, (0,0))
	elif fuelstate == 3:
		screen.blit(fuel3, (0,0))
	elif fuelstate == 2:
		screen.blit(fuel2, (0,0))
	elif fuelstate == 1:
		screen.blit(fuel1, (0,0))
		
	if engine_tempstate == 16:
		screen.blit(temp16, (0,0))
	elif engine_tempstate == 15:
		screen.blit(temp15, (0,0))
	elif engine_tempstate == 14:
		screen.blit(temp14, (0,0))
	elif engine_tempstate == 13:
		screen.blit(temp13, (0,0))
	elif engine_tempstate == 12:
		screen.blit(temp12, (0,0))
	elif engine_tempstate == 11:
		screen.blit(temp11, (0,0))
	elif engine_tempstate == 10:
		screen.blit(temp10, (0,0))
	elif engine_tempstate == 9:
		screen.blit(temp9, (0,0))
	elif engine_tempstate == 8:
		screen.blit(temp8, (0,0))
	elif engine_tempstate == 7:
		screen.blit(temp7, (0,0))
	elif engine_tempstate == 6:
		screen.blit(temp6, (0,0))
	elif engine_tempstate == 5:
		screen.blit(temp5, (0,0))
	elif engine_tempstate == 4:
		screen.blit(temp4, (0,0))
	elif engine_tempstate == 3:
		screen.blit(temp3, (0,0))
	elif engine_tempstate == 2:
		screen.blit(temp2, (0,0))
	elif engine_tempstate == 1:
		screen.blit(temp1, (0,0))
		
	
	screen.blit(musicbutton, (0,0))	
	screen.blit(gpsbutton, (0,0))
	
	
	if engine_tempstate >= 14:
		screen.blit(enginetemperature_lighton, (0,0))
	if fuelstate <= 2:
		screen.blit(lowfuel_lighton, (0,0))
		
	pygame.display.update()
	
ser.close()
