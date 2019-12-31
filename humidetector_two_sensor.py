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
from datetime import datetime
import time
import RPi.GPIO as io

# ES Logging implementation below
from elasticsearch import Elasticsearch

# initialize ES Client Connection
es = Elasticsearch([
    { 'host':'192.168.1.4' }
    ])



# Initialize Variables

# DHT11 Sensor has 1-second polling intervals (1hz)
# DHT22 Sensor has 2-second polling intervals (0.5hz)
polling_interval = 30
trip_count = 0
humidity_limit = 50
trip_count_limit = 3
es_index = "humidetector"
location = "testing"
send_to_elastic = 0



# DHT11 Sensor Data Pin
dht11_pin = 21
# DHT22 Sensor Data Pin
dht22_pin = 26



# ignore errors
io.setwarnings(False)
io.setmode(io.BCM)

# ES Post Function
def log_values(h1, t1, h2, t2):
    
    # Handle bad humidity reading
    if h1 > 100:
        # humidity mis-read: Cannot be this high.  DHT-11 sensor maxes out around 90% Humidity.
        # Humidity can't be over 100%
        print("Bad DHT11 Humidity Reading - setting " + str(h1) + "% to negative one ( -1 )")
        h1 = -1
        
    # Handle bad humidity reading on DHT22 (probably not an issue, but just in case)
    if h2 > 100:
        # humidity mis-read: Cannot be this high.  DHT-11 sensor maxes out around 90% Humidity.
        # Humidity can't be over 100%
        print("Bad DHT22 Humidity Reading - setting " + str(h2) + "% to negative one ( -1 )")
        h2 = -1
        

    # Create document to send to ElasticSearch 
    doc = {
        'datetime': datetime.utcnow(),
        'dht11_humidity': int(h1),
        'dht11_temperature': int(t1),
        'dht22_humidity': int(h2),
        'dht22_temperature': int(t2),
        'location': str(location)
        }
    
    if send_to_elastic == 1:
        try:
            res = es.index(index=es_index, doc_type="humidetector", body=doc)
            print(res['result'])
        except ConnectionError as error:
            print(" Connection Error Occured")
            pass
        except Exception as error:
            print(error)
            pass
        #res.indices.refrsh(index=es_index)
    
    

# clear terminal
os.system('cls' if os.name == 'nt' else 'clear')

# App Init
print('Humidetector Initializing...')

# Init DHT11
humidity1, temperature1 = Adafruit_DHT.read_retry(11, dht11_pin)
print('DHT11 Sensor Initialized:\nHumidity: ' + str(humidity1) + ' and Temperature at ' + str(temperature1))
# Init DHT22
humidity2, temperature2 = Adafruit_DHT.read_retry(22, dht22_pin)
print('DHT22 Sensor Initialized:\nHumidity: ' + str(humidity2) + ' and Temperature at ' + str(temperature2))





while(1):
    # Obtain humidity values
    
    previous_dht11_humidity = humidity1
    previous_dht22_humidity = humidity2


    humidity1, temperature1 = Adafruit_DHT.read_retry(11, dht11_pin)
    humidity2, temperature2 = Adafruit_DHT.read_retry(22, dht22_pin)
   
    # print current date and time
    print("\n" + str(datetime.now()))

    # alert if humidity over threshold and trip count over limit
    if trip_count >= trip_count_limit:
        print('Trip Count Limit Reached - Send Alert (not yet working)')
    # humidity over limit
    if (humidity1 >= humidity_limit) or (humidity2 >= humidity_limit):
        print('Humidity detected over threshold!')
        # increase tripcount
        if trip_count < trip_count_limit:
            trip_count += 1



    # humidity under limit but trip_count tripped
    # only decrease if both sensors showing under the limit
    if (humidity1 < humidity_limit and trip_count > 0) and (humidity2 < humidity_limit and trip_count > 0):
        trip_count -= 1

    # DHT11 Stuff Here
    # humidity increasing
    if humidity1 > previous_dht11_humidity:
        print('DHT11 Humidity increased (+) from ' + str(previous_dht11_humidity) + '% to ' + str(humidity1) + '%')
    # humidity decreasing
    if humidity1 < previous_dht11_humidity:
        print('DHT11 Humidity decreased (-) from ' + str(previous_dht11_humidity) + '% to ' + str(humidity1) + '%')
    # humidity stable
    if humidity1 == previous_dht11_humidity:
        print('DHT11 Humidity stable at ' + str(humidity1) + '%')
        
    #DHT22 Stuff Here (basically a copy of the above)
    # humidity increasing
    if humidity2 > previous_dht22_humidity:
        print('DHT22 Humidity increased (+) from ' + str(previous_dht22_humidity) + '% to ' + str(humidity2) + '%')
    # humidity decreasing
    if humidity2 < previous_dht22_humidity:
        print('DHT22 Humidity decreased (-) from ' + str(previous_dht22_humidity) + '% to ' + str(humidity2) + '%')
    # humidity stable
    if humidity2 == previous_dht22_humidity:
        print('DHT22 Humidity stable at ' + str(humidity2) + '%')

    
    # Notify if Over Threshold for Trip Count
    #print 'Temp: {0:0.1f} C Humidity: {1:0.1f} %'.format(temperature, humidity)
    print('DHT11 Temp is {0:0.1f} C'.format(temperature1))
    print('DHT22 Temp is {0:0.1f} C'.format(temperature2))
    
    log_values(humidity1, temperature1, humidity2, temperature2)
    
        
    #GPIO.output(17, True)
    time.sleep(polling_interval)


