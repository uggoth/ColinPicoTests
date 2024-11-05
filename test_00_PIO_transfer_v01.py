module_name = 'test_00_PIO_transfer_v01.py'
print (module_name, 'starting')

import rp2
from machine import Pin
import utime

@rp2.asm_pio()
def add_four():
    mov(x,invert(null))
    jmp(x_dec,'one')
    label('one')
    jmp(x_dec,'two')
    label('two')
    jmp(x_dec,'three')
    label('three')
    jmp(x_dec,'four')
    label('four')
    mov(y,invert(x))
    in_(y,32)
    push()

sm = rp2.StateMachine(0, add_four, freq=3000, set_base=Pin(25))

sm.active(1)
utime.sleep(1)
if sm.rx_fifo():
    r1 = sm.get()
else:
    r1 = None
sm.active(0)

print (r1)

print (module_name, 'finished')
