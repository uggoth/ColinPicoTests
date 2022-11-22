module_name = 'main_H_recoil_all_v01.py'

import ThisPico_F_v10 as ThisPico
import utime

print (module_name, 'starting')

board_object = ThisPico.Kitronik.Kitronik('The Only Board')
my_drive_train = ThisPico.ThisDriveTrain(board_object)
my_remote_control = ThisPico.ThisRemoteControl(my_drive_train)
my_knob = my_remote_control.knob
my_arm = ThisPico.ThisArm(board_object)
buttons = ThisPico.TheseButtons()
yellow_button = buttons.yellow_button
my_irs = ThisPico.TheseIRSensors()

def get_pose(position):
    if position < -50:
        return 'DOWN'
    elif position < 0:
        return 'SCOOP'
    elif position < 50:
        return 'CARRY'
    else:
        return 'DUMP'

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
            else:
                my_drive_train.fwd(speed=50, millimetres=70)

my_knob.close()
my_arm.close()
my_remote_control.close()
my_drive_train.close()
board_object.close()

print (module_name, 'finished')
