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
	elif temp <= 200:
		temp += 0.5
	else:
		temp = 200

	print(temp, thermocouple_temp)

	return temp

all_inclusive.callback = callback
all_inclusive.start()

