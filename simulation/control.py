from kiln import Kiln

kiln = Kiln()

last_temperature = 0
target = 1000

for _ in range(1800):
	slope = kiln.temperature - last_temperature
	error = target - kiln.temperature

	if error > 0 and (target - (kiln.temperature + 10 * slope)) > 0:
		kiln.on = True
	else:
		kiln.on = False

	last_temperature = kiln.temperature

	kiln.tick()

	print('On' if kiln.on else 'Off', 'Kiln', kiln.temperature, 'Element', kiln.element_temperature)