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
import gps
import threading
from gps_poll import *
from multiprocessing.dummy import Pool
from functools import partial
pool = Pool(processes=1)

#ctypes.CDLL('librt.so', mode=ctypes.RTLD_GLOBAL)
size=(800,480)
GPIO.setmode(GPIO.BCM)

'''import constants used by pygame such as event type = QUIT'''
from pygame.locals import * 
#from wm_ext.appwnd import AppWnd
#from wmctrl import *


'''Dune Buggy Information'''
dune_buggy_owner = "Bernie"
number_points_cvjoint_speedsensor = 16
wheelcircumference = 0.0014379 #miles

'''Sensor Information
	Fuel Level Form arduino is a raw ADC output from 0 to 1024: 630=empty, 210=full
	Alternator Light Voltage Levels: compared at 2.5v. 1.4v = alternator light on, 12v-14v=alternator light off
	Oil Temperature: Resistance chart below and equation. Resistor that I used for the voltage divider is 146.4ohm.
		Note: Arduino does the resistance claulation so the value received form the arduino is the resistance value of the temperature sensor. Pi will need to use the equation to convert resistance to temperature
	Temperature Sensor Resistance chart
		120F	=322.8ohm
		160F	=135ohm
		180F	=105.7
		200F	=76
		220F	=57ohm
		240F	=42ohm
		260F	=31ohm
		280F	=23ohm
		300F	=18.6ohm
		Equation:  Temperature = -63.8*ln("resistance")+479.71'''

path_to_folder = "/home/pi/Desktop/ManxGauged/"

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

'''Init GPS treading poller'''
gpsp = GpsPoller()
try: 
	gpsp.start()
	
except:
	print "GPS thread start error"
	
#Fullscreen toggle, comment back in for car
#pygame.display.toggle_fullscreen()
	
''' Display "Loading Screen" '''
loading_screen = path_to_folder+"manxgaugedboot.png"
loading_screen = pygame.image.load(loading_screen).convert_alpha()
screen.blit(loading_screen, (0,0))
pygame.display.update()

'''Create variables with image names we will use'''
backgroundfile = path_to_folder+"dashbackground.png"
needlefile = path_to_folder+"needle.png"
lightbaron = path_to_folder+"lightbaron.png"
lightbaroff = path_to_folder+"lightbaroff.png"

turn_left_light = path_to_folder+"turn_left_light.png"
turn_right_light = path_to_folder+"turn_right_light.png"

musicbutton = path_to_folder+"musicbutton.png"
gpsbutton = path_to_folder+"gpsbutton.png"
oillighton = path_to_folder+"oil_light.png"
alternatorlighton = path_to_folder+"alternator_light.png"
enginetemperature_lighton = path_to_folder+"enginetemperature_light.png"
lowfuel_lighton = path_to_folder+"lowfuel_lighton.png"


traction_light = path_to_folder+"traction_light.png"

highbeam_lighton = path_to_folder+"highbeam_lighton.png"

tripometer_texton = path_to_folder+"tripometer.png"
shutdown_countdown = path_to_folder+"shutdown_countdown.png"


#Fuel Gauge
xfuel1 = path_to_folder+"fuel1.png"
xfuel2 = path_to_folder+"fuel2.png"
xfuel3 = path_to_folder+"fuel3.png"
xfuel4 = path_to_folder+"fuel4.png"
xfuel5 = path_to_folder+"fuel5.png"
xfuel6 = path_to_folder+"fuel6.png"
xfuel7 = path_to_folder+"fuel7.png"
xfuel8 = path_to_folder+"fuel8.png"
xfuel9 = path_to_folder+"fuel9.png"
xfuel10 = path_to_folder+"fuel10.png"
xfuel11 = path_to_folder+"fuel11.png"
xfuel12 = path_to_folder+"fuel12.png"
xfuel13 = path_to_folder+"fuel13.png"
xfuel14 = path_to_folder+"fuel14.png"
xfuel15 = path_to_folder+"fuel15.png"
xfuel16 = path_to_folder+"fuel16.png"
#Engine Temperature
xtemp1 = path_to_folder+"temp1.png"
xtemp2 = path_to_folder+"temp2.png"
xtemp3 = path_to_folder+"temp3.png"
xtemp4 = path_to_folder+"temp4.png"
xtemp5 = path_to_folder+"temp5.png"
xtemp6 = path_to_folder+"temp6.png"
xtemp7 = path_to_folder+"temp7.png"
xtemp8 = path_to_folder+"temp8.png"
xtemp9 = path_to_folder+"temp9.png"
xtemp10 = path_to_folder+"temp10.png"
xtemp11 = path_to_folder+"temp11.png"
xtemp12 = path_to_folder+"temp12.png"
xtemp13 = path_to_folder+"temp13.png"
xtemp14 = path_to_folder+"temp14.png"
xtemp15 = path_to_folder+"temp15.png"
xtemp16 = path_to_folder+"temp16.png"
#Configuration
clock_12h = path_to_folder+"clock_12h.png"
clock_24h = path_to_folder+"clock_24h.png"
config_bg = path_to_folder+"config_bg.png"
config_bg2 = path_to_folder+"config_bg2.png"
configgear = path_to_folder+"configgear.png"


elevation_units_feet = path_to_folder+"elevation_units_feet.png"
elevation_units_meters = path_to_folder+"elevation_units_meters.png"

speed_sensor_cvpickup = path_to_folder+"speed_sensor_cvpickup.png"
speed_sensor_gps = path_to_folder+"speed_sensor_gps.png"
speed_sensor_gpsandcv = path_to_folder+"speed_sensor_gpsandcv.png"
speed_units_kmh = path_to_folder+"speed_units_kmh.png"
speed_units_mph = path_to_folder+"speed_units_mph.png"
errorlog = path_to_folder+"errorlog.png"
errorlog_page = path_to_folder+"errorlog_page_bg.png"
metering = path_to_folder+"metering.png"
metering_page = path_to_folder+"metering_page_bg.png"

gps_fix_symbol = path_to_folder+"gps_fix_symbol.png"
gps_nofix_symbol = path_to_folder+"gps_nofix_symbol.png"

degree_c_on = path_to_folder+"degree_c_on.png"
degree_c_off = path_to_folder+"degree_c_off.png"
degree_f_on = path_to_folder+"degree_f_on.png"
degree_f_off = path_to_folder+"degree_f_off.png"

on_on = path_to_folder+"on_on.png"
on_off = path_to_folder+"on_off.png"
off_on = path_to_folder+"off_on.png"
off_off = path_to_folder+"off_off.png"


'''Variables'''
needleangle = 0
angle = 0
count_speed = 0
previous_fallingedge = 0
previous_risingedge = 0
time_start = 0
time_end = 0
previous_mouse_click = 0
shutdown_in_progress_skip_read_arduino = 0
error_reading_odo_from_file = 0
boot_time_start = 0
boot_time_end = 0


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
odo_state = 1 # 1 = display odometer, 0 = display tripometer

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
pi_on_arduino = "1"
fuel_level_adc_arduino = "0" #note: this value from pi is a raw dump of the adc from 0 to 1024 (630=emplty, 210=full) 
oil_temperature_resistance_arduino = "1" #noto:this is the raw resistance value see above for resistance to temperature equation
tachometer_arduino = "0"
com_error_ar_pi = 0
com_error_ar_pi_count = 0

odometer_error_flag_from_arduino = 1  # 1 = Error, 0 = No error (odometer reading from arduino is correct)
displayed_odometer_kmh = 0.00
displayed_odometer_mph = 0.00
displayed_tripometer_kmh = 0.00
displayed_tripometer_mph = 0.00
tripometer_index = 0
pi_on_index = 0
shutdown_message = "nothing" 
gps_speed_index = 0
gps_speed_flag = 0

callback_done = 1

#enginetemp_light_arduino = "1"
#fuel_light_arduino = "1"

'''GPS Variables'''
gps_time_pst = "00:00"
gps_time_pst_24h = "24:00"
gps_altitude_feet = "0"
gps_speed_kmh = "0"
gps_climb_feetpermin = "0"



#State Variable
state = "gauge"

#Configuration variables
config_speed_sensor_type = "gpsandcv"
config_engine_temp_units = "f"
config_elevation_units = "feet"
config_elevation_climb = "off"
config_display_traction = "on"
config_clock_units = "12h"
config_daylight_savings = "off"


