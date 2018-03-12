#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Author: Ben Lester 
    Electrical and Computer Engineering Senior Capstone
    Oregon State University
"""

from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil
import time
import math
#import picamera

DEBUG = True

# Initialize Camera Object 
# camera = picamera.PiCamera()

#DEBUG tests code without piCamera and using SITL 
if DEBUG == True:
   connection_string = 0
else:
   connection_string = '/dev/serial0'

sitl = None


#Start SITL if DEBUG enabled 
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()


# Connect to the Vehicle
print 'Connecting to vehicle on: %s' % connection_string
vehicle = connect(connection_string,baud = 57600, wait_ready=True)


# Function to arm and takeoff copter
# Monitors alititude and confirms alitude before falling out of function
def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print "Basic pre-arm checks"
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print " Waiting for vehicle to initialise..."
        time.sleep(1)

        
    print "Arming motors"
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True    

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:      
        print " Waiting for arming..."
        time.sleep(1)

    print "Taking off!"
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print " Altitude: ", vehicle.location.global_relative_frame.alt 
        #Break and return from function just below target altitude.        
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: 
            print "Reached target altitude"
            break
        time.sleep(1)

# Function to yaw the copter
# Needs a check function to monitor yaw progress
def condition_yaw(heading, relative=True):
    if relative:
        is_relative=1 #yaw relative to direction of travel
    else:
        is_relative=0 #yaw is an absolute angle
    # create the CONDITION_YAW command using command_long_encode()
    msg = vehicle.message_factory.command_long_encode(
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
        0, #confirmation
        heading,    # param 1, yaw in degrees
        0,          # param 2, yaw speed deg/s
        1,          # param 3, direction -1 ccw, 1 cw
        is_relative, # param 4, relative offset 1, absolute angle 0
        0, 0, 0)    # param 5 ~ 7 not used
    # send command to vehicle
    vehicle.send_mavlink(msg)

'''    while True:
	print "Yaw heading: ", 

'''

# Function to adjust yaw and trigger camera for full 360 degrees
def collect_images(image_number):
    image_number = 10 		# Number of images to be collected
    degrees = 360/image_number	# Heading offset in degrees per image
    heading = 0			# Innitial heading in degrees

    for i in range (1,image_number):
	if DEBUG == True:
	   print 'Capturing image at %s degrees' % heading
	else:
	   camera.capture('image%s.jpg' % i)
	time.sleep(1)
	print 'Image %s saved' % i
        condition_yaw(degrees)
        heading = heading + degrees
	time.sleep(3)


arm_and_takeoff(10)

collect_images(10)

print "Returning to Launch"
vehicle.mode = VehicleMode("RTL")

#Close vehicle object before exiting script
print "Close vehicle object"
vehicle.close()

# Shut down simulator if it was started.
if sitl is not None:
    sitl.stop()
