from kiln import Kiln
from pid import PID

kiln = Kiln()
pid = PID(1, 0.0001, 1)

last_temperature = 0
target = 300

for x in range(300):
	slope = kiln.temperature - last_temperature
	error = target - kiln.temperature

	if error > 0 and (target - (kiln.temperature + 10 * slope)) > 0:
		kiln.on = True
	else:
		kiln.on = False

	last_temperature = kiln.temperature

	kiln.tick()

	print('On' if kiln.on else 'Off', 'Kiln', kiln.temperature, 'Element', kiln.element_temperature)
	pid_out = pid.update(kiln.temperature, target, x)

	if pid_out[0] is not None:
		print(pid_out)
		print(pid_out[0] + pid_out[1] + pid_out[2])