#imports
import pyb
from pyb import Pin, Timer
import time
from pyb import ExtInt
import micropython
from cncDriver import cncDriver

micropython.alloc_emergency_exception_buf(100)

if __name__ == '__main__':
    tim = Timer(4, freq = 2000)
    #motor setup stuff
    mot = cncDriver(Pin.cpu.C0, tim, Pin.cpu.B6)
    mot.enable()
    print('Running')
    try:  
        while True:
            #timer 4 ch1: b6
            #prompt the user for which motor to use
            while True:
                try:
                    userin = input('What speed do you want to run the treadmill at [mph]? Input a number only.\n')
                    if float(userin) > 0 and float(userin) <= 12:
                        break
                    else:
                        raise ValueError('Value error\n')
                except ValueError:
                        print('Bad Input, try again!\n\r')
                        pass
            # set speed of motor
            mot.set_speed(float(userin))
            print('Motor speed set to: ' + userin + ' mph' + '\r\nTimer freq: ' + str(tim.freq()) + 'Hz\r\n')
    except KeyboardInterrupt:
            print('Exit.') 