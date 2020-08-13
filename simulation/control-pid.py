from kiln import Kiln
from pid import PID

kiln = Kiln()
pid = PID(1, 0.00001, 0.1)

target = 300

for x in range(1000):
	pid_out = pid.update(kiln.temperature, target, x)

	if pid_out[0] is not None:
		print(pid_out)

		pid_sum = pid_out[0] + pid_out[1] + pid_out[2]
		print(pid_sum)

		pid_transformed = 1 / (1 + 1.5 ** (-pid_sum))

		kiln.on = (pid_transformed >= 0.5)

	print('On' if kiln.on else 'Off', 'Kiln', kiln.temperature, 'Element', kiln.element_temperature)

	kiln.tick()
	