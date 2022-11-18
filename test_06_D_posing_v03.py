# Posing Test and Setup

import PicoBotF_v03 as ThisPico
import utime

module_name = 'test_06_D_posing_v03.py'

print (module_name, "starting")

bucket_servo = ThisPico.ThisBucketServo()
shoulder_servo = ThisPico.ThisShoulderServo()

my_arm = PicoBotF.ThisArm()

def do_pose(pose_id, speed):
    print (pose_id)
    my_arm.do_pose(pose_id, speed)

speed=100
do_pose('PARK', speed)
utime.sleep(1)
do_pose('UP', speed)
utime.sleep(2)
do_pose('DOWN', speed)
utime.sleep(2)
do_pose('PARK', speed)
utime.sleep(1)

print (module_name, "finished")
