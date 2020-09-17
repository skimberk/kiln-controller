import all_inclusive

temp = None
stage = 0
counter = 0

# Overwrite temp/stage/counter in case of program restart
# temp = 0
# stage = 0
# counter = 0

def callback(thermocouple_temp):
	global stage
	global counter
	global temp

	if temp is None:
		temp = thermocouple_temp
	elif temp <= 300 and stage == 0:
		temp += 2
	elif temp <= 1771 and stage == 0:
		temp += 4
	elif thermocouple_temp >= 1770 and stage == 0:
		stage = 1
	elif temp <= 1971 and stage == 1:
		temp += 0.75
	elif temp >= 1971 and stage == 1:
		stage = 2
	elif stage == 2:
		temp = 1971
		counter += all_inclusive.period
		if counter >= 60 * 10:
			stage = 3
			counter = 0
	elif stage == 3:
		temp = 0

	print(temp, thermocouple_temp)

	return temp

all_inclusive.callback = callback
all_inclusive.start()

