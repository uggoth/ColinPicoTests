module_name = 'test_00_A_onboard_led_flash_v01.py'

import utime
from machine import Pin

print (module_name, 'starting')

led = Pin(25, Pin.OUT)

for i in range(40):
    led.toggle()
    utime.sleep(0.15)

led.off()

print (module_name, 'finished')