'''Initalize Serial Port'''
#ser = serial.Serial ("/dev/ttyAMA0", timeout=0.6) #use this line for raspberry pi 2
ser = serial.Serial ("/dev/ttyS0", timeout=0.6) #use this line for raspberry pi 3
ser.baudrate = 57600

'''Convert images to a format that pygame understands'''
background = pygame.image.load(path_to_folder+"dashbackground.png").convert_alpha()


'''Convert alpha means we use the transparency in the pictures that support it'''
needle_orig = pygame.image.load(needlefile).convert_alpha()
needle = needle_orig.copy()
needle_rect = needle_orig.get_rect(center=(400, 240))

#Load pictures for buttons
lightbaron = pygame.image.load(lightbaron).convert_alpha()
lightbaroff = pygame.image.load(lightbaroff).convert_alpha()
musicbutton = pygame.image.load(musicbutton).convert_alpha()
gpsbutton = pygame.image.load(gpsbutton).convert_alpha()
shutdown_countdown = pygame.image.load(shutdown_countdown).convert_alpha()
traction_light = pygame.image.load(traction_light).convert_alpha()
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
turn_left_light = pygame.image.load(turn_left_light).convert_alpha()
turn_right_light = pygame.image.load(turn_right_light).convert_alpha()

highbeam_lighton = pygame.image.load(highbeam_lighton).convert_alpha()
enginetemperature_lighton = pygame.image.load(enginetemperature_lighton).convert_alpha()
lowfuel_lighton = pygame.image.load(lowfuel_lighton).convert_alpha()
tripometer_texton = pygame.image.load(tripometer_texton).convert_alpha()

#load state images
clock_12h = pygame.image.load(clock_12h).convert_alpha()
clock_24h = pygame.image.load(clock_24h).convert_alpha()
config_bg = pygame.image.load(config_bg).convert_alpha()
config_bg2 = pygame.image.load(config_bg2).convert_alpha()
configgear = pygame.image.load(configgear).convert_alpha()

elevation_units_feet = pygame.image.load(elevation_units_feet).convert_alpha()
elevation_units_meters = pygame.image.load(elevation_units_meters).convert_alpha()

speed_sensor_cvpickup = pygame.image.load(speed_sensor_cvpickup).convert_alpha()
speed_sensor_gps = pygame.image.load(speed_sensor_gps).convert_alpha()
speed_sensor_gpsandcv = pygame.image.load(speed_sensor_gpsandcv).convert_alpha()
speed_units_kmh = pygame.image.load(speed_units_kmh).convert_alpha()
speed_units_mph = pygame.image.load(speed_units_mph).convert_alpha()
errorlog = pygame.image.load(errorlog).convert_alpha()
errorlog_page = pygame.image.load(errorlog_page).convert_alpha()
metering = pygame.image.load(metering).convert_alpha()
metering_page = pygame.image.load(metering_page).convert_alpha()

gps_fix_symbol = pygame.image.load(gps_fix_symbol).convert_alpha()
gps_nofix_symbol = pygame.image.load(gps_nofix_symbol).convert_alpha()

degree_c_on = pygame.image.load(degree_c_on).convert_alpha()
degree_c_off = pygame.image.load(degree_c_off).convert_alpha()
degree_f_on = pygame.image.load(degree_f_on).convert_alpha()
degree_f_off = pygame.image.load(degree_f_off).convert_alpha()

on_on = pygame.image.load(on_on).convert_alpha()
on_off = pygame.image.load(on_off).convert_alpha()
off_on = pygame.image.load(off_on).convert_alpha()
off_off = pygame.image.load(off_off).convert_alpha()


'''Used to manage how fast the screen updates'''
clock = pygame.time.Clock()

'''before we start the main section, hide the mouse cursor'''
#pygame.mouse.set_visible(False)


'''Display Font'''
font_path = path_to_folder+"Myriad Pro Regular.ttf"
font_size = 70   #55 is the original font size for the backgroup image
fontObj = pygame.font.Font(font_path, font_size)
fontObj.set_bold(True)

font_airtemp = pygame.font.Font(font_path, 21)
font_speedunits = pygame.font.Font(font_path, 21)
font_speedunits.set_bold(True)
#myfont = pygame.font.SysFont("monospace", 15)
font_traction = pygame.font.Font(font_path, 21)
font_traction.set_bold(True)

font_metering_title = pygame.font.Font(font_path, 25)
font_metering_title.set_bold(True)

font_tripreset = pygame.font.Font(font_path, 50)
font_tripreset.set_bold(True)

font_shutdown_countdown = pygame.font.Font(font_path, 95)
font_shutdown_countdown.set_bold(True)



'''Set up GPIO pins'''
#GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)

'''Text File or Odometer and Tripometer Infroamtion'''
odometer = 0
tripometer = 0
odofile = open(path_to_folder+"odo.txt", "r")
odo_from_file_text_line1 = odofile.readline()
response = odo_from_file_text_line1.replace('\n',"")
response2 = response.replace('\r',"")
response3 = response2.replace("odo:","")
try:
	odometer = int(response3)
except:
	print "Error: ODO read from file is not an int"
	error_reading_odo_from_file = 1
odometer_arduino = odometer

odo_from_file_text_line2 = odofile.readline()
response = odo_from_file_text_line2.replace('\n',"")
response2 = response.replace('\r',"")
response3 = response2.replace("trip:","")
try:
	tripometer = int(response3)
except:
	print "Error: Trip read from file is not an int"
	error_reading_odo_from_file = 1
odofile.close()

odometer_resend_2arduino_index = 0
odometer_error_out_index = 0
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
        
''' Declare multiprocessing functions so Pi can Read from Arduino without slowing the whole program'''
def async_function(name):
	read_from_arduino()
	
	return
    
def callback_function(name, age):
	
	
	#do the loop again to read from arduino
	new_callback_function = partial(callback_function, age=6)
	pool.apply_async(
		async_function,
		args=["start"],
		callback=new_callback_function
	)
	
	
	
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
	global pi_on_arduino
	global fuel_level_adc_arduino
	global oil_temperature_resistance_arduino
	global tachometer_arduino
	global com_error_ar_pi
	global com_error_ar_pi_count
	global shutdown_in_progress_skip_read_arduino
	
	if shutdown_in_progress_skip_read_arduino == 0:
		#ser.write('\n')
		ser.write("testing")
		ser.write('\n')
		
		#"datastart" tag
		response = ser.readline()
		response2 = response.replace('\n',"")
		datastart_tag = response2.replace('\r',"")
		
		#Check datastart tag
		if datastart_tag != "datastart":
			ser.flushInput()
			com_error_ar_pi_count = com_error_ar_pi_count + 1
			return
		
		#Left Speed
		response = ser.readline()
		response2 = response.replace('\n',"")
		leftspeed_arduino_temp = response2.replace('\r',"")
		
		#Right Speed
		response = ser.readline()
		response2 = response.replace('\n',"")
		rightspeed_arduino_temp = response2.replace('\r',"")
		
		#Air Temperature
		response = ser.readline()
		response2 = response.replace('\n',"")
		airtemperature_arduino_temp = response2.replace('\r',"")
		#print leftspeed_arduino
		#response = ser.readline()
		#leftspeed_arduino.rstrip()
		
		#Engine Temperature
		response = ser.readline()
		response2 = response.replace('\n',"")
		enginetemperature_arduino_temp = response2.replace('\r',"")
		
		#Oil Light
		response = ser.readline()
		response2 = response.replace('\n',"")
		oil_light_arduino_temp = response2.replace('\r',"")
		
		
		#Alternator Light
		response = ser.readline()
		response2 = response.replace('\n',"")
		alternator_light_arduino_temp = response2.replace('\r',"")
		
		
		#HighBeam Light
		response = ser.readline()
		response2 = response.replace('\n',"")
		highbeam_light_arduino_temp = response2.replace('\r',"")
		
		#Left Turn signal Light
		response = ser.readline()
		response2 = response.replace('\n',"")
		left_turn_light_arduino_temp = response2.replace('\r',"")
		
		#Right turn signal Light
		response = ser.readline()
		response2 = response.replace('\n',"")
		right_turn_light_arduino_temp = response2.replace('\r',"")
		
		#Odometer
		response = ser.readline()
		response2 = response.replace('\n',"")
		odometer_arduino_temp = response2.replace('\r',"")
		
		#Pi On
		response = ser.readline()
		response2 = response.replace('\n',"")
		pi_on_arduino_temp = response2.replace('\r',"")
		
		
		#Fuel Level
		response = ser.readline()
		response2 = response.replace('\n',"")
		fuel_level_adc_arduino_temp = response2.replace('\r',"")
		
		
		#Oil Temperature
		response = ser.readline()
		response2 = response.replace('\n',"")
		oil_temperature_resistance_arduino_temp = response2.replace('\r',"")

		#Tachometer
		response = ser.readline()
		response2 = response.replace('\n',"")
		tachometer_arduino_temp = response2.replace('\r',"")
		
		#"dataend" tag
		response = ser.readline()
		response2 = response.replace('\n',"")
		dataend_tag = response2.replace('\r',"")
		
		#Check datastart tag
		if dataend_tag != "dataend":
			ser.flushInput()
			com_error_ar_pi_count = com_error_ar_pi_count + 1
			return
			
		
		#If we make it to this part we need to update the real variables from the temporary veriables.
		#If we made it here. The data was read from the arduino correctly. Turns out im having anissue somehow
		com_error_ar_pi = 0
		com_error_ar_pi_count = 0
		leftspeed_arduino = leftspeed_arduino_temp
		rightspeed_arduino = rightspeed_arduino_temp
		airtemperature_arduino = airtemperature_arduino_temp
		enginetemperature_arduino = enginetemperature_arduino_temp
		oil_light_arduino = oil_light_arduino_temp
		alternator_light_arduino = alternator_light_arduino_temp
		highbeam_light_arduino = highbeam_light_arduino_temp
		left_turn_light_arduino = left_turn_light_arduino_temp
		right_turn_light_arduino = right_turn_light_arduino_temp
		pi_on_arduino = pi_on_arduino_temp
		fuel_level_adc_arduino = fuel_level_adc_arduino_temp
		oil_temperature_resistance_arduino = oil_temperature_resistance_arduino_temp
		tachometer_arduino = tachometer_arduino_temp
		#check if odometer from arduino is lower then displayed odo. If so, arduino odo is wrong and odo needs to be resynced
		# first change odometer_arduino_temp to an int
		try:
			odometer_arduino_temp = int(odometer_arduino_temp)
			if odometer_arduino > odometer_arduino_temp:
				print "Odometer read from arduino is less then displayed odometer. Resyncing..."
				init_send_arduino_odometer()
			else:
				odometer_arduino = odometer_arduino_temp
		except:
			print "Error: ODO read from Arduino was not a int"
		
	else:
		
		time.sleep(2)

	return
	
