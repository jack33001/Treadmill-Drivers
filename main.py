#imports
import pyb
from pyb import Pin, Timer
import time
from pyb import ExtInt
import micropython
from cncDriver import cncDriver

micropython.alloc_emergency_exception_buf(100)

if __name__ == '__main__':
    try:  
        while True:
            #timer 4 ch1: b6
            print('Running')

            #motor setup stuff
            print('Motor Enabled')
            tim = Timer(4, freq = 20000)
            mot = cncDriver(Pin.cpu.C0, tim)
            mot.enable()
           

            #prompt the user for which motor to use
            while True:
                try:
                    userin = input('What speed do you want to run the treadmill at [mph]? Input a number only.\n')
                    if userin.isdigit():
                        print('goodinputbro')
                        break
                    else:
                        raise ValueError('Bad input, must be number\n')
                except ValueError:
                        print('excepted')
                        pass
            # set speed of motor
            mot.set_speed(int(userin))
            print('Motor speed set to: ' + userin  + '\r\nTimer freq: ' + tim.freq() + 'Hz')

    except KeyboardInterrupt:
            print('leaving')