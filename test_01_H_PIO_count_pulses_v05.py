module_name = 'test_01_H_PIO_count_pulses_v05.py'
print (module_name, 'starting')
import utime
import rp2
from machine import Pin

@rp2.asm_pio()
def measure():
    mov(x,invert(null))  #  No increment command, so must decrement, so must start high
    wrap_target()
    wait(1,pin,0)  #  if PULL_DOWN then wait(1,pin,0)
    nop()[31]  #  slight debounce in case pulse wave not perfectly square
    #             NOTE: needs a LOT more debounce for physical button if you really cared
    wait(0,pin,0)  #  if PULL_DOWN then wait(0,pin,0)
    jmp(x_dec,'pin_off') #  Note: x will never be zero. We just want the decrement
    label('pin_off')
    mov(y,invert(x))
    wrap()  #  for clarity. Not actually needed

sm_hertz = 1000000  #  should not be critical

sm0_start_pin = Pin(17, Pin.IN, Pin.PULL_UP)  #  button for compare. NOT accurate
sm0 = rp2.StateMachine(0, measure, freq=sm_hertz, in_base=sm0_start_pin)

sm1_start_pin = Pin(18, Pin.IN, Pin.PULL_UP)  #  pulses from signal generator or test motor
sm1 = rp2.StateMachine(1, measure, freq=sm_hertz, in_base=sm1_start_pin)

sm_list = [sm0,sm1]

for sm in sm_list:
    sm.active(1)

def read_sm(sm):
    sm.active(0)
    sm.exec('in_(y,32)')
    sm.exec('push(noblock)')
#
#    NOTE: pulses will be missed while this runs, so best to avoid loops
#          unless there will definitely be some data there
#    result = []
#    for j in range(sm.rx_fifo()):
#        y = sm.get()
#        result.append(y)
#
#    NOTE: to reset counter to zero after each read:
#    sm.exec('mov(x,invert(null))')
#
    result = sm.get()
    sm.active(1)
    return result

loops = 3

for i in range(loops):
    utime.sleep(1)
    for j in range(len(sm_list)):
        print (i,j,read_sm(sm_list[j]))

for sm in sm_list:
    sm.active(0)

print (module_name, 'finished')