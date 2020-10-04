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

	# Based on "fast" cone 04 bisque schedule here:
	# https://community.ceramicartsdaily.org/topic/16636-firing-question/
	if temp is None:
		temp = thermocouple_temp
	elif temp <= 250:
		temp += all_inclusive.per_hour(120)
	elif temp <= 1000:
		temp += all_inclusive.per_hour(300)
	elif temp <= 1100:
		temp += all_inclusive.per_hour(150)
	elif temp <= 1695:
		temp += all_inclusive.per_hour(180)
	elif temp <= 1945:
		temp += all_inclusive.per_hour(108)
	else:
		if counter >= 60 * 10:
			temp = 0
		else:
			counter += all_inclusive.period
			temp = 1945

	print(temp, thermocouple_temp)

	return temp

all_inclusive.callback = callback
all_inclusive.start()

