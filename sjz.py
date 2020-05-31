import Adafruit_DHT
import RPi.GPIO as GPIO
import serial
ser = serial.Serial("/dev/ttyAMA0",115200)
sensor=Adafruit_DHT.DHT11
GPIO_DHT=4
while True:
	humidity, temperature = Adafruit_DHT.read_retry(sensor, GPIO_DHT)
	if humidity is not None and temperature is not None:
		print(temperature)
		temp=str(temperature)
		ser.write(temp+'\n')
