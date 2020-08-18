import time
from random import randrange
from PIL import ImageFont
from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1351

serial = spi(port=0, device=0)
device = ssd1351(serial)

fnt = ImageFont.truetype("SourceCodeVariable-Roman.ttf", 53)

counter = 0

while True:
	with canvas(device) as draw:
		text_width, text_height = draw.textsize(str(counter), font=fnt)
		draw.text((128 - text_width, -17), str(counter), fill=(randrange(256), randrange(256), randrange(256)), font=fnt)
	counter = (counter + 1) % 5000
	time.sleep(0.1)

