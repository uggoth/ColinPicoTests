module_name = 'test_07_A_motor_identification_v01.py'
#  run on stand to check rotation speed

import Kitronik_v08 as Kitronik
import utime

print (module_name, 'starting')

utime.sleep(1)

# when correct, copy info to ThisPico.ThisDriveTrain
motors = [Kitronik.KitronikMotor('FRONT_LEFT', Kitronik.board, 4),
          Kitronik.KitronikMotor('REAR_LEFT', Kitronik.board, 1),
          Kitronik.KitronikMotor('FRONT_RIGHT', Kitronik.board, 3),
          Kitronik.KitronikMotor('REAR_RIGHT', Kitronik.board, 2)]

speed = 50

for motor in motors:
    print (motor.name)
    motor.clk(speed)
    utime.sleep(2)
    motor.stop()
    utime.sleep(1)

for motor in motors:
    motor.close()

print (module_name, 'finished')
