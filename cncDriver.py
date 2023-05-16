class cncDriver: 
    def __init__(self, EN_pin, tim):
        self.EN_pin = EN_pin                                                     # Enable pin                                                                                       
        self.direction = 1                                                       # direction pin, 1 is forward, 0 is backwards
        self.tim = tim                                                           # Timer for sending PWM
        self.chn = self.tim.channel(1, pyb.Timer.PWM, pulse_width_percent=50)  # Timer channel in PWM mode, 50% duty cycle, send PWM on this pin as well
        self.speed_sp = 0

# input: speed set point in mph 
# this function takes the speed set point (in mph) converts that to a shaft speed (rpm) at the motor using the appropriate 
# tread roller OD and pulley reduction 
# Timer_freq [hz] = (6*Motor_shaft_speed)/step_angle
    def set_speed(self, speed):

        # constants 
        pulley_reduction = 2                                                    # motor shaft to tread roller
        tread_roller_radius = 0.0612/2                                          # tread roller OD (m)
        step_angle = 360/30                                                     # 360/(30 ticks/rev) -----> from inertia mass on motor shaft

        # Calcs
        self.speed_sp = speed
        tread_roller_speed = ((speed/2.237)/(tread_roller_radius))*9.5492968    # tread roller speed (rpm)
        motor_shaft_speed = (tread_roller_speed)*pulley_reduction               # motor shaft speed (rpm)
        timer_freq = (6*motor_shaft_speed)/step_angle                           # required timer freq to achieve motor speed (Hz)

        self.tim.freq(timer_freq)                                               # set timer to desired freq from above


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

