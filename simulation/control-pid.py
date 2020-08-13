from kiln import Kiln
from pid import PID

kiln = Kiln()
pid = PID(0.02, 0.00005, 0, 0, 1)

target = 300
period = 10

for tick_num in range(1900):
	pid_out = pid.update(kiln.temperature, target, tick_num)

	if pid_out is not None:
		ticks_on = round(period * pid_out)
		ticks_off = period - ticks_on

		if ticks_off > 0:
			kiln.on = False
			kiln.multi_tick(ticks_off)

		if ticks_on > 0:
			kiln.on = True
			kiln.multi_tick(ticks_on)

		print('Kiln', kiln.temperature, 'Element', kiln.element_temperature, 'Duty cycle', ticks_on / period)

	if tick_num == 100:
		target = 600
	elif tick_num == 500:
		target = 1080
	elif tick_num >= 1200 and tick_num < 1500:
		target -= 2
		print('Target', target)
	elif tick_num >= 1500 and tick_num < 1700:
		target += 2
		print('Target', target)
	