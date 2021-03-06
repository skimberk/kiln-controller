import atexit
import time
import board
import busio
import digitalio
import adafruit_max31855
import RPi.GPIO as GPIO
from pid import PID

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D5)

max31855 = adafruit_max31855.MAX31855(spi, cs)

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)

#goal_temperature = max31855.temperature * 9 / 5 + 32
goal_temperature = 1911
period = 10

pid = PID(0.02, 0.00005, 0, 0, 1)
last_good_temperature = 0

def cleanup():
	GPIO.output(16, GPIO.LOW)

atexit.register(cleanup)

while True:
	try:
		tempC = max31855.temperature

		if tempC == 0:
			raise RuntimeError('temperature is exactly zero, probably an issue')
	except RuntimeError:
		print('runtime error')
	else:
		tempF = tempC * 9 / 5 + 32
		print(tempF)

		last_good_temperature = tempF

	pid_out = pid.update(last_good_temperature, goal_temperature, time.time())
	print(goal_temperature)
	print(pid_out)


	if pid_out is None:
		time.sleep(period)
	else:
		time_on = period * pid_out
		time_off = period - time_on

		if time_off > 0:
			GPIO.output(16, GPIO.LOW)
			time.sleep(time_off)

		if time_on > 0:
			GPIO.output(16, GPIO.HIGH)
			time.sleep(time_on)
	
	if goal_temperature < 1800:
		goal_temperature += 4
	elif goal_temperature < 1971:
		goal_temperature += 0.75
#	else:
#		break
		