def init_send_arduino_odometer():
	global odometer
	global odometer_error_flag_from_arduino
	index = 0
	
	ser.flushInput()
	
	#ser.write('\n')
	ser.write("odometer")
	ser.write('\n')
	ser.write(str(odometer))
	ser.write('\n')
	
	#send odometer value to arduino
	response = ser.readline()
	response2 = response.replace('\n',"")
	response3 = response2.replace('\r',"")
	#print response3
	while response3 != "odoupdated" and index < 30:
		response = ser.readline()
		response2 = response.replace('\n',"")
		response3 = response2.replace('\r',"")
		index = index + 1
		#print response3
	if index > 29:
		print "Error: Could not receive any confimation back form arduino regarding odometer transfer"
	index = 0
	#check to make sure arduino sends the exact same odometer value back, if it doesthen we know arduino has the correct odometer value 
	response = ser.readline()
	response2 = response.replace('\n',"")
	response3 = response2.replace('\r',"")
	#print response3
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
	global tripometer
	global odometer_error_flag_from_arduino
	global error_reading_odo_from_file
	global odofile
	global path_to_folder
	
	if odometer_error_flag_from_arduino == 0 and error_reading_odo_from_file == 0:
		odofile = open(path_to_folder+"odo.txt", "w+")
		odofile.write("odo:" + str(odometer_arduino) + '\n')
		odofile.write("trip:" + str(tripometer) + '\n')
		odofile.close()
		
	return

#Function for saving configuratio data to text file
def save_configuration_txtfile():
	global config_speed_sensor_type
	global kmh
	global degC
	global config_engine_temp_units
	global config_elevation_units
	global config_elevation_climb
	global config_display_traction
	global config_clock_units
	global wheelcircumference
	global number_points_cvjoint_speedsensor
	global dune_buggy_owner

	configfile = open(path_to_folder+"config.txt", "w+")
	configfile.write("speed_sensor:" + str(config_speed_sensor_type + '\n'))
	configfile.write("speed_units(kmh=1):" + str(kmh) + str('\n'))
	configfile.write("air_temp_units(c=1):" + str(degC) + '\n')
	configfile.write("engine_temp_units:" + str(config_engine_temp_units + '\n'))
	configfile.write("elevation_units:" + str(config_elevation_units + '\n'))
	configfile.write("elevation_climb:" + str(config_elevation_climb + '\n'))
	configfile.write("display_traction:" + str(config_display_traction + '\n'))
	configfile.write("clock_units:" + str(config_clock_units + '\n'))
	configfile.write("config_daylight_savings:" + str(config_daylight_savings + '\n'))
	configfile.write("wheel_circumference(miles):" + str(wheelcircumference) + str('\n'))
	configfile.write("number_points_cvjoint_speedsensor:" + str(number_points_cvjoint_speedsensor) + str('\n'))
	configfile.write("dune_buggy_owner:" + str(dune_buggy_owner) + str('\n'))
	#configfile.write("trip:" + str(tripometer) + '\n')
	#kmh = 0  #1 = km/h, 0 = mph
	#degC = 1
	configfile.close()
	return

#Function for reading configuratio data from text file
def read_configuration_txtfile():
	global config_speed_sensor_type
	global kmh
	global degC
	global config_engine_temp_units
	global config_elevation_units
	global config_elevation_climb
	global config_display_traction
	global config_clock_units
	global config_daylight_savings
	global wheelcircumference
	global number_points_cvjoint_speedsensor
	global dune_buggy_owner
	
	try:
		configfile = open(path_to_folder+"config.txt", "r")
		
		config_from_file_text_line1 = configfile.readline()             #line 1 -> speed_sensor
		response = config_from_file_text_line1.replace('\n',"")
		response2 = response.replace('\r',"")
		response3 = response2.replace("speed_sensor:","")
		config_speed_sensor_type = response3
		
		config_from_file_text_line1 = configfile.readline()             #line 2 -> speed_units(kmh=1)
		response = config_from_file_text_line1.replace('\n',"")
		response2 = response.replace('\r',"")
		response3 = response2.replace("speed_units(kmh=1):","")
		kmh = int(response3)
		
		config_from_file_text_line1 = configfile.readline()             #line 3 -> air_temp_units(c=1)
		response = config_from_file_text_line1.replace('\n',"")
		response2 = response.replace('\r',"")
		response3 = response2.replace("air_temp_units(c=1):","")
		degC = int(response3)
		
		config_from_file_text_line1 = configfile.readline()             #line 4 -> engine_temp_units:
		response = config_from_file_text_line1.replace('\n',"")
		response2 = response.replace('\r',"")
		response3 = response2.replace("engine_temp_units:","")
		config_engine_temp_units = response3
		
		config_from_file_text_line1 = configfile.readline()             #line 5 -> elevation_units:
		response = config_from_file_text_line1.replace('\n',"")
		response2 = response.replace('\r',"")
		response3 = response2.replace("elevation_units:","")
		config_elevation_units = response3
		
		config_from_file_text_line1 = configfile.readline()             #line 6 -> elevation_climb:
		response = config_from_file_text_line1.replace('\n',"")
		response2 = response.replace('\r',"")
		response3 = response2.replace("elevation_climb:","")
		config_elevation_climb = response3
		
		config_from_file_text_line1 = configfile.readline()             #line 7 -> display_traction:
		response = config_from_file_text_line1.replace('\n',"")
		response2 = response.replace('\r',"")
		response3 = response2.replace("display_traction:","")
		config_display_traction = response3
		
		config_from_file_text_line1 = configfile.readline()             #line 8 -> clock_units:
		response = config_from_file_text_line1.replace('\n',"")
		response2 = response.replace('\r',"")
		response3 = response2.replace("clock_units:","")
		config_clock_units = response3
		
		config_from_file_text_line1 = configfile.readline()             #line 9 -> config_daylight_savings:
		response = config_from_file_text_line1.replace('\n',"")
		response2 = response.replace('\r',"")
		response3 = response2.replace("config_daylight_savings:","")
		config_daylight_savings = response3
		
		config_from_file_text_line1 = configfile.readline()             #line 10 -> wheel_circumference(miles):
		response = config_from_file_text_line1.replace('\n',"")
		response2 = response.replace('\r',"")
		response3 = response2.replace("wheel_circumference(miles):","")
		wheelcircumference = float(response3)
		
		config_from_file_text_line1 = configfile.readline()             #line 11 -> number_points_cvjoint_speedsensor:
		response = config_from_file_text_line1.replace('\n',"")
		response2 = response.replace('\r',"")
		response3 = response2.replace("number_points_cvjoint_speedsensor:","")
		number_points_cvjoint_speedsensor = int(response3)
		
		config_from_file_text_line1 = configfile.readline()             #line 12 -> dune_buggy_owner:
		response = config_from_file_text_line1.replace('\n',"")
		response2 = response.replace('\r',"")
		response3 = response2.replace("dune_buggy_owner:","")
		dune_buggy_owner = response3
		
		configfile.close()
	except:
		print "Error Reading Config file"
	return
	
