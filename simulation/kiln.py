class Kiln:
	max_element_temperature = 2600

	def __init__(self):
		self.temperature = 0
		self.element_temperature = 0
		self.on = False

	def tick(self):
		new_temperature = self.temperature
		new_temperature -= 0.001 * self.temperature

		new_element_temperature = self.element_temperature
		new_element_temperature += 0.1 * (self.temperature - self.element_temperature)

		if self.on:
			new_element_temperature += 20  * (1 - self.element_temperature / self.max_element_temperature)

		new_temperature += 0.01 * (self.element_temperature - self.temperature)

		self.temperature = new_temperature
		self.element_temperature = new_element_temperature

if __name__ == '__main__':
	kiln = Kiln()
	kiln.on = True

	for _ in range(1000):
		print('Kiln:', kiln.temperature)
		print('Element: ', kiln.element_temperature)
		print()

		kiln.tick()
