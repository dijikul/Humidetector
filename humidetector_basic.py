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

# DHT11 Sensor Data Pin
sensor_pin = 21

# ignore errors
io.setwarnings(False)
io.setmode(io.BCM)

# clear terminal
os.system('cls' if os.name == 'nt' else 'clear')

# App Init
print('Humidetector Initializing')

humidity, temperature = Adafruit_DHT.read_retry(11, sensor_pin)
print('Current Humidity at ' + str(humidity) + ' and Temperature at ' + str(temperature))

while(1):
    # Obtain humidity values from library
    previous_humidity = humidity

    humidity, temperature = Adafruit_DHT.read_retry(11, sensor_pin)
   
    # print current date and time
    print("\n" + str(datetime.datetime.now()))

    # alert if humidity over threshold and trip count over limit
    if trip_count >= trip_count_limit:
        print('Trip Count Limit Reached - Send Alert (not yet working)')
    # humidity over limit
    if humidity >= humidity_limit:
        print('Humidity Over Threshold!')
        # increase tripcount
        if trip_count < trip_count_limit:
            trip_count += 1

   
    # humidity under limit but trip_count tripped
    if humidity < humidity_limit and trip_count > 0:
        trip_count -= 1
    
    # humidity increasing
    if humidity > previous_humidity:
        print('Humidity increased (+) from ' + str(previous_humidity) + '% to ' + str(humidity) + '%')
    
    # humidity decreasing
    if humidity < previous_humidity:
        print('Humidity decreased (-) from ' + str(previous_humidity) + '% to ' + str(humidity) + '%')
        
    # humidity stable
    if humidity == previous_humidity:
        print('Humidity stable at ' + str(humidity) + '%')

    
    # Notify if Over Threshold for Trip Count
    #print 'Temp: {0:0.1f} C Humidity: {1:0.1f} %'.format(temperature, humidity)
    print('Temperature is {0:0.1f} C'.format(temperature))
    
    #GPIO.output(17, True)
    time.sleep(polling_interval)


