import time
from random import randrange
import PIL.ImageFont
import luma.core.interface.serial
import luma.oled.device
import luma.core.render

serial = luma.core.interface.serial.spi(port=0, device=0)
device = luma.oled.device.ssd1351(serial)

fnt = PIL.ImageFont.truetype("SourceCodeVariable-Roman.ttf", 53)

counter = 0

while True:
	with luma.core.render.canvas(device) as draw:
		text_width, text_height = draw.textsize(str(counter), font=fnt)
		draw.text((128 - text_width, -17), str(counter), fill=(randrange(256), randrange(256), randrange(256)), font=fnt)
	counter = (counter + 1) % 5000

