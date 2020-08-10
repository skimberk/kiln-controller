from kiln import Kiln

kiln = Kiln()

for _ in range(600):
	if kiln.temperature < 500:
		kiln.on = True
	else:
		kiln.on = False

	kiln.tick()
	print(kiln.on, kiln.temperature)