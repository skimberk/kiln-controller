import RPi.GPIO as GPIO
import time

GPIO.setup(16, GPIO.OUT)

while True:
	GPIO.output(16, GPIO.HIGH)
	time.sleep(1)
	GPIO.output(16, GPIO.LOW)
	time.sleep(1)