import cotask
import task_share
import gc
import struct
from pyb import CAN, Pin
from encoder import Encoder
from time import ticks_us, ticks_add, ticks_diff

# Message received callback
def cb0(bus, reason):
    global messageReceived
    messageReceived = True
    
    if reason == 0:
        #message accepted in empty fifo
        pass
    if reason == 1:
        #fifo is full
        pass
    elif reason == 2:
        #message lost due to full fifo
        pass

# CAN task
def send_recv_data(can,force,location,speed):
    # If the CAN has not been initialized yet, initialize
    if can_init_flag.get()
        # Set timing scheme
        period = 2_500
        start_time = ticks_us()
        next_time = ticks_add(start_time, period)

        # Set up callback variable
        messageReceived = False

        # Initialize everything
        # Set up encoder object
        encoder_1 = Encoder(Pin.cpu.B4, Pin.cpu.B5, 3, 10000)

        # Set up CAN pins
        RxPin = Pin(Pin.cpu.B8, mode = Pin.AF_PP, alt = Pin.AF9_CAN1)
        TxPin = Pin(Pin.cpu.B9, mode = Pin.AF_PP, alt = Pin.AF9_CAN1)

        # Set up CAN communication object
        can = CAN(1, CAN.NORMAL, baudrate=1_000_000, auto_restart = True) # Make CAN object (still unsure of some settings, though this is what semi worked)
        SEND_ID = 4 # Address to send data out on
        PING_ID = 6 # Address to receive incoming pings on
        can.setfilter(0, CAN.LIST16, 0, (SEND_ID, PING_ID, 7, 8))  # Set a filter to receive messages with id = SEND_ID, PING_ID, 7, and 8 (7 and 8 are arbitrary, never used)
        can.rxcallback(0, cb0) # Set up interrupt when a message comes in

        # Set up dataBytes object
        dataBytes = struct.pack('<ih', 0, 0)

    # Now that initialization has occurred 
    else
        # If a ping has been received, instantly do the task it asks for
        if messageReceived:
            while can.any(0):
                data = can.recv(0)
                messageReceived = False
                # See if the message accepted is from the right ID
                if data[0] == PING_ID:
                    # Check what the message included to see what to do
                    if data[4] == 5: # Check for 5 value (arbitrary for now) to send data
                        can.send(dataBytes, SEND_ID)
                    elif data[4] == 0: # Check for 0 value (arbitrary for now) to zero encoders
                        encoder_1.zero()
        else:
            # Check if time to run
            current_time = ticks_us()
            if ticks_diff(current_time, next_time) >= 0:
                # Set next time
                next_time = ticks_add(next_time, period)
                # Update encoder
                encoder_1.update()
                positionDec = encoder_1.get_position()
                velocityDec = encoder_1.get_delta()
                # Pack dataBytes to be ready to send whenever
                dataBytes = struct.pack('<ih', round(positionDec), round(velocityDec*1000)) # pack position to a 4 byte int and (velocity * 1000) to a 2 byte int
            # If not time, then pass
            else:
                pass

# Force sensing task
def force_sensing():
    # poll the strain gauge boards, translate this to a force and location
    '''insert code here'''
    # assumed values for programming purposes
    sens1= 0
    sens2 = 0
    sens3 = 0
    sens4= 0
    sens5 = 0
    sens6 = 0
    # find the net force and position
    '''insert code here'''

# Treadmill speed task
def run_treadmill(controller):
    # run controller
    '''insert code here'''
    # run stepper driver
    '''insert code here'''
    pass

# Mastermind task
def mastermind():
    # setttin da flagz
    pass


if __name__ == "__main__": 
    # making and initializing objects:
    # CAN
    can = CAN(1, CAN.LOOPBACK)
    can.setfilter(0, CAN.LIST16, 0, (123, 124, 125, 126))  # set a filter to receive messages with id=123, 124, 125 and 126

    # Controller
    controller = 5 '''change this to controller object'''

    # Measurement


    # make shares/queues                      
    force = task_share.Share ('f', thread_protect = False, name = "force")                          # measured force
    location = task_share.Share ('f', thread_protect = False, name = "location")                    # measured force location
    speed = task_share.Share ('f', thread_protect = False, name = "speed")                          # desired treadmill speed
    can_init_flag = task_share.Share ('f', thread_protect = False, name = "can_init_flag")          # desired brushless speed

    # flags
    init_flag = task_share.Share ('h', thread_protect = False, name = "init_flag")                  # flag that says to zero everything

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task_mastermind = cotask.Task(mastermind(), name = 'Task_Mastermind', priority = 1, period = 5, profile = True, trace = False)
    task_run_treadmill = cotask.Task(run_treadmill(controller), name = 'Task_Run_Treadmill', priority = 1, period = 5, profile = True, trace = False)
    task_force_sensing = cotask.Task(force_sensing(), name = 'Task_Force_Sensing', priority = 1, period = 5, profile = True, trace = False)
    task_send_recv_data = cotask.Task(send_recv_data(can,force,location,speed), name = 'Task_Send_Recv_Data', priority = 1, period = 5, profile = True, trace = False)
    cotask.task_list.append(task_mastermind)
    cotask.task_list.append(task_run_treadmill)
    cotask.task_list.append(task_force_sensing)
    cotask.task_list.append(task_send_recv_data)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()

    try:
        while(True):
            cotask.task_list.pri_sched()
    except KeyboardInterrupt:
        print('\n\r\r> Program Terminated')