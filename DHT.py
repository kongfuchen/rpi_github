# -*- coding: utf-8 -*-
import Adafruit_DHT
import urllib2
import json
import time

url = "http:// api.heclouds.com/devices/597808637/datapoints"
API_KEY ='pUMeUM=pxUhsNZcyLSOkYqNexKA='
headers = {'api-key':API_KEY}
  
# Set sensor type : Options are DHT11,DHT22 or AM2302
sensor=Adafruit_DHT.DHT11
  
# Set GPIO sensor is connected to
gpio=4

while True:
  
    # Use read_retry method. This will retry up to 15 times to
    # get a sensor reading (waiting 2 seconds between each retry).
    humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
  
    # Reading the DHT11 is very sensitive to timings and occasionally
    # the Pi might fail to get a valid reading. So check if readings are valid.
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        values = { "datastreams": [ { "id": "temp", "datapoints": [{"value":33}]}]}
      	jdata = json.dumps(values)
        request = urllib2.Request(url,jdata)
        request.add_header('api-key',API_KEY)
        request.get_metmod = lambda:'POST'
        request = urllib2.urlopen(request)
        print request.read()
    else:
        print('Failed to get reading. Try again!')

        
