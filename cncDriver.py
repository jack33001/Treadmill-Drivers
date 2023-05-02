from pyb import Timer
from pyb import Pin

class cncDriver: 
    def __init__(self, step_pin, dir_pin):
        self.step_pin = step_pin
        self.dir_pin = dir_pin
    
    def step(self, direction):
        self.dir_pin.value(direction)
        self.step_pin.value(1)
        self.step_pin.value(0)