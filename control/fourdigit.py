import tm1637
import time

Display = tm1637.TM1637(CLK=21, DIO=20, brightness=1.0)
Display.Show([1, 2, 3, 4])

time.sleep(2)

Display.cleanup()