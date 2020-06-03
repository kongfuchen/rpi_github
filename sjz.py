import Adafruit_DHT
import RPi.GPIO as GPIO
import serial
import threading
from queue import Queue

ser = serial.Serial("/dev/ttyAMA0",115200)
sensor=Adafruit_DHT.DHT11
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO_DHT=4
GPIO_FAN=12
GPIO.setup(GPIO_FAN,GPIO.OUT,initial=GPIO.HIGH)
Threshold=40
def thread_1():
	global Threshold
	while True:
        	humidity, temperature = Adafruit_DHT.read_retry(sensor, GPIO_DHT)
		if humidity is not None and temperature is not None:
			print(temperature)
			temp=str(temperature)
			ser.write(temp+'\n')
			print(Threshold)
			if temperature>Threshold:
				GPIO.output(GPIO_FAN,GPIO.LOW)
			else:
				GPIO.output(GPIO_FAN,GPIO.HIGH)
def thread_2():
	global Threshold
	while True:
        	Threshold=int(ser.readline()[:2])
def multithreading():
 	threads=[]
 	Thread_1=threading.Thread(target=thread_1)
	Thread_1.start()
 	threads.append(Thread_1)
 	Thread_2=threading.Thread(target=thread_2)
 	Thread_2.start()
 	threads.append(Thread_2)
	for thread in threads:
		thread.join()

if __name__ == "__main__":
	multithreading()
