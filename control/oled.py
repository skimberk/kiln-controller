import time
import PIL.ImageFont
import luma.core.interface.serial
import luma.oled.device
import luma.core.render
import max31855

serial = luma.core.interface.serial.spi(port=0, device=0)
device = luma.oled.device.ssd1351(serial)

fnt = PIL.ImageFont.truetype("SourceCodeVariable-Roman.ttf", 53)

thermocouple = max31855.MAX31855(0, 1)

while True:
	temp_f = int(thermocouple.temperature * 9 / 5 + 32)
	with luma.core.render.canvas(device) as draw:
		text_width, text_height = draw.textsize(str(temp_f), font=fnt)
		draw.text((128 - text_width, -17), str(temp_f), fill=(255, 255, 255), font=fnt)

