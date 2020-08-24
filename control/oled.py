import time
import PIL.ImageFont
import luma.core.interface.serial
import luma.oled.device
import luma.core.render
import max31855

serial = luma.core.interface.serial.spi(port=0, device=0)
device = luma.oled.device.ssd1351(serial)

fnt_53 = PIL.ImageFont.truetype("SourceCodeVariable-Roman.ttf", 53)
fnt_24 = PIL.ImageFont.truetype("SourceCodeVariable-Roman.ttf", 20)

thermocouple = max31855.MAX31855(0, 1)

while True:
	temp_f = int(thermocouple.temperature * 9 / 5 + 32)
	with luma.core.render.canvas(device) as draw:
		text_width, text_height = draw.textsize(str(temp_f), font=fnt_53)
		draw.text((128 - text_width, -17), str(temp_f), fill=(255, 255, 255), font=fnt_53)
		draw.text((0, 37), 'Goal 2350', fill=(0, 255, 0), font=fnt_24)
		draw.text((0, 57), 'Duty 93.7%', fill=(0, 0, 255), font=fnt_24)
		draw.text((0, 77), 'Time ' + time.strftime('%I:%M'), fill=(255, 128, 0), font=fnt_24)
		draw.text((0, 97), 'Temp ' + str(int(thermocouple.reference_temperature * 9 / 5 + 32)) + '°', fill=(0, 128, 255), font=fnt_24)

