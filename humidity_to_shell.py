#!/usr/bin/python
#
# Humidetector v0.1
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


import sys
import Adafruit_DHT
import datetime
import time
import RPi.GPIO as GPIO

# Setup GPIO Ports
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# double check these if you rewire the breadboard
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)


# initialize a trip counter
trip_count = 0
humidity_limit = 30
trip_count_limit = 3

# set defeault for previous below
humidity = 0


def blink_led(pin, speed):
    GPIO.output(pin,False)
    time.sleep(speed)
    GPIO.output(pin,True)
    time.sleep(speed)
    GPIO.output(pin, False)

# initialize LEDs
blink_led(17, 0.1)
blink_led(27, 0.1)



while True:
    # Obtain humidity values from library
    previous_humidity = humidity
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    
    # print current date and time
    print "\n" + str(datetime.datetime.now())

    # alert if humidity over threshold and trip count over limit
    if trip_count >= trip_count_limit:
        print 'Trip Count Limit Reached - Send Alert (not yet working)'
        # Set Red LED to ON
        GPIO.output(27,True)

    # humidity over limit
    if humidity >= humidity_limit:
        print 'Humidity Over Threshold!'
        # increase tripcount
        if trip_count < trip_count_limit:
            trip_count += 1
            # Blink Red LED
            blink_led(27, 0.2)

    
    # humidity under limit but trip_count tripped
    if humidity < humidity_limit and trip_count > 0:
        trip_count -= 1
        blink_led(17, 0.5)
    
    # humidity increasing
    if humidity > previous_humidity:
        print 'Humidity increased (+) from ' + str(previous_humidity) + '% to ' + str(humidity) + '%'
    
    # humidity decreasing
    if humidity < previous_humidity:
        print 'Humidity decreased (-) from ' + str(previous_humidity) + '% to ' + str(humidity) + '%'
        
    # humidity stable
    if humidity == previous_humidity:
        print 'Humidity stable at ' + str(humidity) + '%'
        if trip_count == 0:
            GPIO.output(27, False)

    
    # Notify if Over Threshold for Trip Count
    #print 'Temp: {0:0.1f} C Humidity: {1:0.1f} %'.format(temperature, humidity)
    print 'Temperature is {0:0.1f} C'.format(temperature)
    blink_led(17, 0.05)
    GPIO.output(17, True)
