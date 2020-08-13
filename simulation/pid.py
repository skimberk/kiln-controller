class PID:
	def __init__(self, k_p, k_i, k_d):
		self.k_p = k_p
		self.k_i = k_i
		self.k_d = k_d

		self.last_value = None
		self.last_error = None
		self.last_time = None
		self.integral = 0

	def update(self, value, target, time):
		error = target - value

		if self.last_value is not None:
			self.integral += (time - self.last_time) * (error + self.last_error) / 2

			p = self.k_p * error
			i = self.k_i * self.integral
			d = self.k_d * (error - self.last_error) / (time - self.last_time)

			self.last_value = value
			self.last_time = time
			self.last_error = error

			return [p, i, d]
		else:
			self.last_value = value
			self.last_time = time
			self.last_error = error

			return [None, None, None]
