import PicoBotF_v03 as ThisPico
import utime

my_drive_train = ThisPico.ThisDriveTrain()

def move(side, speed, rotation):
    side.move(speed, rotation)
    utime.sleep(1)
    side.stop()
    
speed = 95
millimetres = 50
sleep_time = 1.0
my_drive_train.fwd(speed,millimetres)
utime.sleep(sleep_time)
my_drive_train.rev(speed,millimetres)
utime.sleep(sleep_time)

speed = 95
degrees = 25
my_drive_train.spl(speed,degrees)
utime.sleep(sleep_time)
my_drive_train.spr(speed,degrees)
utime.sleep(sleep_time)

my_drive_train.stop()