import PicoBotF_v03 as ThisPico
import utime

module_name = 'test_06_A_bucket_v02.py'

print (module_name, "starting")

bucket_servo = ThisPico.ThisBucketServo()

my_speed = 35
bucket_servo.move_to(new_position=80, speed=my_speed)
utime.sleep(1)
bucket_servo.move_to(new_position=90, speed=my_speed)
utime.sleep(1)
bucket_servo.move_to(new_position=155, speed=my_speed)
utime.sleep(1)
#bucket_servo.move_to(new_position=90, speed=my_speed)
utime.sleep(1)

print (module_name, "finished")
