class PID:
	def __init__(self, kp, ki, kd, min_out, max_out):
		self.kp = kp
		self.ki = ki
		self.kd = kd

		self.min_out = min_out
		self.max_out = max_out

		self.last_error = None
		self.last_time = None
		self.integral = 0

	def update(self, value, target, time):
		error = target - value

		if self.last_error is None:
			self.last_error = error
			self.last_time = time
			return None

		dt = time - self.last_time

		# Use ki when calculating integral to prevent massive growth
		# and keep output from jumping when changing ki
		self.integral += self.ki * error * dt
		derivative = (error - self.last_error) / dt

		# multiplied by ki above (because multiplication is distributive)
		output = self.kp * error + self.integral + self.kd * derivative

		# Clamp integral and output
		# Clamping integral reduces windup
		self.integral = min(max(self.integral, self.min_out), self.max_out)
		output = min(max(output, self.min_out), self.max_out)

		self.last_time = time
		self.last_error = error

		return output
