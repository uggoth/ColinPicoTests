import PicoBotF_v02 as ThisPico
GPIO = ThisPico.GPIO
import utime

module_name = 'test_01_C_buttons_v01.py'
print (module_name, 'starting')

these_buttons = ThisPico.TheseButtons()

my_buttons = GPIO.Button.button_list

print ('NOTE: On Pico F the red button is hard-wired to RESET')

out_string = "List of buttons:\n"
for button in my_buttons:
    button.previous = 'UNKNOWN'
    out_string += '   ' + button.name + "\n"
print (out_string)

for i in range(100):
    utime.sleep(0.1)
    for button in my_buttons:
        current = button.get()
        if current != button.previous:
            print (button.name, current)
            button.previous = current

print (module_name, 'finished')
