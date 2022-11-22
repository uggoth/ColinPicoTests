import RemoteControl_v16 as RemoteControl
GPIO = RemoteControl.GPIO
ColObjects = RemoteControl.ColObjects
import Kitronik_v10 as Kitronik
from machine import Pin

module_name = 'ThisPico_F_v11.py'

class ThisVolts(GPIO.Volts):
    def __init__(self):
        super().__init__('VIN',29)


class ThisHCSR04(GPIO.HCSR04):
    def __init__(self):
        super().__init__(name='FRONT_US',
                 trigger_pin_no=19,
                 echo_pin_no=20,
                 critical_distance=100.0)


class TheseIRSensors():
    def __init__(self):
        self.front_left_ir = GPIO.IRSensor('FRONT_LEFT_IR',22)
        self.front_right_ir = GPIO.IRSensor('FRONT_RIGHT_IR',16)
        self.rear_left_ir = GPIO.IRSensor('REAR_LEFT_IR',18)
        self.rear_right_ir = GPIO.IRSensor('REAR_RIGHT_IR',2)
        self.ir_list = [self.front_left_ir, self.front_right_ir, self.rear_left_ir, self.rear_right_ir]
    def close(self):
        for ir in self.ir_list:
            ir.close()


class TheseSwitches():
    def __init__(self):
        self.DIP_1 = GPIO.Switch('DIP_1',13)
        self.DIP_2 = GPIO.Switch('DIP_2',12)
        self.DIP_3 = GPIO.Switch('DIP_3',11)
        self.DIP_4 = GPIO.Switch('DIP_4',6)
        self.switch_list = [self.DIP_1,self.DIP_2,self.DIP_3,self.DIP_4]
    def close(self):
        for switch in self.switch_list:
            switch.close()


class TheseButtons():
    def __init__(self):
        self.yellow_button = GPIO.Button('YELLOW_BUTTON',7)
        self.button_list = [self.yellow_button]
        #   NOTE.  On this robot, the red button is hardwired to reset
    def close(self):
        for button in self.button_list:
            button.close()

class ThisLeftHeadlight(GPIO.RGBLED):
    def __init__(self):
        red_led = GPIO.LED('LEFT_RED',10)
        green_led = GPIO.LED('LEFT_GREEN',14)
        blue_led = GPIO.LED('LEFT_BLUE',15)
        super().__init__("Left Headlight", red_led, green_led, blue_led)

class ThisRightHeadlight(GPIO.RGBLED):
    def __init__(self):
        red_led = GPIO.LED('RIGHT_RED',27)
        green_led = GPIO.LED('RIGHT_GREEN',26)
        blue_led = GPIO.LED('RIGHT_BLUE',17)
        super().__init__("Right Headlight", red_led, green_led, blue_led)

class ThisDriveTrain(ColObjects.DriveTrain):
    def __init__(self, board_object):
        self.left_side = ColObjects.Side('Left Side', 'R', [
            Kitronik.KitronikMotor('FRONT_LEFT', board_object, 4),
            Kitronik.KitronikMotor('REAR_LEFT', board_object, 1)])
        self.right_side = ColObjects.Side('Right Side', 'R', [
            Kitronik.KitronikMotor('FRONT_RIGHT', board_object, 3),
            Kitronik.KitronikMotor('REAR_RIGHT', board_object, 2)])
        super().__init__('ThisDriveTrain', self.left_side, self.right_side)
        self.last_spin = ''
        self.millimetre_factor = 102
        self.degree_factor = 275
        self.speed_exponent = 0.5

