module_name = 'test_07_B_individual_motors_v02.py'
#  run on stand to check rotation speed

import Kitronik_v05 as Kitronik
import utime

def move(motor, speed, rotation):
    motor.move(speed, rotation)
    utime.sleep(5)
    motor.stop()
    utime.sleep(1)

print (module_name, 'starting')

my_board = Kitronik.PicoRobotics.KitronikPicoRobotics()
utime.sleep(1)

# when correct, copy info to ThisDriveTrain
motors = [Kitronik.KitronikMotor('FRONT_LEFT', my_board, 4, 'r', 'f'),
          Kitronik.KitronikMotor('REAR_LEFT', my_board, 1, 'r', 'f'),
          Kitronik.KitronikMotor('FRONT_RIGHT', my_board, 3, 'f', 'r'),
          Kitronik.KitronikMotor('REAR_RIGHT', my_board, 2, 'f', 'r')]

speed = 100
rotation = 'c'
print ('Rotation should be', rotation)
for motor in motors:
    print (motor.name)
    move(motor, speed, rotation)

print (module_name, 'finished')
