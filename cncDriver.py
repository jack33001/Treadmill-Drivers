from pyb import Timer
from pyb import Pin
#Motor speed (r/min) = step angle (°/step) ÷ 360 (°) × pulse rate (Hz) × 60
class cncDriver: 
    def __init__(self, dir_pin, step_pin, EN_pin, tim, tim_chn_pin):
        self.ARR = 100 #ticks per second (based on 30 ticks/rev)
        self.EN_pin = EN_pin
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.direction = 0
        self.tim = tim
        self.chn = self.tim.channel(1, pyb.Timer.PWM, pulse_width_percent=50)
    
    def set_duty(self, duty):
        if duty < 0: 
            print('Invalid Input')
        else: 
            self.tim.freq(2000)

    def enable (self):
        self.EN_pin = Pin(self.EN_pin,mode=Pin.OUT_PP)
        self.EN_pin.high()
        print('enable pin high\n')
        pass

    def disable (self):
        self.EN_pin = Pin(self.EN_pin,mode=Pin.OUT_PP)
        self.EN_pin.low()
        print('enable pin low\n')
        pass

