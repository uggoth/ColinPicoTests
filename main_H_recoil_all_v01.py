module_name = 'main_H_recoil_all_v01.py'

import ThisPico_F_v11 as ThisPico
import utime
import sys

print (module_name, 'starting')

def get_pose(position):
    if position < -50:
        return 'DOWN'
    elif position < 0:
        return 'SCOOP'
    elif position < 50:
        return 'CARRY'
    else:
        return 'DUMP'

def close_down():
    my_knob.close()
    my_arm.close()
    my_remote_control.close()
    my_drive_train.close()
    board_object.close()

board_object = ThisPico.Kitronik.Kitronik('The Only Board')
left_headlight = ThisPico.ThisLeftHeadlight()
right_headlight = ThisPico.ThisRightHeadlight()
my_drive_train = ThisPico.ThisDriveTrainWithHeadlights(board_object, left_headlight, right_headlight)
my_remote_control = ThisPico.ThisRemoteControlWithHeadlights(my_drive_train, left_headlight, right_headlight)
my_knob = my_remote_control.knob
my_arm = ThisPico.ThisArm(board_object)
buttons = ThisPico.TheseButtons()
yellow_button = buttons.yellow_button
my_irs = ThisPico.TheseIRSensors()
onboard_led = ThisPico.onboard_led

if not yellow_button.wait(100, onboard_led):
    print ('Tired of waiting')
    close_down()
    sys.exit(1)

utime.sleep_ms(1000)
previous_pose = 'UNKNOWN'

while True:
    utime.sleep_ms(10)
    my_remote_control.drive()
    position = my_knob.get()
    pose = get_pose(position)
    if pose != previous_pose:
        previous_pose = pose
        my_arm.do_pose(pose)
    if yellow_button.get() == 'ON':
        break
    for ir in my_irs.ir_list:
        if ir.get() != 'ON':
            if ir.name[0:4] == 'FRON':
                my_drive_train.rev(speed=50, millimetres=70)
                if ir.name[6:10] == 'LEFT':
                    my_drive_train.spr(90,20)
                else:
                    my_drive_train.spl(90,20)
            else:
                my_drive_train.fwd(speed=50, millimetres=70)
                if ir.name[5:9] == 'LEFT':
                    my_drive_train.spl(90,20)
                else:
                    my_drive_train.spr(90,20)

close_down()
print (module_name, 'finished')