class ThisDriveTrainWithHeadlights(ColObjects.DriveTrainWithHeadlights):
    def __init__(self, board_object, left_headlight, right_headlight):
        self.board_object = board_object
        self.left_headlight = left_headlight
        self.right_headlight = right_headlight
        self.left_side = ColObjects.Side('Left Side', 'R', [
            Kitronik.KitronikMotor('FRONT_LEFT', board_object, 4),
            Kitronik.KitronikMotor('REAR_LEFT', board_object, 1)])
        self.right_side = ColObjects.Side('Right Side', 'R', [
            Kitronik.KitronikMotor('FRONT_RIGHT', board_object, 3),
            Kitronik.KitronikMotor('REAR_RIGHT', board_object, 2)])
        super().__init__('ThisDriveTrain', self.left_side, self.right_side, self.left_headlight, self.right_headlight)
        self.last_spin = ''
        self.millimetre_factor = 102
        self.degree_factor = 275
        self.speed_exponent = 0.5

class ThisShoulderServo(Kitronik.Servo):
    def __init__(self, board_object):
        super().__init__('Shoulder Servo',
                 board_object,
                 servo_no=1,
                 max_rotation=180,
                 min_rotation=0,
                 park_position=90,
                 transport_position=90)
    def up(self, speed=100):
        self.move_to(new_position=90, speed=speed)
    def down(self, speed=165):
        self.move_to(new_position=159, speed=speed)
    

class ThisBucketServo(Kitronik.Servo):
    def __init__(self, board_object):
        super().__init__('Bucket Servo',
                 board_object,
                 servo_no=2,
                 max_rotation=180,
                 min_rotation=0,
                 park_position=10,
                 transport_position=90)
    def up(self, speed=1):
        self.move_to(new_position=130, speed=speed)
    def down(self, speed=155):
        self.move_to(new_position=155, speed=speed)

class ThisArm(Kitronik.Arm):
    def __init__(self, board_object):
        bucket_servo = ThisBucketServo(board_object)
        shoulder_servo = ThisShoulderServo(board_object)
        super().__init__('Front Loader', board_object, shoulder_servo, bucket_servo)
        my_arm = self
        my_arm.poses['PARK'] = [[my_arm.shoulder_servo,90],[my_arm.bucket_servo,90]]
        my_arm.poses['UP'] = [[my_arm.shoulder_servo,100],[my_arm.bucket_servo,110]]
        my_arm.poses['DUMP'] = [[my_arm.shoulder_servo,90],[my_arm.bucket_servo,155]]
        my_arm.poses['CARRY'] = [[my_arm.shoulder_servo,70],[my_arm.bucket_servo,1]]
        my_arm.poses['DOWN'] = [[my_arm.shoulder_servo,165],[my_arm.bucket_servo,10]]
        my_arm.poses['SCOOP'] = [[my_arm.shoulder_servo,160],[my_arm.bucket_servo,1]]

class ThisInterpolator(RemoteControl.Interpolator):
    def __init__(self):
        name = 'Standard Interpolator'
        keys = [48, 60, 62, 102]
        values = [-100.0, 0.0, 0.0, 100.0]
        super().__init__(name, keys, values)

class ThisThrottle(RemoteControl.Joystick):
    def __init__(self, interpolator):
        tsm = RemoteControl.StateMachine(name='Throttle SM', code='MEASURE', pin_no=3)
        super().__init__(name='Throttle', state_machine=tsm, interpolator=interpolator)

class ThisAileron(RemoteControl.Joystick):
    def __init__(self, interpolator):
        tsm = RemoteControl.StateMachine(name='Aileron SM', code='MEASURE', pin_no=4)
        super().__init__(name='Aileron', state_machine=tsm, interpolator=interpolator)

class ThisFlap(RemoteControl.Joystick):
    def __init__(self, interpolator):
        tsm = RemoteControl.StateMachine(name='Flap SM', code='MEASURE', pin_no=5)
        super().__init__(name='Flap', state_machine=tsm, interpolator=interpolator)

