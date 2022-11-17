module_name = 'test_07_C_sides.py'

import PicoBotF_v03 as ThisPico
import utime

def move(side, speed, rotation):
    side.move(speed, rotation)
    utime.sleep(1)
    side.stop()
    
print (module_name, 'starting')

speed = 55

drive_train = ThisPico.ThisDriveTrain()

drive_train.left_side.move(55,'a')
utime.sleep(1)
drive_train.left_side.stop()

utime.sleep(2)

drive_train.right_side.move(55,'a')
utime.sleep(1)
drive_train.right_side.stop()

print (module_name, 'finished')
