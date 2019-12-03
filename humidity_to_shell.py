#!/usr/bin/python
import sys
import Adafruit_DHT
import datetime
#from __future__ import print_function

# initialize a trip counter
trip_count = 0
humidity_limit = 30
trip_count_limit = 3

# set defeault for previous below
humidity = 0

while True:
    # Obtain humidity values from library
    previous_humidity = humidity
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    
    # print current date and time
    print "\n" + str(datetime.datetime.now())

    # alert if humidity over threshold and trip count over limit
    if trip_count >= trip_count_limit:
        print 'Trip Count Limit Reached - Send Alert (not yet working)'

    # humidity over limit
    if humidity >= humidity_limit:
        print 'Humidity Over Threshold!'
        # increase tripcount
        if trip_count < trip_count_limit:
            trip_count += 1
    
    # humidity under limit but trip_count tripped
    if humidity < humidity_limit and trip_count > 0:
        trip_count -= 1
    
    # humidity increasing
    if humidity > previous_humidity:
        print 'Humidity increased (+) from ' + str(previous_humidity) + '% to ' + str(humidity) + '%'
    
    # humidity decreasing
    if humidity < previous_humidity:
        print 'Humidity decreased (-) from ' + str(previous_humidity) + '% to ' + str(humidity) + '%'
        

    # humidity stable
    if humidity == previous_humidity:
        print 'Humidity stable at ' + str(humidity) + '%'
        
    
    
    
    # Notify if Over Threshold for Trip Count
    #print 'Temp: {0:0.1f} C Humidity: {1:0.1f} %'.format(temperature, humidity)
    print 'Temperature is {0:0.1f} C'.format(temperature)
