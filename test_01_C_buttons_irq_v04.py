module_name = 'test_01_C_buttons_irq_v02.py'

import ThisPico_V_V41 as ThisPico
GPIO = ThisPico.GPIO
import machine
import utime

print (module_name, 'starting')

button_press_counts = {}
trigger_criterion = machine.Pin.IRQ_FALLING

def ir_callback_counting(my_pin):
    global button_press_counts, my_ids, trigger_criterion
    my_pin.irq(None)
    button_press_counts[my_ids[id(my_pin)]] += 1
    utime.sleep_ms(300)  #  debounce
    my_pin.irq(my_callback, trigger=trigger_criterion)
    
def ir_callback_logging(my_pin):
    global my_ids, my_callback, trigger_criterion
    my_pin.irq(None)
    print (my_ids[id(my_pin)], my_pin.value())
    utime.sleep_ms(500)  #  debounce
    my_pin.irq(my_callback, trigger=trigger_criterion)

my_callback = ir_callback_counting
#my_callback = ir_callback_logging

my_blue_button = ThisPico.BlueButton()
my_yellow_button = ThisPico.YellowButton()
my_oscilloscope = ThisPico.Oscilloscope()
my_buttons = GPIO.Button.button_list
my_ids = ThisPico.GPIO.GPIO.ids
for button in my_buttons:
    button_press_counts[my_ids[id(button.pin)]] = 0
    button.pin.irq(my_callback, trigger=trigger_criterion)

out_string = "\nList of all buttons:\n"
for button in GPIO.Button.button_list:
    out_string += '   ' + button.name + "\n"
print (out_string)

utime.sleep(5)

for button in my_buttons:
    button.pin.irq(None)
if my_callback == ir_callback_counting:
    for button in my_buttons:
        print (button.name, 'pressed', button_press_counts[my_ids[id(button.pin)]], 'times')

print (' ')
print (module_name, 'finished')
