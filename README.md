# Kiln Controller

Inspired by https://github.com/jbruce12000/kiln-controller

## Hardware I'm using

- Old Skutt K-1018: Craigslist
- High temperature Type K thermocouple (I got the 12 inch with 11 gauge wires): http://auberins.com/index.php?main_page=product_info&cPath=3&products_id=39
- 40a 240v contactor (with 240v coil): https://www.auberins.com/index.php?main_page=product_info&cPath=2_31&products_id=164
- Raspberry Pi Zero W: https://www.adafruit.com/product/3400 (although I bought mine from Microcenter)
- Small relay for driving the contactor: https://www.adafruit.com/product/3191
- Thermocouple amplifier: https://www.adafruit.com/product/269

## Setting up Raspberry Pi

I'm using a Raspberry Pi Zero W.

### Installing OS

1. Downloaded and unzipped Raspberry Pi OS (32-bit) Lite (kernel version 4.19) from here https://www.raspberrypi.org/downloads/raspberry-pi-os/
2. Flashed image to SD card using Etcher (the application is called balenaEtcher)
3. Removed and reinserted SD card then followed this tutorial to make it SSH-able via USB: https://desertbot.io/blog/ssh-into-pi-zero-over-usb (the `ssh-keygen` step didn't work, so I skipped right to SSH-ing which seemed to be ok)
4. Installed vim with `sudo apt-get install vim`
5. Installed git with `sudo apt-get install git`

### Setting up CircuitPython

Followed these instructions: https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi

1. I had to install `pip3`.
2. I didn't make `python3` default.
3. I enabled both I2C and SPI (even though I think technically I'll only be using SPI).

I ran the `blinkatest.py` script they included at the end, and it worked!

### Other necessary stuff

1. Installed drivers for thermocouple amplifier: `pip3 install adafruit-circuitpython-max31855`
2. Cloned this repository

### Running script on startup

I used cron: https://www.raspberrypi.org/documentation/linux/usage/cron.md

Ran `crontab -e` then added `@reboot python3 /home/pi/kiln-controller/control/temperature-readout.py &`

### Shutting down

```
sudo shutdown -h now
```