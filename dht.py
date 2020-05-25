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
GPIO_MQ_2=13
GPIO.setmode(GPIO.BOARD)
GPIO.setup(GPIO_IR,GPIO.IN)
GPIO.setup(GPIO_MQ_2,GPIO.IN)
#humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
#print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
url = "http://api.heclouds.com/devices/599461350/datapoints"
API_KEY = 'DC1E5ISmakdYV7fzXQAG8iXL08U='
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
		values = { "datastreams": [ { "id": "humi", "datapoints": [{"value":humidity}]}]}
		jdata = json.dumps(values)
		request = urllib2.Request(url,jdata)
        	request.add_header('api-key',API_KEY)
        	request.get_metmod = lambda:'POST'
        	request = urllib2.urlopen(request)
		print request.read()
		str=time.strftime('%Y.%m.%d %H:%M:%S ',time.localtime(time.time()))
		h=int(str[10,13])
		if GPIO.input(GPIO_IR)==GPIO.HIGH and h>9 and h<17:
			IR=1
		else: IR=0
		values = { "datastreams": [ { "id": "ir", "datapoints": [{"value":IR}]}]}
        	jdata = json.dumps(values)
        	request = urllib2.Request(url,jdata)
        	request.add_header('api-key',API_KEY)
        	request.get_metmod = lambda:'POST'
        	request = urllib2.urlopen(request)
		print request.read()
		if GPIO.input(GPIO_MQ_2)==GPIO.HIGH:
			MQ_2=1
		else: MQ_2=0

		values = { "datastreams": [ { "id": "mq_2", "datapoints": [{"value":MQ_2}]}]}
        	jdata = json.dumps(values)
        	request = urllib2.Request(url,jdata)
        	request.add_header('api-key',API_KEY)
        	request.get_metmod = lambda:'POST'
        	request = urllib2.urlopen(request)
		print request.read()
