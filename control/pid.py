class PID:
	def __init__(self, kp, ki, kd):
		self.kp = kp
		self.ki = ki
		self.kd = kd

		self.last_error = None
		self.last_time = None
		self.integral = 0

	def update(self, value, target, time):
		error = target - value

		if self.last_value is not None:
			dt = time - self.last_time
			self.integral += error * dt
			derivative = (error - self.last_error) / dt

			self.last_time = time
			self.last_error = error

			return kp * error + ki * self.integral + kd * derivative
		else:
			self.last_value = value
			self.last_time = time
			self.last_error = error

			return None
