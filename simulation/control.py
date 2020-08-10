from kiln import Kiln

kiln = Kiln()

for _ in range(600):
	if kiln.temperature < 100:
		kiln.on = True
	else:
		kiln.on = False

	kiln.tick()

	print('On' if kiln.on else 'Off', 'Kiln', kiln.temperature, 'Element', kiln.element_temperature)