module_name = 'test_01_C_buttons_loop_v03.py'

import ThisPico_V_V41 as ThisPico
GPIO = ThisPico.GPIO
import utime

print (module_name, 'starting')

my_blue_button = ThisPico.BlueButton()
my_yellow_button = ThisPico.YellowButton()
my_buttons = GPIO.Button.button_list

out_string = "List of buttons in :\n"
for button in my_buttons:
    button.previous = 'UNKNOWN'
    out_string += '   ' + button.name + "\n"
print (out_string)

for i in range(1000):
    utime.sleep_ms(20)  #  debounce
    for button in my_buttons:
        current = button.get()
        if current != button.previous:
            print (button.name, current)
            button.previous = current

print (module_name, 'finished')
