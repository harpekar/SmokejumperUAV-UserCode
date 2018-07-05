#!/bin/python
#The KY040 Pinout is as follows: 
# CLK is Encoder Pin A, DT is Encoder Pin B, and GND is Encoder Pin C.

import picamera
import gpiozero
import math
import time
from RPi import GPIO
from time import sleep
from bounce import arm_and_takeoff, collect_images, condition_yaw, send_global_velocity
from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil

led = gpiozero.LED(1)
button = gpiozero.Button(12)
clk = 20
dt = 21
power = 16

counter = 0
pressed = False; 

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(power, GPIO.OUT, initial = GPIO.HIGH)
#GPIO.setup(clk,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(dt,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

#camera = picamera.PiCamera();

clkLastState = GPIO.input(clk)
def button_pressed():
    global pressed
    led.on()    
    pressed = True;

def button_released():
    global pressed
    led.off()
    pressed = False;

def rotaryTurn(clkLastState):
    global counter
    clkState = GPIO.input(clk)
    dtState = GPIO.input(dt)
    if clkState != clkLastState:
	    if dtState != clkState:
		    counter -= 1
	    else:
		    counter += 1 

	    if (counter == 20) or (counter < -1):
		    counter = 0
	    clkLastState = clkState
	    sleep(0.02)
            counter = 0.75
    return counter

button.when_pressed = button_pressed
button.when_released = button_released

print "Please choose your Altitude. Press button to select"
currentHeight = 0

while not pressed: 
    clkLastState = GPIO.input(clk)
    height = rotaryTurn(clkLastState) 
   
    if height != currentHeight: 
        currentHeight = height
        print "Height =" + str(height) + "m"

print "Ascending to " + str(height) + "m"

#Set connection string  
connection_string = '/dev/serial0'

# Connect to the Vehicle
print 'Connecting to vehicle on: %s' % connection_string
vehicle = connect(connection_string,baud = 57600, wait_ready=True)
	
print "Place aircraft in launch location"
time.sleep(5)
print "Taking off in: "
for i in range (0,10):
	print 10-i
	time.sleep(1)

arm_and_takeoff(vehicle, height)

send_global_velocity(0,0,0,vehicle)

collect_images(6, camera, vehicle)
print "Returning to Launch"
vehicle.parameters['RTL_ALT'] = 0
vehicle.mode = VehicleMode("RTL")

#Close vehicle object before exiting script
print "Close vehicle object"
vehicle.close()
          
