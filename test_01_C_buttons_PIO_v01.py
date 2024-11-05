module_name = 'test_01_C_buttons_PIO_v01.py'
print (module_name, 'starting')

import ThisPico_V_V41 as ThisPico
GPIO = ThisPico.GPIO
from machine import Pin
import utime
import rp2

my_blue_button = ThisPico.BlueButton()
my_yellow_button = ThisPico.YellowButton()
my_buttons = GPIO.Button.button_list
my_ids = ThisPico.GPIO.GPIO.ids

@rp2.asm_pio()
def measure():
    wrap_target()
    wait(1,pin,0)  #  don't start in the middle of a pulse
    wait(0,pin,0)
    mov(x,invert(null))
    label('loop')    
    jmp(x_dec,'pin_off') #  Note: x will never be zero. We just want the decrement
    nop()  
    label('pin_off')
    jmp(pin, 'loop')
    mov(isr,invert(x))
    push(noblock)
    wrap()

sm_hertz = 100000

sm0_pin = Pin(my_blue_button.pin_no, Pin.IN, Pin.PULL_UP)  # Pin.PULL_DOWN   Pin.PULL_UP   None
sm0 = rp2.StateMachine(0, measure, freq=sm_hertz, in_base=sm0_pin, jmp_pin=sm0_pin)
sm0.active(1)

sm1_pin = Pin(my_yellow_button.pin_no, Pin.IN, Pin.PULL_UP)  # Pin.PULL_DOWN   Pin.PULL_UP   None
sm1 = rp2.StateMachine(1, measure, freq=sm_hertz, in_base=sm1_pin, jmp_pin=sm1_pin)
sm1.active(1)

for i in range(9000):  #  arbitrary test duration
    utime.sleep_ms(1)  #  debounce
    if sm0.rx_fifo():
        y = sm0.get()
        print ('blue button',i,y)
    if sm1.rx_fifo():
        y = sm1.get()
        print ('yellow button',i,y)

sm0.active(0)
sm1.active(0)

print ('\n', module_name, 'finished')