def confirm_shutdown():
	global shutdown_message
	#ser.write('\n')
	ser.write("shutdown")
	ser.write('\n')
	
	#send odometer value to arduino
	response = ser.readline()
	response2 = response.replace('\n',"")
	response3 = response2.replace('\r',"")
	
	shutdown_message = response3
	

#pygame.display.toggle_fullscreen
#init GPIO pins
GPIO.output(headlightpin, True)
GPIO.output(highbeampin, True)
GPIO.output(lightbarpin, True)
GPIO.output(hornpin, True)


'''Read Config File'''
read_configuration_txtfile()

'''Initilize Odometer: Send Odometer to Arduino to continue incrementing'''
init_send_arduino_odometer()

'''Start the first multiprocessing for reading from arduino'''
new_callback_function = partial(callback_function, age=6)
pool.apply_async(
	async_function,
	args=["start"],
	callback=new_callback_function
)




while True:
	
	'''The code below quits the program if the X button is pressed'''
	for event in pygame.event.get():
		if event.type == QUIT:
			ser.close()
			pygame.quit()
			sys.exit()
						
	'''Now we have initialized everything, lets start with the main part'''
	
	'''Check for fullscreen toogle, press "F" to toggle fullscreen and Esc to exit'''
	event1 = pygame.event.poll()
	if event.type == KEYDOWN:
		if event.key == K_ESCAPE:
			
			break    
		elif event.key ==K_f:
			pygame.display.toggle_fullscreen()
			print "Go full screen"
		elif event.key ==K_g:
			pygame.display.toggle_fullscreen()
			print "Go full screen"
		elif event.key ==K_q:
			print "Shuting Down"
			os.system('shutdown now -h')
			
	
	'''Check Ardunio Communication error and display message to user if there is an error'''
	if com_error_ar_pi_count > 5:
		com_error_ar_pi = 1
		
	if com_error_ar_pi == 1:
		print "AR Com Error"

	'''Get GPS Data from Thread'''
	
	try:
		'''Units for each variable:
		speed = m/s
		alt = m
		climb = m/s 
		'''
	
		gps_report = gpsp.get_current_value()
		#gps_speed_kmh = int(((float(gps_report['speed'])/1000.0)*60.0)) old one.
		gps_speed_kmh = int(((float(gps_report['speed'])*2.217*1.60934)))
		gps_altitude_feet = gps_report['alt'] * 3.28084 # 1 meter = 3.28084 feet
	
		gps_climb_feetpermin = gps_report['climb']*60 * 3.28084 # 1 meter = 3.28084 feet
		temp_time = str(gps_report['time'])
		temp_time2 = temp_time.partition('T')[2].split('.', 1)[0]
		time0 = temp_time2.split(':', 3)[0]
		time1 = temp_time2.split(':', 3)[1]
		time2 = temp_time2.split(':', 3)[2]
		time_hour = int(time0)+17 #fix Vancouver Time
		if config_daylight_savings == "on":
			time_hour = time_hour -1
		#fix to 24 hour
		if time_hour > 23: 
			time_hour = time_hour - 24
			gps_time_pst_24h = str(time_hour) + ":" +time1
		#fix to 12 hour
		if time_hour > 12:
			time_hour = time_hour - 12
			pm_or_am = "PM"
		else:
			pm_or_am = "AM"
			
		pst_time = str(time_hour) + ":" + time1 + pm_or_am
		gps_time_pst = pst_time
		gps_speed_flag = 1 #1 means use gps speed
		gps_speed_index = 0
	except:
		#print "Error: Getting GPS Data"
		if gps_speed_index < 500:
			gps_speed_index = gps_speed_index + 1
		
	
	'''Get the X and Y mouse positions to variables called x and y'''
	mousex,mousey = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	
	'''Limit screen updates to 20 frames per second so we dont use 100% cpu time'''
	clock.tick(30)
	
	if odometer_error_flag_from_arduino == 1 and odometer_error_out_index < 3:
		if odometer_resend_2arduino_index > 40:
			odometer_resend_2arduino_index = 0
			init_send_arduino_odometer()
			odometer_error_out_index = odometer_error_out_index + 1
		else:
			odometer_resend_2arduino_index = odometer_resend_2arduino_index + 1
		 
	
	if pi_on_arduino == "0":
		pi_on_index = pi_on_index +1
		print pi_on_index
	else:
		pi_on_index = 0
		
	if pi_on_index > 40:
		
		shutdown_in_progress_skip_read_arduino = 1
		#Clear Serial Data first
		ser.flushInput()
		print "Waiting for confimation of shutdown from pi"
		print odometer_arduino
		print tripometer
		update_odometer_trip_txtfile()
		pi_on_index = 0
		while(1):
			confirm_shutdown()
			if shutdown_message == "confirm":
				time.sleep(1)
				print "Shuting down..."
				os.system('shutdown now -h')
			elif shutdown_message == "stopsd":
				shutdown_in_progress_skip_read_arduino = 0
				break
			else:
				print "Error incorrect shutdown confirmation, trying agian..."

	
	odometer_update_index_time = odometer_update_index_time + 1
	#Figure out if we need to update odometer text file
	if odometer_update_index_time > 600:
		odometer_update_index_time = 0
		update_odometer_trip_txtfile()
		print "updating Odometer Value in  Txt File"
	
	
	'''#Find faster speed left or right to display as main speed on interface
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
		print "Error Converting left speed"'''
	
	
	'''Display Speed based on config ---------------------------------------------------------------'''
	if config_speed_sensor_type == "cv":
		#Always display right wheel since its better unless it is <5mph.
		try: 
			int(rightspeed_arduino)
			try: 
				int(leftspeed_arduino)
				if 2 > int(rightspeed_arduino):
					displayed_speed = leftspeed_arduino
				else:
					displayed_speed = rightspeed_arduino
			except:
				print "Error Converting right speed"
		except:
			print "Error Converting left speed"
		
	#Display GPS speed if there is a gps lock and the speed is faster then 5km/h. if not display CV Speed
	if config_speed_sensor_type == "gpsandcv":
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
		#Display GPS speed if there is a gps lock and the speed is faster then 5km/h
		if gps_speed_index > 100:
			gps_speed_flag = 0
		if gps_speed_flag == 1:
			displayed_speed = str(gps_speed_kmh)
		
	
	if config_speed_sensor_type == "gps":
		if gps_speed_flag == 1: #If GPS fix
			displayed_speed = str(gps_speed_kmh)
		else:
			displayed_speed = "GPS!"
						
	#print mousex, mousey
	
		
	#------------------------------------------------------------------ Display State = Gauge-------------------------------------- 
	if state == "gauge":
		'''Draw the Manx Gauged Background'''
		screen.blit(background, (0,0))	
		
		if com_error_ar_pi == 1:
			speedtext = font_tripreset.render("Com Error", 1, (255, 255, 255))
			speedtext_rect = speedtext.get_rect(right = 270, top = 4) #(right = 440, top = 148)
			screen.blit(speedtext, speedtext_rect) 
		
		'''Display Speed'''
		#Chnage text 
		if displayed_speed == "GPS!": #gps no fix
			speedtext = fontObj.render(str(displayed_speed_ones), 1, (255, 255, 255))
			speedtext_rect = speedtext.get_rect(right = 490, top = 130) #(right = 450, top = 130)
			screen.blit(speedtext, speedtext_rect) 
		else:
			if kmh == 0:
				speedtext = font_speedunits.render("MPH", 1, (255, 255, 255))
				speedtext_rect = speedtext.get_rect(centerx = 400, top = 190) #(right = 400, top = 190)
				screen.blit(speedtext, speedtext_rect)
				
			else:
				speedtext = font_speedunits.render("KM/H", 1, (255, 255, 255))
				speedtext_rect = speedtext.get_rect(centerx = 400, top = 190) #(right = 400, top = 190)
				screen.blit(speedtext, speedtext_rect)
				try:
					displayed_speed = (int(int(displayed_speed)*(1.60934)))
				except:
					print "Error displaying main speed"	
			
			displayed_speed_ones = int(displayed_speed)%10
			displayed_speed_tens = (int(displayed_speed)/10)%10
			displayed_speed_hundreds = (int(displayed_speed)/100)%10	
				
			speed_length = len(str(displayed_speed))
			if speed_length == 1:
				speedtext = fontObj.render(str(displayed_speed_ones), 1, (255, 255, 255))
				speedtext_rect = speedtext.get_rect(right = 430, top = 130) #(right = 450, top = 130)
				screen.blit(speedtext, speedtext_rect) 
			if speed_length == 2:
				speedtext = fontObj.render(str(displayed_speed_ones), 1, (255, 255, 255))
				speedtext_rect = speedtext.get_rect(right = 451, top = 130) #(right = 450, top = 130)
				screen.blit(speedtext, speedtext_rect) 
				speedtext = fontObj.render(str(displayed_speed_tens), 1, (255, 255, 255))
				speedtext_rect = speedtext.get_rect(right = 409, top = 130) #(right = 450, top = 130)
				screen.blit(speedtext, speedtext_rect) 
			if speed_length == 3:
				speedtext = fontObj.render(str(displayed_speed_ones), 1, (255, 255, 255))
				speedtext_rect = speedtext.get_rect(right = 465, top = 130) #(right = 450, top = 130)
				screen.blit(speedtext, speedtext_rect) 
				speedtext = fontObj.render(str(displayed_speed_tens), 1, (255, 255, 255))
				speedtext_rect = speedtext.get_rect(right = 423, top = 130) #(right = 450, top = 130)
				screen.blit(speedtext, speedtext_rect) 
				speedtext = fontObj.render(str(displayed_speed_hundreds), 1, (255, 255, 255))
				speedtext_rect = speedtext.get_rect(right = 388, top = 130) #(right = 450, top = 130)
				screen.blit(speedtext, speedtext_rect)
			
		
	
			
		
			
		'''Display Traction Lights and Speed'''
		if config_display_traction == "on":
			try:
				
				if int(leftspeed_arduino) > 9+int(rightspeed_arduino):
					tractiontext = font_traction.render(leftspeed_arduino, 1, (255, 195, 0))
					tractiontext_rect = tractiontext.get_rect(right = 317, top = 270) #(right = 440, top = 148)
					screen.blit(tractiontext, tractiontext_rect) 
					tractiontext = font_traction.render(rightspeed_arduino, 1, (255, 195, 0))
					tractiontext_rect = tractiontext.get_rect(right = 510, top = 270) #(right = 440, top = 148)
					screen.blit(tractiontext, tractiontext_rect) 
					screen.blit(traction_light, (287,231))
				elif int(rightspeed_arduino) > 9+int(leftspeed_arduino):
					tractiontext = font_traction.render(leftspeed_arduino, 1, (255, 195, 0))
					tractiontext_rect = tractiontext.get_rect(right = 317, top = 270) #(right = 440, top = 148)
					screen.blit(tractiontext, tractiontext_rect) 
					tractiontext = font_traction.render(rightspeed_arduino, 1, (255, 195, 0))
					tractiontext_rect = tractiontext.get_rect(right = 510, top = 270) #(right = 440, top = 148)
					screen.blit(tractiontext, tractiontext_rect) 
					screen.blit(traction_light, (480,231))	
			except:
				print "Error displaying traction information"
					
		'''Display GPS Fix Status Symbol'''
		if gps_speed_flag == 1:
			screen.blit(gps_fix_symbol, (460,195))	
		else:
			screen.blit(gps_nofix_symbol, (460,195))	
			
		'''Display Air Temperature'''
		if degC == 1:
			try:
				speedtext = font_airtemp.render(airtemperature_arduino + unichr(176)+"C", 1, (255, 255, 255))
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
				
		'''Display Odometer (depending on if Km/h or mph is selected.'''
		try:
			displayed_odometer_mph = round((float(odometer_arduino)/number_points_cvjoint_speedsensor)*wheelcircumference,1)
			displayed_odometer_kmh = round((float(odometer_arduino)/number_points_cvjoint_speedsensor)*wheelcircumference*(1.60934),1)
			
			displayed_tripometer_mph = round(((float(odometer_arduino)-tripometer)/number_points_cvjoint_speedsensor)*wheelcircumference,1)
			displayed_tripometer_kmh = round(((float(odometer_arduino)-tripometer)/number_points_cvjoint_speedsensor)*wheelcircumference*(1.60934),1)
		
		except:
			print "Error converting odometer string from arduino to float"
		if odometer_error_flag_from_arduino == 0:
			if odo_state == 1:
				if kmh == 0:
					#odometer displayed in miles
					speedtext = font_airtemp.render(str(displayed_odometer_mph), 1, (255, 255, 255))
					speedtext_rect = speedtext.get_rect(right = 680, top = 331) #(right = 440, top = 148)
					screen.blit(speedtext, speedtext_rect) 
					speedtext = font_airtemp.render("miles", 1, (255, 255, 255))
					speedtext_rect = speedtext.get_rect(right = 675, top = 349) #(right = 440, top = 148)
					screen.blit(speedtext, speedtext_rect) 
				else:
					#odometer displayed in km/h
					speedtext = font_airtemp.render(str(displayed_odometer_kmh), 1, (255, 255, 255))
					speedtext_rect = speedtext.get_rect(right = 680, top = 331) #(right = 440, top = 148)
					screen.blit(speedtext, speedtext_rect) 
					speedtext = font_airtemp.render("km", 1, (255, 255, 255))
					speedtext_rect = speedtext.get_rect(right = 675, top = 349) #(right = 440, top = 148)
					screen.blit(speedtext, speedtext_rect) 
			else:
				if kmh == 0:
					#tripometer displayed in miles
					speedtext = font_airtemp.render(str(displayed_tripometer_mph), 1, (255, 255, 255))
					speedtext_rect = speedtext.get_rect(right = 680, top = 331) #(right = 440, top = 148)
					screen.blit(speedtext, speedtext_rect) 
					speedtext = font_airtemp.render("miles", 1, (255, 255, 255))
					speedtext_rect = speedtext.get_rect(right = 675, top = 349) #(right = 440, top = 148)
					screen.blit(speedtext, speedtext_rect) 
				else:
					#tripometer displayed in km/h
					speedtext = font_airtemp.render(str(displayed_tripometer_kmh), 1, (255, 255, 255))
					speedtext_rect = speedtext.get_rect(right = 680, top = 331) #(right = 440, top = 148)
					screen.blit(speedtext, speedtext_rect) 
					speedtext = font_airtemp.render("km", 1, (255, 255, 255))
					speedtext_rect = speedtext.get_rect(right = 675, top = 349) #(right = 440, top = 148)
					screen.blit(speedtext, speedtext_rect) 
		else:
			speedtext = font_airtemp.render("Odo Error", 1, (255, 255, 255))
			speedtext_rect = speedtext.get_rect(right = 680, top = 331) #(right = 440, top = 148)
			screen.blit(speedtext, speedtext_rect) 
			speedtext = font_airtemp.render("Touch Here", 1, (255, 255, 255))
			speedtext_rect = speedtext.get_rect(right = 675, top = 349) #(right = 440, top = 148)
			screen.blit(speedtext, speedtext_rect) 
		
		'''Display idiot lights/turn signals if needed'''
		if oil_light_arduino == "1":
			screen.blit(oillighton, (311,324))
			
		if alternator_light_arduino == "1":
			screen.blit(alternatorlighton, (445,323)) #done
			
		if highbeam_light_arduino == "1":
			screen.blit(highbeam_lighton, (380,323)) #done
			
		if left_turn_light_arduino == "1":
			screen.blit(turn_left_light, (270,198))
			
			
		if right_turn_light_arduino == "1":
			screen.blit(turn_right_light, (495,198))
			
		
		screen.blit(configgear, (750,430))
			
		'''Display Time'''
		if config_clock_units == "12h":
			#speedtext = font_airtemp.render(time.strftime("%I:%M"), 1, (255, 255, 255))
			speedtext = font_airtemp.render(gps_time_pst, 1, (255, 255, 255))
		if config_clock_units == "24h":
			speedtext = font_airtemp.render(gps_time_pst_24h, 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(right = 500, top = 460) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 

		'''Display Altitude'''
		try:
			if config_elevation_units == "feet":
				speedtext = font_airtemp.render(str(int(gps_altitude_feet))+"ft", 1, (255, 255, 255))
			if config_elevation_units == "meters":
				speedtext = font_airtemp.render(str(int(int(gps_altitude_feet)/3.28084))+"m", 1, (255, 255, 255))
			speedtext_rect = speedtext.get_rect(right = 360, top = 460) #(right = 440, top = 148)
			screen.blit(speedtext, speedtext_rect) 	
		except:
			print "Error Altitude Display"
			
		'''Display Altitude Climb'''
		try:
			if config_elevation_climb == "on":
				if config_elevation_units == "feet":
					speedtext = font_airtemp.render(str(int(gps_climb_feetpermin))+"ft/min", 1, (255, 255, 255))
				if config_elevation_units == "meters":
					speedtext = font_airtemp.render(str(int(int(gps_climb_feetpermin)/3.28084))+"m/min", 1, (255, 255, 255))
				speedtext_rect = speedtext.get_rect(right = 710, top = 460) #(right = 440, top = 148)
				screen.blit(speedtext, speedtext_rect) 	
		except:
			print "Error Altitude Display"
			
		'''Display Tach (Needle rotate)'''
		'''Calcualte needle form speed to make it spin!!! just a test lolz'''
		'''So the tach circle is not evenly spaced so we need some weird
		ratios to get the tach to display correcly. '''
		try:
			tachometer_arduino = int(tachometer_arduino)
		except:
			print "Cant change tachometer to int"
		if tachometer_arduino < 4000:
			angle = ((float(tachometer_arduino)/9000)*(-360.0))*0.87
		else:
			angle = 0 # this is so if the tach gets higher then 9000 it will just stay at 0
			if 3999 < tachometer_arduino < 5000:
				startingangle = -139
				endingangle = -180
				anglerange = 41
				angle = (-anglerange)*((float(tachometer_arduino) - 4000.0)/1000.0)+startingangle
				#angle = (((float(tachometer_arduino)/9000)*(360.0))*0.886)*(-1) #0.897
			if 4999 < tachometer_arduino < 6000:
				startingangle = -180
				endingangle = -226
				anglerange = 46
				angle = (-anglerange)*((float(tachometer_arduino) - 5000.0)/1000.0)+startingangle
			if 5999 < tachometer_arduino < 7000:
				startingangle = -226
				endingangle = -279
				anglerange = 53
				angle = (-anglerange)*((float(tachometer_arduino) - 6000.0)/1000.0)+startingangle
			if 6999 < tachometer_arduino < 8000:
				startingangle = -279
				endingangle = -320
				anglerange = 41
				angle = (-anglerange)*((float(tachometer_arduino) - 7000.0)/1000.0)+startingangle
			if 7999 < tachometer_arduino < 9000:
				startingangle = -320
				endingangle = -360
				anglerange = 40
				angle = (-anglerange)*((float(tachometer_arduino) - 8000.0)/1000.0)+startingangle
		needle = pygame.transform.rotate(needle_orig, angle)
		needle_rect = needle.get_rect(center=needle_rect.center)
		#needleangle = needleangle - 1
		angle = angle - 1
		#print needleangle
		screen.blit(needle, needle_rect)
		
		
		'''Calculate  Fuel Level'''
		'''fuel_level_adc_arduino = "0" #note: this value from pi is a raw dump of the adc from 0 to 1024 (630=emplty, 210=full) '''
		try:
			eqn_m = (0.0-100.0)/(630.0-165.0)
			eqn_b = 100.0-(eqn_m*165.0)
			fuel_level = (float(fuel_level_adc_arduino)*eqn_m) + eqn_b
			fuelstate = int((fuel_level/100)*16)
			#print "ardu:"+fuel_level_adc_arduino+"fuel100:"+str(fuel_level)+"m:"+str(eqn_m)+"b:"+str(eqn_b)
		except:
			print "error fuel level"
			
		'''Oil Temperature'''
		'''Temperature = -63.8*ln("resistance")+479.71'''
		
		try:
			#oil_temperature_resistance_arduino = 105
			oil_temperature = -63.8*math.log(float(oil_temperature_resistance_arduino),2.718281828459)+479.71
			engine_tempstate = int((((oil_temperature-120.0))/180)*16.0)
			if config_engine_temp_units == "f":
				speedtext = font_airtemp.render(str(int(oil_temperature)) + unichr(176)+"F", 1, (255, 255, 255))
			if config_engine_temp_units == "c":
				speedtext = font_airtemp.render(str(int((oil_temperature-32)/1.8)) + unichr(176)+"C", 1, (255, 255, 255))
			speedtext_rect = speedtext.get_rect(right = 155, top = 270) #(right = 440, top = 148)
		except:
			print "error temperature level"
			
		screen.blit(speedtext, speedtext_rect) 
		
		
		'''Create Head Light Button'''
		#screen.blit(headlightsoff, (0,0))
		#leftmousebutton_up(currentmousebutton)
		
		'''if 104 > mousex > 34 and 80 > mousey > 13 and leftmousebutton_up(click[0]): #head lights
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
				#wiperplusstate = 1'''
				
		if  87 > mousex > 7 and 471 > mousey > 406 and leftmousebutton_up(click[0]): # lightbar
			if lightbarstate == 1:
				lightbarstate = 0
			else:
				lightbarstate = 1
				
		'''if  173 > mousex > 111 and 366 > mousey > 318 and leftmousebutton_up(click[0]): # temp toggle Celcius and fahrenheit
			if degC == 1:
				degC = 0
			else:
				degC = 1'''
				
		'''if  475 > mousex > 328 and 211 > mousey > 120 and leftmousebutton_up(click[0]): # Speed toggle KM/H and MPH
			if kmh == 1:
				kmh = 0
			else:
				kmh = 1'''
				
		if  241 > mousex > 175 and 470 > mousey > 400 and leftmousebutton_up(click[0]): # music button
			#code for switching to music application
			print "Switch to music app"
			ps = subprocess.Popen(['wmctrl','-a','audacious'], stdout=subprocess.PIPE)
			
		if  603 > mousex > 553 and 470 > mousey > 404 and leftmousebutton_up(click[0]): #gps button
			#code for switching to navit
			print "Switich to Navit"
			ps = subprocess.Popen(['wmctrl','-a','Navit'], stdout=subprocess.PIPE)
			
		if  800 > mousex > 720 and 480 > mousey > 410 and leftmousebutton_up(click[0]): # Config Button
			state = "config_page1"						
				
		'''Reset Trip when trip value is held for 3 seconds'''		
		if  700 > mousex > 600 and 380 > mousey > 320 and (click[0]) and odo_state == 0: # Counter for reset tripometer
			tripometer_index = tripometer_index + 1

		if 700 > mousex > 600 and 380 > mousey > 320 and tripometer_index > 20 and not(click[0]) and odo_state == 0:
			tripometer_index = 0
			odo_state = 1
			tripometer = int(odometer_arduino)
			speedtext = font_tripreset.render("Trip Reset", 1, (255, 255, 255))
			speedtext_rect = speedtext.get_rect(right = 540, top = 4) #(right = 440, top = 148)
			screen.blit(speedtext, speedtext_rect) 

		if tripometer_index > 20 and odo_state == 0:
			speedtext = font_tripreset.render("Trip Reset", 1, (255, 255, 255))
			speedtext_rect = speedtext.get_rect(right = 540, top = 4) #(right = 440, top = 148)
			screen.blit(speedtext, speedtext_rect) 
				
		if  700 > mousex > 600 and 380 > mousey > 320 and leftmousebutton_up(click[0]): # Toggle Odometer and Tripometer
			if odometer_error_flag_from_arduino == 1:
				screen.blit(background, (0,0))
				speedtext = font_airtemp.render("Please Wait", 1, (255, 255, 255))
				speedtext_rect = speedtext.get_rect(right = 680, top = 331) #(right = 440, top = 148)
				screen.blit(speedtext, speedtext_rect) 
				speedtext = font_airtemp.render("Updating Odo", 1, (255, 255, 255))
				speedtext_rect = speedtext.get_rect(right = 675, top = 349) #(right = 440, top = 148)
				screen.blit(speedtext, speedtext_rect) 
				pygame.display.update()
				init_send_arduino_odometer()
				
			else:
				if odo_state == 1:
					odo_state = 0
				else:
					odo_state = 1

				
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
				
		'''Finish off by update the full display surface to the screen'''
		'''Update buttons'''
		'''if headlightsstate == 1:
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
			screen.blit(wiperminusoff, (0,0))'''
			
		
		if lightbarstate == 1:
			screen.blit(lightbaron, (3,400))
			GPIO.output(lightbarpin, False)
		else:
			screen.blit(lightbaroff, (3,400))
			GPIO.output(lightbarpin, True)
			
		'''if hornstate == 1:
			screen.blit(hornon, (0,0))
			GPIO.output(hornpin, False)
		else:
			screen.blit(hornoff, (0,0))
			GPIO.output(hornpin, True)'''
			
		if fuelstate == 16:
			screen.blit(fuel16, (642,108))
		elif fuelstate == 15:
			screen.blit(fuel15, (642,108))
		elif fuelstate == 14:
			screen.blit(fuel14, (642,108))
		elif fuelstate == 13:
			screen.blit(fuel13, (642,108))
		elif fuelstate == 12:
			screen.blit(fuel12, (642,108))
		elif fuelstate == 11:
			screen.blit(fuel11, (642,108))
		elif fuelstate == 10:
			screen.blit(fuel10, (642,108))
		elif fuelstate == 9:
			screen.blit(fuel9, (642,108))
		elif fuelstate == 8:
			screen.blit(fuel8, (642,108))
		elif fuelstate == 7:
			screen.blit(fuel7, (642,108))
		elif fuelstate == 6:
			screen.blit(fuel6, (642,108))
		elif fuelstate == 5:
			screen.blit(fuel5, (642,108))
		elif fuelstate == 4:
			screen.blit(fuel4, (642,108))
		elif fuelstate == 3:
			screen.blit(fuel3, (642,108))
		elif fuelstate == 2:
			screen.blit(fuel2, (642,108))
		elif fuelstate == 1:
			screen.blit(fuel1, (642,108))
			
		if engine_tempstate == 16:
			screen.blit(temp16, (95,105))
		elif engine_tempstate == 15:
			screen.blit(temp15, (95,105))
		elif engine_tempstate == 14:
			screen.blit(temp14, (95,105))
		elif engine_tempstate == 13:
			screen.blit(temp13, (95,105))
		elif engine_tempstate == 12:
			screen.blit(temp12, (95,105))
		elif engine_tempstate == 11:
			screen.blit(temp11, (95,105))
		elif engine_tempstate == 10:
			screen.blit(temp10, (95,105))
		elif engine_tempstate == 9:
			screen.blit(temp9, (95,105))
		elif engine_tempstate == 8:
			screen.blit(temp8, (95,105))
		elif engine_tempstate == 7:
			screen.blit(temp7, (95,105))
		elif engine_tempstate == 6:
			screen.blit(temp6, (95,105))
		elif engine_tempstate == 5:
			screen.blit(temp5, (95,105))
		elif engine_tempstate == 4:
			screen.blit(temp4, (95,105))
		elif engine_tempstate == 3:
			screen.blit(temp3, (95,105))
		elif engine_tempstate == 2:
			screen.blit(temp2, (95,105))
		elif engine_tempstate == 1:
			screen.blit(temp1, (95,105))
		
		screen.blit(musicbutton, (172,400))	
		screen.blit(gpsbutton, (552,405))
			
		if odo_state == 0:
			screen.blit(tripometer_texton, (613,375))
		
		if engine_tempstate >= 12: #12
			screen.blit(enginetemperature_lighton, (430,277))
			
		if fuelstate <= 2:
			screen.blit(lowfuel_lighton, (388,275))
					
	#------------------------------------------------------------------ Display State = Configuration Page 1-------------------------------------- 
	if state == "config_page1":	
		'''Draw configuration background'''
		screen.blit(config_bg, (0,0))	
		
		if  70 > mousex > 0 and 70 > mousey > 0 and leftmousebutton_up(click[0]): # Back to Gauged
			state = "gauge"
			save_configuration_txtfile()
			
		
		'''Speed Sensor'''
		#Display then check if one is clicked
		if config_speed_sensor_type == "gpsandcv":
			screen.blit(speed_sensor_gpsandcv, (327,106))
		if config_speed_sensor_type == "cv":
			screen.blit(speed_sensor_cvpickup, (327,106))
		if config_speed_sensor_type == "gps":
			screen.blit(speed_sensor_gps, (327,106))
		if  415 > mousex > 330 and 160 > mousey > 110 and leftmousebutton_up(click[0]): # Back to Gauged
			config_speed_sensor_type = "gpsandcv"
		if  508 > mousex > 416 and 160 > mousey > 110 and leftmousebutton_up(click[0]): # Back to Gauged
			config_speed_sensor_type = "cv"
		if  570 > mousex > 509 and 160 > mousey > 110 and leftmousebutton_up(click[0]): # Back to Gauged
			config_speed_sensor_type = "gps"
			
		'''Speed Units'''
		#Display then check if one is clicked
		if kmh == 1:
			screen.blit(speed_units_kmh, (328,163))
		if kmh == 0:
			screen.blit(speed_units_mph, (328,163))
		if  415 > mousex > 330 and 215 > mousey > 165 and leftmousebutton_up(click[0]): # Back to Gauged
			kmh = 0
		if  508 > mousex > 416 and 215 > mousey > 165 and leftmousebutton_up(click[0]): # Back to Gauged
			kmh = 1
			
		'''Air Temperature Units'''
		#Display then check if one is clicked
		
		if degC == 0:
			screen.blit(degree_f_on, (327,222))
			screen.blit(degree_c_off, (420,222))
		if degC == 1:
			screen.blit(degree_f_off, (327,222))
			screen.blit(degree_c_on, (420,222))
		if  385 > mousex > 330 and 275 > mousey > 225 and leftmousebutton_up(click[0]): # Back to Gauged
			degC = 0
		if  475 > mousex > 425 and 275 > mousey > 225 and leftmousebutton_up(click[0]): # Back to Gauged
			degC = 1
			
		'''Engine Termperature Units'''
		if config_engine_temp_units == "f":
			screen.blit(degree_f_on, (327,279))
			screen.blit(degree_c_off, (420,279))
		if config_engine_temp_units == "c":
			screen.blit(degree_f_off, (327,279))
			screen.blit(degree_c_on, (420,279))
		if  385 > mousex > 330 and 333 > mousey > 282 and leftmousebutton_up(click[0]): # Engine Temp F button
			config_engine_temp_units = "f"
		if  475 > mousex > 425 and 333 > mousey > 282 and leftmousebutton_up(click[0]): # Back to Gauged
			config_engine_temp_units = "c"
	
		
		'''Metering and Error Log Buttons'''
		screen.blit(metering, (234,353))
		screen.blit(errorlog, (448,350))
		if  353 > mousex > 235 and 424 > mousey > 354 and leftmousebutton_up(click[0]): # Metering Button
			state = "metering"
		if  570 > mousex > 452 and 424 > mousey > 354 and leftmousebutton_up(click[0]): # Error Log Button
			state = "errorlog"
			
		'''Left and Right Page Select Buttons'''
		if  800 > mousex > 720 and 480 > mousey > 400 and leftmousebutton_up(click[0]): # Right Arrow
			state = "config_page2"
		if  80 > mousex > 0 and 480 > mousey > 400 and leftmousebutton_up(click[0]): # Left Arrow
			state = "config_page2"
			
			
	#------------------------------------------------------------------ Display State = Configuration Page 2-------------------------------------- 			
	if state == "config_page2":	
		'''Draw configuration background'''
		screen.blit(config_bg2, (0,0))	
		
		if  70 > mousex > 0 and 70 > mousey > 0 and leftmousebutton_up(click[0]): # Back to Gauged
			state = "gauge"
			save_configuration_txtfile()

		'''Display Elevation'''
		#Display then check if one is clicked
		if config_elevation_units == "feet":
			screen.blit(elevation_units_feet, (328,106))
		if config_elevation_units == "meters":
			screen.blit(elevation_units_meters, (328,106))
		if  415 > mousex > 330 and 160 > mousey > 110 and leftmousebutton_up(click[0]): # 
			config_elevation_units = "feet"
		if  508 > mousex > 416 and 160 > mousey > 110 and leftmousebutton_up(click[0]): # 
			config_elevation_units = "meters"
			
		'''Elevation Climb'''
		#Display then check if one is clicked
		if config_elevation_climb == "on":
			screen.blit(elevation_climb_on, (0,0))
			screen.blit(on_on, (327,164))
			screen.blit(off_off, (420,164))
		if config_elevation_climb == "off":
			screen.blit(on_off, (327,164))
			screen.blit(off_on, (420,164))
		if  385 > mousex > 330 and 215 > mousey > 165 and leftmousebutton_up(click[0]): # on
			config_elevation_climb = "on"
		if  475 > mousex > 425 and 215 > mousey > 165 and leftmousebutton_up(click[0]): # off
			config_elevation_climb = "off"
			
		'''Display Traction'''
		#Display then check if one is clicked
		if config_display_traction == "on":
			screen.blit(on_on, (327,223))
			screen.blit(off_off, (420,223))
		if config_display_traction == "off":
			screen.blit(on_off, (327,223))
			screen.blit(off_on, (420,223))
		if  385 > mousex > 330 and 275 > mousey > 225 and leftmousebutton_up(click[0]): # On
			config_display_traction = "on"
		if  475 > mousex > 425 and 275 > mousey > 225 and leftmousebutton_up(click[0]): # Off
			config_display_traction = "off"
			
		'''Clock Units'''
		if config_clock_units == "12h":
			screen.blit(clock_12h, (328,284))
		if config_clock_units == "24h":
			screen.blit(clock_24h, (328,284))
		if  411 > mousex > 330 and 333 > mousey > 282 and leftmousebutton_up(click[0]): # 12h
			config_clock_units = "12h"
		if  504 > mousex > 425 and 333 > mousey > 282 and leftmousebutton_up(click[0]): # 24h
			config_clock_units = "24h"
	
		'''Daylight Savings'''
		if config_daylight_savings == "on":
			screen.blit(on_on, (327,342))
			screen.blit(off_off, (420,342))
		if config_daylight_savings == "off":
			screen.blit(on_off, (327,342))
			screen.blit(off_on, (420,342))
		if  385 > mousex > 330 and 395 > mousey > 345 and leftmousebutton_up(click[0]): # On
			config_daylight_savings = "on"
		if  475 > mousex > 425 and 395 > mousey > 345 and leftmousebutton_up(click[0]): # Off
			config_daylight_savings = "off"
		
		'''Left and Right Page Select Buttons'''
		if  800 > mousex > 720 and 480 > mousey > 400 and leftmousebutton_up(click[0]): # Right Arrow
			state = "config_page1"
		if  80 > mousex > 0 and 480 > mousey > 400 and leftmousebutton_up(click[0]): # Left Arrow
			state = "config_page1"

	#------------------------------------------------------------------ Display State = Metering Page -------------------------------------- 	
	if state == "metering":	
		'''Display Metering Page Background'''
		screen.blit(metering_page, (0,0))
		
		if  70 > mousex > 0 and 70 > mousey > 0 and leftmousebutton_up(click[0]): # Back to Gauged
			state = "config_page1"
			
		#Display Arduino Variables
		speedtext = font_metering_title.render("Raw from Arduino", 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(left = 40, top = 90) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
		
		speedtext = font_airtemp.render("Left Wheel Speed:", 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(right = 220, top = 120) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
		speedtext = font_airtemp.render(leftspeed_arduino+" km/h", 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(left = 230, top = 120) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
				
		speedtext = font_airtemp.render("Right Wheel Speed:", 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(right = 220, top = 140) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
		speedtext = font_airtemp.render(rightspeed_arduino+" km/h", 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(left = 230, top = 140) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
				
		speedtext = font_airtemp.render("Tachometer:", 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(right = 220, top = 160) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
		speedtext = font_airtemp.render(str(tachometer_arduino) +" rpm", 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(left = 230, top = 160) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
		
		speedtext = font_airtemp.render("Oil Temp Resistance", 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(right = 220, top = 180) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
		speedtext = font_airtemp.render(oil_temperature_resistance_arduino+unichr(937)+" ohms", 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(left = 230, top = 180) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
		
		speedtext = font_airtemp.render("Fuel Level ADC:", 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(right = 220, top = 200) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
		speedtext = font_airtemp.render(fuel_level_adc_arduino+" (630->165)", 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(left = 230, top = 200) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
		
		speedtext = font_airtemp.render("Air Temperature", 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(right = 220, top = 220) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
		speedtext = font_airtemp.render(airtemperature_arduino+unichr(176)+"C", 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(left = 230, top = 220) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
		
		speedtext = font_airtemp.render("Left Turn Light:", 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(right = 220, top = 240) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
		speedtext = font_airtemp.render(left_turn_light_arduino, 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(left = 230, top = 240) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
		
		speedtext = font_airtemp.render("Right Turn Light:", 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(right = 220, top = 260) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
		speedtext = font_airtemp.render(right_turn_light_arduino, 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(left = 230, top = 260) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
		
		speedtext = font_airtemp.render("Oil Light:", 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(right = 220, top = 280) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
		speedtext = font_airtemp.render(oil_light_arduino, 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(left = 230, top = 280) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
		
		speedtext = font_airtemp.render("Alternator Light:", 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(right = 220, top = 300) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
		speedtext = font_airtemp.render(alternator_light_arduino, 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(left = 230, top = 300) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
		
		speedtext = font_airtemp.render("Highbeam Light:", 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(right = 220, top = 320) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
		speedtext = font_airtemp.render(highbeam_light_arduino, 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(left = 230, top = 320) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
		
		speedtext = font_airtemp.render("pi on:", 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(right = 220, top = 340) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
		speedtext = font_airtemp.render(pi_on_arduino, 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(left = 230, top = 340) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
		
		
		#Display GPS Variables
		speedtext = font_metering_title.render("Raw from GPS", 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(left = 500, top = 90) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
		
		speedtext = font_airtemp.render("Status:", 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(right = 580, top = 120) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
		if gps_speed_flag == 1:
			speedtext = font_airtemp.render(" FIX", 1, (255, 255, 255))
		else:
			speedtext = font_airtemp.render(" NO FIX", 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(left = 590, top = 120) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
				
		speedtext = font_airtemp.render("GPS Speed:", 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(right = 580, top = 140) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
		speedtext = font_airtemp.render(str(gps_speed_kmh)+" km/h", 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(left = 590, top = 140) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
				
		speedtext = font_airtemp.render("Altitude:", 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(right = 580, top = 160) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
		speedtext = font_airtemp.render(str(int(gps_altitude_feet)) +" ft", 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(left = 590, top = 160) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
		
		speedtext = font_airtemp.render("Vertical Climb:", 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(right = 580, top = 180) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
		speedtext = font_airtemp.render(str(int(gps_climb_feetpermin)) + " ft/min", 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(left = 590, top = 180) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
		
		speedtext = font_airtemp.render("GPS Time:", 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(right = 580, top = 200) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
		speedtext = font_airtemp.render(gps_time_pst, 1, (255, 255, 255))
		speedtext_rect = speedtext.get_rect(left = 590, top = 200) #(right = 440, top = 148)
		screen.blit(speedtext, speedtext_rect) 
		
		
		
		

	#------------------------------------------------------------------ Display State = Error Log -------------------------------------- 	
	if state == "errorlog":	
		'''Display Error Log Page Background'''
		screen.blit(errorlog_page, (0,0))
		
		if  70 > mousex > 0 and 70 > mousey > 0 and leftmousebutton_up(click[0]): # Back to Gauged
			state = "config_page1"
	
		'''Need to add all printed information to an array, then print the array on each line to show the log'''
		
	
	#------------------------------------------------------------------ -------------------------------------- 
	
	if pi_on_index > 0: #counts up to 40
		screen.blit(shutdown_countdown, (0,0))
		if 30 >= pi_on_index > 0:
			speedtext = font_shutdown_countdown.render(str((40-pi_on_index)/10), 1, (255, 255, 255))
			speedtext_rect = speedtext.get_rect(right = 430, top = 260) #(right = 450, top = 130)
			screen.blit(speedtext, speedtext_rect) 
		if pi_on_index > 30:
			speedtext = font_shutdown_countdown.render("NOW", 1, (255, 255, 255))
			speedtext_rect = speedtext.get_rect(right = 520, top = 260) #(right = 450, top = 130)
			screen.blit(speedtext, speedtext_rect) 
	
	#print previous_mouse_click
	previous_mouse_click = 0
	if click[0]:
		previous_mouse_click = 1
		
	#Update the screen	
	pygame.display.update()
	'''Add a wait'''
	#time.sleep(60)
	
ser.close()
