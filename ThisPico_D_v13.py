module_name = 'ThisPico_D_v13.py'

import GPIOPico_v25 as GPIO
ColObjects = GPIO.ColObjects
import Kitronik_v13 as Kitronik
import machine

class ThisVolts(GPIO.Volts):
    def __init__(self):
        super().__init__('VIN',29)


class ThisHCSR04(GPIO.HCSR04):
    def __init__(self):
        super().__init__(name='FRONT_US',
                 trigger_pin_no=16,
                 echo_pin_no=17,
                 critical_distance=100.0)

class TheseIRSensors():
    def __init__(self, front_left_callback, front_right_callback):
        self.front_left = GPIO.IRSensor('Front Left', 19, callback=front_left_callback)
        self.front_right = GPIO.IRSensor('Front Right', 20, callback=front_right_callback)
        self.rear_centre = GPIO.IRSensor('Rear Centre', 2)
        self.ir_list = [self.front_left, self.front_right, self.rear_centre]
    def close(self):
        for ir in self.ir_list:
            ir.close()

class TheseSwitches():
    def __init__(self):
        #  self.DIP_1 = GPIO.Switch('DIP_1',13)    --- used by buzzer ---
        self.DIP_2 = GPIO.Switch('DIP_2',12)
        self.DIP_3 = GPIO.Switch('DIP_3',11)
        self.switch_list = [self.DIP_2,self.DIP_3]
    def close(self):
        for switch in self.switch_list:
            switch.close()

class TheseButtons():
    def __init__(self):
        self.yellow_button = GPIO.Button('Yellow Button', 14)
        self.red_button = GPIO.Button('Red Button', 15)
        self.button_list = [self.yellow_button, self.red_button]
    def close(self):
        for button in self.button_list:
            button.close()

class ThisBuzzer(GPIO.Buzzer):
    def __init__(self):
        self.DIP_1 = GPIO.Switch('DIP_1',13)  
        super().__init__('Buzzer', 18, self.DIP_1)
    def close(self):
        self.DIP_1.close()
        super().close()

class ThisLeftHeadlight(GPIO.RGBLED):
    def __init__(self):
        red_led = GPIO.LED('LEFT_RED',21)
        green_led = GPIO.LED('LEFT_GREEN',5)
        blue_led = GPIO.LED('LEFT_BLUE',3)
        super().__init__("Left Headlight", red_led, green_led, blue_led)

class ThisRightHeadlight(GPIO.RGBLED):
    def __init__(self):
        red_led = GPIO.LED('RIGHT_RED',22)
        green_led = GPIO.LED('RIGHT_GREEN',10)
        blue_led = GPIO.LED('RIGHT_BLUE',6)
        super().__init__("Right Headlight", red_led, green_led, blue_led)

class ThisDriveTrain(ColObjects.DriveTrain):
    def __init__(self, board_object):
        self.left_side = ColObjects.Side('Left Side', 'L', [
            Kitronik.KitronikMotor('Left Motor', board_object, 1)])
        self.right_side = ColObjects.Side('Right Side', 'R', [
            Kitronik.KitronikMotor('Right Motor', board_object, 2)])
        super().__init__('ThisDriveTrain', self.left_side, self.right_side)
        self.last_spin = ''
        self.millimetre_factor = 140
        self.degree_factor = 155
        self.speed_exponent = 0.5

class ThisDriveTrainWithHeadlights(ColObjects.DriveTrainWithHeadlights):
    def __init__(self, board_object, left_headlight, right_headlight):
        self.board_object = Kitronik.Kitronik.board_object
        self.left_headlight = left_headlight
        self.right_headlight = right_headlight
        self.left_side = ColObjects.Side('Left Side', 'L', [
            Kitronik.KitronikMotor('Left Motor', board_object, 1)])
        self.right_side = ColObjects.Side('Right Side', 'R', [
            Kitronik.KitronikMotor('Right Motor', board_object, 2)])
        super().__init__('ThisDriveTrain', self.left_side, self.right_side, self.left_headlight, self.right_headlight)
        self.last_spin = ''
        self.millimetre_factor = 140
        self.degree_factor = 155
        self.speed_exponent = 0.5

class ThisDriveTrainPlus(ColObjects.DriveTrainPlus):
    def __init__(self):
        self.board_object = Kitronik.Kitronik('OnlyBoard')
        self.left_side = ColObjects.Side('Left Side', 'L', [
            Kitronik.KitronikMotor('Left Motor', self.board_object, 1)])
        self.right_side = ColObjects.Side('Right Side', 'R', [
            Kitronik.KitronikMotor('Right Motor', self.board_object, 2)])
        self.left_headlight = ThisLeftHeadlight()
        self.right_headlight = ThisRightHeadlight()
        self.my_irs = TheseIRSensors(None, None)
        self.front_left_ir = self.my_irs.front_left
        self.front_right_ir = self.my_irs.front_right
        self.rear_left_ir = self.my_irs.rear_centre
        self.rear_right_ir = self.my_irs.rear_centre
        super().__init__('ThisDriveTrain', self.left_side, self.right_side,
                         self.left_headlight, self.right_headlight,
                         self.front_left_ir, self.front_right_ir, self.rear_left_ir, self.rear_right_ir)
        self.last_spin = ''
        self.millimetre_factor = 140
        self.degree_factor = 155
        self.speed_exponent = 0.5

class ThisShoulderServo(Kitronik.Servo):
    def __init__(self, board_object):
        super().__init__('Shoulder Servo',
                 board_object,
                 servo_no=5,
                 max_rotation=180,
                 min_rotation=0)
    def up(self, speed=50):
        self.move_to(new_position=105, speed=speed)
    def down(self, speed=55):
        self.move_to(new_position=75, speed=speed)

uart_tx = GPIO.Reserved('UART TX', 'OUTPUT', 0)
uart_rx = GPIO.Reserved('UART RX', 'INPUT', 1)
smps_mode = GPIO.Reserved('SMPS Mode', 'OUTPUT', 23)
vbus_monitor = GPIO.Reserved('VBUS Monitor','INPUT',24)
onboard_led = machine.Pin(25, machine.Pin.OUT)
onboard_volts = GPIO.Volts('Onboard Voltmeter', 29)
    
#####  For testing compilation and GPIO clashes
if __name__ == "__main__":
    print (module_name, '\n')
    #board_object = Kitronik.Kitronik('The Only Board')
    #left_headlight = ThisLeftHeadlight()
    #right_headlight = ThisRightHeadlight()
    #drive_train = ThisDriveTrainPlus(board_object,left_headlight,right_headlight)
    drive_train = ThisDriveTrainPlus()
    shoulder_servo = ThisShoulderServo(drive_train.board_object)
    buttons = TheseButtons()
    switches = TheseSwitches()
    buzzer = ThisBuzzer()
    #ir_sensors = TheseIRSensors()
    hcsr04 = ThisHCSR04()
    print ('----- GPIO pin allocations -----')
    print (GPIO.GPIO.str_allocated())
    print ('----- Kitronik servo allocations -----')
    print (drive_train.board_object.str_servo_list())
    print ('----- Kitronik motor allocations -----')
    print (drive_train.board_object.str_motor_list())
