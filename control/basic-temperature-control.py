import tm1637
import time
import atexit
import board
import busio
import digitalio
import adafruit_max31855

Display = tm1637.TM1637(CLK=21, DIO=20, brightness=1.0)

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D5)

max31855 = adafruit_max31855.MAX31855(spi, cs)

def cleanup():
	Display.cleanup()

atexit.register(cleanup)

goal_temperature = 652
last_temperature = 0

while True:
	try:
		tempC = max31855.temperature
	except RuntimeError:
		print('runtime error')
		# Display.Show([0, 0, 0, 0])
	else:
		tempF = tempC * 9 / 5 + 32
		print(tempF)

		slope = tempF - last_temperature
		error = goal_temperature - tempF

		if error > 0 and (goal_temperature - (tempF + 10 * slope)) > 0:
			GPIO.output(16, GPIO.HIGH)
		else:
			GPIO.output(16, GPIO.LOW)

		last_temperature = tempF

		# tempInt = int(tempF)
		# print(tempInt)

		# Display.Show([
		# 	(tempInt // 1000) % 10,
		# 	(tempInt // 100) % 10,
		# 	(tempInt // 10) % 10,
		# 	tempInt % 10,
		# ])

	time.sleep(3.0)
