import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 1)
spi.max_speed_hz=8000000

while True:
	spi.writebytes([0, 0, 0, 0])
	print(spi.readbytes(4))
	time.sleep(0.5)

