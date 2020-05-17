# -*- coding: utf-8 -*-
import urllib2
import json
import time
import Adafruit_DHT
import RPi.GPIO as GPIO
#import datatime
sensor=Adafruit_DHT.DHT11
GPIO_DHT=4
GPIO_IR=11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(GPIO_IR,GPIO.IN)

#humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
#print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
url = "http://api.heclouds.com/devices/597808637/datapoints"
API_KEY = 'pUMeUM=pxUhsNZcyLSOkYqNexKA='
headers = {'api-key':API_KEY}
while True:
	humidity, temperature = Adafruit_DHT.read_retry(sensor, GPIO_DHT)
	if humidity is not None and temperature is not None:
		values = {"datastreams":[{"id":"temp","datapoints":[{"value":temperature}]}]}
		print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
		jdata = json.dumps(values)
		request = urllib2.Request(url, jdata)
		request.add_header('api-key', API_KEY)
		request.get_method = lambda:'POST' # 设置HTTP的访问方式 
		request = urllib2.urlopen(request)
		print request.read()
		values = { "datastreams": [ { "id": "hum", "datapoints": [{"value":humidity}]}]}
		jdata = json.dumps(values)
		request = urllib2.Request(url,jdata)
        	request.add_header('api-key',API_KEY)
        	request.get_metmod = lambda:'POST'
        	request = urllib2.urlopen(request)
		print request.read()
		if GPIO.input(GPIO_IR)==GPIO.HIGH:
			IR=0
		else: IR=1

		values = { "datastreams": [ { "id": "ir", "datapoints": [{"value":IR}]}]}
        	jdata = json.dumps(values)
        	request = urllib2.Request(url,jdata)
        	request.add_header('api-key',API_KEY)
        	request.get_metmod = lambda:'POST'
        	request = urllib2.urlopen(request)
		print request.read()
