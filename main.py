from time import sleep
import time
import keyboard
from phonesensors import PhoneSensorsClient, Apps
from threading import Timer  
 
def setTimeout(fn, ms, *args, **kwargs): 
    t = Timer(ms / 1000., fn, args=args, kwargs=kwargs) 
    t.start() 
    return t 

def count_down(time):
  for i in reversed(range(1, time+1)):
    print(i)
    sleep(1)

def calibrate():
    accum = 0
    print('Move to the right in: ', end='')

    count_down(3)
    t_end = time.time() + .300
    for data in client:
        x = round(data.lin_acc.values[0][0], 2)
        accum += x
        if (t_end < time.time()):
            break
    right_x = accum
    accum = 0

    print('Move to the left in: ', end='')

    count_down(3)
    t_end = time.time() + .300
    for data in client:
        x = round(data.lin_acc.values[0][0], 2)
        accum += x
        if (t_end < time.time()):
            break
    left_x = accum
    accum = 0


    print('Finished calibration')
    print(f'Right x: {right_x}')
    print(f'Left x: {left_x}')

    return [left_x, right_x]

def check_direction():
    global horizontalMovementDetect
    global ix_hist
    global ix

    ix_hist = ix

    total_x = record_x[0]
    if (total_x < xleft):
        print('LEFT')
        #keyboard.press_and_release('left')
    elif (total_x > xright):
        print('RIGHT')
        #keyboard.press_and_release('right')
        
    record_x.clear()

def check_up_down():
    global verticalMovementDetect
    global iy_hist
    global iy

    iy_hist = iy

    total_y = sum(record_y[0:len(record_y)//2])
    if (total_y < -15):
        print('DOWN')
        #keyboard.press_and_release('down')
    elif (total_y > 35):
        print('UP')
        #keyboard.press_and_release('up')

    record_y.clear()


def check_movement(x):
    global horizontalMovementDetect
    global ix_hist
    if (ix - ix_hist > 30):
        if (x > xright):
            print('RIGHT AA')
            keyboard.press_and_release('right')
            horizontalMovementDetect = True
            ix_hist = ix
        if (x < xleft):
            print('LEFT AA')
            keyboard.press_and_release('left')
            horizontalMovementDetect = True
            ix_hist = ix

def check_vertical(y):
    global verticalMovementDetect
    global iy_hist
    if (iy - iy_hist > 20):
        if (y > yup):
            print('UP AA')
            keyboard.press_and_release('up')
            verticalMovementDetect = True
            iy_hist = iy
        if (y < ydown):
            print('DOWN AA')
            keyboard.press_and_release('down')
            verticalMovementDetect = True
            iy_hist = iy

with PhoneSensorsClient("192.168.1.101", 5000, Apps.SENSORSTREAMER) as client:

    horizontalMovementDetect = False; # Track if movement has already been detected
    verticalMovementDetect = False
    timeThreshold = 10; # Time threshold in ms

    xleft = -2.5
    xright = 2.5

    yup = 4
    ydown = -6

    ix = 0
    ix_hist = 0

    iy = 0
    iy_hist = 0

    record_x = []
    record_y = []
    for data in client:
        ix+=1
        iy+=1
        x = round(data.lin_acc.values[0][0], 2)
        y = round(data.lin_acc.values[0][1], 2)


        if (not horizontalMovementDetect):
            check_movement(x)
            '''
            if(horizontalMovementDetect):
                movementTimeout = setTimeout(check_direction, timeThreshold)'''

        if horizontalMovementDetect:
            #record_x.append(x)
            if (abs(x) < xright/2):
                horizontalMovementDetect = False


        if (not verticalMovementDetect):
            check_vertical(y)
            '''
            if(verticalMovementDetect):
                movementTimeout = setTimeout(check_up_down, timeThreshold)'''

        if verticalMovementDetect:
            #record_y.append(y)
            if (abs(y) < yup/2):
                verticalMovementDetect = False