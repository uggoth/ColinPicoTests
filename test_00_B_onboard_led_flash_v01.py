module_name = 'test_00_B_onboard_led_flash_v01.py'

import PicoBotF_v02 as ThisPico
import utime

print (module_name, 'starting')

my_led = ThisPico.OnboardLED

for i in range(40):
    my_led.toggle()
    utime.sleep(0.15)
    
my_led.off()

print (module_name, 'finished')
