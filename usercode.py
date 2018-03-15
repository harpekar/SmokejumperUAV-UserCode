#!/bin/python
#The KY040 Pinout is as follows: 
# CLK is Encoder Pin A, DT is Encoder Pin B, and GND is Encoder Pin C.


from gpiozero import LED
from RPi import GPIO
from time import sleep
from bounce.py import arm_and_takeoff, condition_yaw, collect_images

led = gpiozero.LED(1)
button = gpiozero.Button(12)
clk = 20
dt = 21
power = 16

counter = 0
pressed = False; 

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

clkLastState = GPIO.input(clk)
button.when_pressed = button_pressed
button.when_released = button_released

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
            
	    if (counter == 20) or (counter == -20):
		    counter = 0
	    clkLastState = clkState
	    sleep(0.02)

    return counter

print "Please choose your Altitude. Press button to select"
currentHeight = 0

while not pressed: 
    clkLastState = GPIO.input(clk)
    height = 6*rotaryTurn(clkLastState) 
    #Maximum height is 120m, max output of Encoder is 20. So resolution = 6meters/div
    
    if height != currentHeight: 
        currentHeight = height
        print "Height =" + str(height) + "m"

print "Place aircraft in launch location"
time.sleep(2)
print "Taking off in: "
for i in range (10,0):
	print i
	time.sleep(1)
print "Ascending to " + str(height) + "m"
arm_and_takeoff(height)

collect_images(6)
print "Returning to Launch"
vehicle.mode = VehicleMode("RTL")

#Close vehicle object before exiting script
print "Close vehicle object"
vehicle.close()
          
