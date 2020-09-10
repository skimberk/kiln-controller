import all_inclusive

temp = None
stage = 0
counter = 0

def callback(thermocouple_temp):
	global stage
	global counter
	global temp

	if temp is None:
		temp = 1765
	elif temp <= 1771 and stage == 0:
		temp += 4
	elif thermocouple_temp >= 1770 and stage == 0:
		stage = 1
	elif temp <= 1971 and stage == 1:
		temp += 0.75
	elif temp >= 1971 and stage == 1:
		stage = 2
	elif stage == 2:
		counter += all_inclusive.period
		if counter >= 60 * 15:
			stage = 3
	elif stage == 3:
		temp = 0

	return temp

all_inclusive.callback = callback
all_inclusive.start()

