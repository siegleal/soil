import time
from board import SCL, SDA

import busio
from adafruit_seesaw.seesaw import Seesaw

class Soil:
    def __init__(self):

        self.i2c_bus = busio.I2C(SCL, SDA)

        self.ss = Seesaw(self.i2c_bus, addr=0x36)

    def read(self):

        touch = self.ss.moisture_read()

        temp = self.ss.get_temp()
        return touch, temp