class ThisRemoteControl(RemoteControl.RemoteControl):
    def __init__(self, drive_train):
        left_side = drive_train.left_side
        right_side = drive_train.right_side
        # NOTE: Interpolation values are set experimentally with test_18_A_radio_control_v02.py
        int_t = RemoteControl.Interpolator('Throttle Interpolator', [40, 50, 70, 73, 96, 110], [-100.0, -100.0, 0.0, 0.0, 100.0, 100.0])
        int_s = RemoteControl.Interpolator('Steering Interpolator', [40, 56, 74, 76, 93, 110], [100.0, 100.0, 0.0, 0.0, -100.0, -100.0])
        int_k = RemoteControl.Interpolator('Knob Interpolator', [40, 50, 74, 76, 101, 110], [-100.0, -100.0, 0.0, 0.0, 100.0, 100.0])
        left_up_down = ThisThrottle(int_t)
        left_sideways=None
        right_up_down=None
        right_sideways = ThisAileron(int_s)
        self.knob = ThisFlap(int_k)
        mode_switch=None
        super().__init__(
                 'PicoF Remote',
                 left_side,
                 right_side,
                 left_up_down,
                 left_sideways,
                 right_up_down,
                 right_sideways,
                 mode_switch,
                 )

class ThisRemoteControlWithHeadlights(RemoteControl.RemoteControlWithHeadlights):
    def __init__(self, drive_train, left_headlight, right_headlight):
        self.left_headlight = left_headlight
        self.right_headlight = right_headlight
        left_side = drive_train.left_side
        right_side = drive_train.right_side
        # NOTE: Interpolation values are set experimentally with test_18_A_radio_control_v02.py
        int_t = RemoteControl.Interpolator('Throttle Interpolator', [40, 50, 70, 73, 96, 110], [-100.0, -100.0, 0.0, 0.0, 100.0, 100.0])
        int_s = RemoteControl.Interpolator('Steering Interpolator', [40, 56, 74, 76, 93, 110], [100.0, 100.0, 0.0, 0.0, -100.0, -100.0])
        int_k = RemoteControl.Interpolator('Knob Interpolator', [40, 50, 74, 76, 101, 110], [-100.0, -100.0, 0.0, 0.0, 100.0, 100.0])
        left_up_down = ThisThrottle(int_t)
        left_sideways=None
        right_up_down=None
        right_sideways = ThisAileron(int_s)
        self.knob = ThisFlap(int_k)
        mode_switch=None
        super().__init__(
                 'PicoF Remote',
                 left_side,
                 right_side,
                 left_up_down,
                 left_sideways,
                 right_up_down,
                 right_sideways,
                 mode_switch,
                 left_headlight,
                 right_headlight
                 )

uart_tx = GPIO.Reserved('UART TX', 'OUTPUT', 0)
uart_rx = GPIO.Reserved('UART RX', 'INPUT', 1)
smps_mode = GPIO.Reserved('SMPS Mode', 'OUTPUT', 23)
vbus_monitor = GPIO.Reserved('VBUS Monitor','INPUT',24)
onboard_led = GPIO.LED('Onboard LED', 25)
onboard_volts = GPIO.Volts('Onboard Voltmeter', 29)
    
#####  For testing compilation and GPIO clashes
if __name__ == "__main__":
    print (module_name, '\n')
    board_object = Kitronik.Kitronik('The Only Board')
    #bucket_servo = ThisBucketServo()
    #shoulder_servo = ThisShoulderServo()
    arm = ThisArm(board_object)
    left_headlight = ThisLeftHeadlight()
    right_headlight = ThisRightHeadlight()
    drive_train = ThisDriveTrainWithHeadlights(board_object,left_headlight,right_headlight)
    buttons = TheseButtons()
    switches = TheseSwitches()
    ir_sensors = TheseIRSensors()
    hcsr04 = ThisHCSR04()
    #throttle = ThisThrottle()
    #steering = ThisAileron()
    my_remote = ThisRemoteControl(drive_train)
    print ('----- GPIO pin allocations -----')
    print (GPIO.GPIO.str_allocated())
    print ('----- Kitronik servo allocations -----')
    print (board_object.str_servo_list())
    print ('----- Kitronik motor allocations -----')
    print (board_object.str_motor_list())
