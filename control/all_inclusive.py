import time
import asyncio
import os
import atexit
import signal

import PIL.ImageFont
import luma.core.interface.serial
import luma.oled.device
import luma.core.render
import RPi.GPIO

import max31855
from pid import PID

serial = luma.core.interface.serial.spi(port=0, device=0)
device = luma.oled.device.ssd1351(serial)

thermocouple = max31855.MAX31855(0, 1)

RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(16, RPi.GPIO.OUT)

file_dir = os.path.dirname(os.path.realpath(__file__))
font_path = os.path.join(file_dir, "SourceCodeVariable-Roman.ttf")

fnt_53 = PIL.ImageFont.truetype(font_path, 53)
fnt_24 = PIL.ImageFont.truetype(font_path, 20)

pid = PID(0.02, 0.00005, 0, 0, 1)
period = 10

last_good_thermocouple_temp = 0
last_good_outside_temp = 0

goal_temperature = 0
duty_cycle = 0

callback = None

def per_hour(degrees):
	return degrees / (60 * 60 / period)

def c_to_f(c):
	return c * 9 / 5 + 32

def update_temperatures():
	global last_good_thermocouple_temp
	global last_good_outside_temp

	try:
		thermocouple_temp_c = thermocouple.temperature

		if thermocouple_temp_c == 0:
			raise RuntimeError('temperature is exactly zero, probably an issue')

		last_good_thermocouple_temp = c_to_f(thermocouple_temp_c)
	except RuntimeError:
		print('runtime error (thermocouple)')

	try:
		outside_temp_c = thermocouple.reference_temperature

		if outside_temp_c == 0:
			raise RuntimeError('temperature is exactly zero, probably an issue')

		last_good_outside_temp = c_to_f(outside_temp_c)
	except RuntimeError:
		print('runtime error (outside)')

def update_display():
	with luma.core.render.canvas(device) as draw:
		thermocouple_temp_str = str(int(last_good_thermocouple_temp))
		outside_temp_str = str(int(last_good_outside_temp))
		goal_temp_str = str(int(goal_temperature))
		duty_str = str(int(duty_cycle * 1000) / 10)
		time_str = time.strftime('%I:%M')

		text_width, text_height = draw.textsize(thermocouple_temp_str, font=fnt_53)
		draw.text((128 - text_width, -17), thermocouple_temp_str, fill=(255, 255, 255), font=fnt_53)
		draw.text((0, 37), 'Goal ' + goal_temp_str, fill=(0, 255, 0), font=fnt_24)
		draw.text((0, 57), 'Duty ' + duty_str + '%', fill=(0, 0, 255), font=fnt_24)
		draw.text((0, 77), 'Time ' + time_str, fill=(255, 128, 0), font=fnt_24)
		draw.text((0, 97), 'Temp ' + outside_temp_str + '°', fill=(0, 128, 255), font=fnt_24)

async def update_loop():
	while True:
		update_temperatures()
		update_display()
		await asyncio.sleep(1)

async def duty_loop():
	global goal_temperature
	global duty_cycle

	while True:
		if callback is None:
			await asyncio.sleep(1)
		else:
			update_temperatures()
			goal_temperature = callback(last_good_thermocouple_temp)
	
			pid_out = pid.update(last_good_thermocouple_temp, goal_temperature, time.time())
	
			if pid_out is None:
				await asyncio.sleep(period)
			else:
				duty_cycle = pid_out
	
				time_on = period * duty_cycle
				time_off = period - time_on
	
				if time_off > 0:
					RPi.GPIO.output(16, RPi.GPIO.LOW)
					await asyncio.sleep(time_off)
	
				if time_on > 0:
					RPi.GPIO.output(16, RPi.GPIO.HIGH)
					await asyncio.sleep(time_on)

loop = asyncio.get_event_loop()
loop.create_task(update_loop())
loop.create_task(duty_loop())

def start():
	loop.run_forever()

def cleanup():
	device.cleanup()
	RPi.GPIO.output(16, RPi.GPIO.LOW)

atexit.register(cleanup)
signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGINT, cleanup)
