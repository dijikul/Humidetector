#!/usr/bin/python3
#
# Humidetector v0.2
#
# Detecting Humidity with a DHT11 Sensor and some LED's
#
# TO-DO:
# - Send e-mail notification (and error handling) 
# - write to database? Sqlite?
# - variables for pins / LED colours
# - threshold trip and reset timer .. how long until we re-send a notification?
# - README.md
# - publish on Github


import os
import sys
import Adafruit_DHT
import datetime
import time
import RPi.GPIO as io
#import asyncio


# initialize vars
polling_interval = 2
trip_count = 0
humidity_limit = 40
trip_count_limit = 3
rgb_state = "blue"

# blink loop variabls
blink_low = 0
blink_high = 100
blink_interval = 50

# PIN Variables
# LED Diode pin numbers
red_pin = 13
green_pin = 19
blue_pin = 26
# DHT11 Sensor Data Pin
sensor_pin = 21

# ignore errors
io.setwarnings(False)
io.setmode(io.BCM)
io.setup(red_pin,io.OUT) # make red pin an out
io.setup(green_pin,io.OUT) # make green pin an out
io.setup(blue_pin,io.OUT) # make blue pin an out

# set outputs as PWM @ 60 hz
ledR = io.PWM(red_pin, 60) 
ledG = io.PWM(green_pin, 60)
ledB = io.PWM(blue_pin, 60)


# start off the pwm    
ledR.start(0)
ledG.start(0)
ledB.start(0)

# RGB LED Set Function
def set_led(r, g, b):
    time.sleep(0.1)
    ledR.ChangeDutyCycle(r)
    ledG.ChangeDutyCycle(g)
    ledB.ChangeDutyCycle(b)
    #print("Setting LED to R: " + str(r) + " G: " + str(g) + " B: " + str(b) + "")

# RGB LED Turn Off Function
def set_led_off():
    ledR.ChangeDutyCycle(0)
    ledG.ChangeDutyCycle(0)
    ledB.ChangeDutyCycle(0)

def blink_red(low = blink_low, high = blink_high, interval = blink_interval):
    # Red Loop
    for step in range(low, high, interval):
        set_led(step, 0, 0)
    for step in range(high, low, interval * -1):
        set_led(step, 0, 0)    

def blink_green(low = blink_low, high = blink_high, interval = blink_interval):
    # Green Loop
    for step in range(low, high, interval):
        set_led(0, step, 0)
    for step in range(high, low, interval * -1):
        set_led(0, step, 0)    

def blink_blue(low = blink_low, high = blink_high, interval = blink_interval):
    # Blue Loop
    for step in range(low, high, interval):
        set_led(0, 0, step)
    for step in range(high, low, interval * -1):
        set_led(0, 0, step)    

# clear terminal
os.system('cls' if os.name == 'nt' else 'clear')

# App Init
print('Humidetector Initializing')
# obtain initial humidity
blink_red(low=0, high=100, interval=25)
blink_green(low=0, high=100, interval=25)
blink_blue(low=0, high=100, interval=25)

humidity, temperature = Adafruit_DHT.read_retry(11, sensor_pin)
print('Current Humidity at ' + str(humidity) + ' and Temperature at ' + str(temperature))

if humidity > humidity_limit:
    rgb_state = "red"
else:
    rgb_state = "green"


while(1):
    # Obtain humidity values from library
    previous_humidity = humidity

    humidity, temperature = Adafruit_DHT.read_retry(11, sensor_pin)
    blink_blue(low=0, high=70, interval=70)
    
    # print current date and time
    print("\n" + str(datetime.datetime.now()))

    # alert if humidity over threshold and trip count over limit
    if trip_count >= trip_count_limit:
        print('Trip Count Limit Reached - Send Alert (not yet working)')
        # Set Red LED to ON
        rgb_state = "red"

    # humidity over limit
    if humidity >= humidity_limit:
        print('Humidity Over Threshold!')
        # increase tripcount
        if trip_count < trip_count_limit:
            trip_count += 1
            # Blink Red LED
            blink_red(low=10, high=70, interval=35)

    
    # humidity under limit but trip_count tripped
    if humidity < humidity_limit and trip_count > 0:
        trip_count -= 1
        blink_green()
    
    # humidity increasing
    if humidity > previous_humidity:
        print('Humidity increased (+) from ' + str(previous_humidity) + '% to ' + str(humidity) + '%')
    
    # humidity decreasing
    if humidity < previous_humidity:
        print('Humidity decreased (-) from ' + str(previous_humidity) + '% to ' + str(humidity) + '%')
        
    # humidity stable
    if humidity == previous_humidity:
        print('Humidity stable at ' + str(humidity) + '%')
        if trip_count == 0:
            rgb_state = "green"

    
    # Notify if Over Threshold for Trip Count
    #print 'Temp: {0:0.1f} C Humidity: {1:0.1f} %'.format(temperature, humidity)
    print('Temperature is {0:0.1f} C'.format(temperature))
    
    # set RGB LED based on current state
    if rgb_state == "red":
        set_led(10, 0, 0)
    if rgb_state == "green":
        set_led(0, 10, 0)    
    if rgb_state == "blue":
        set_led(0, 0, 10)
    #GPIO.output(17, True)
    time.sleep(polling_interval)


