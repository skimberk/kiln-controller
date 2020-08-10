class Kiln:
	max_temperature = 2300

	def __init__(self):
		self.temperature = 0
		self.on = False

	def tick(self):
		new_temperature = self.temperature
		new_temperature -= self.temperature / self.max_temperature

		if self.on:
			new_temperature += (self.max_temperature - self.temperature) / self.max_temperature + 1

		self.temperature = new_temperature

if __name__ == '__main__':
	kiln = Kiln()
	kiln.on = True

	for _ in range(2000):
		print(kiln.temperature)
		kiln.tick()
