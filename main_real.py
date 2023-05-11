from pyb import can as CAN
import cotask
import task_share
import gc

def send_recv_data(can,force,location,speed):
    # if there is a message waiting, receive it and raise the flag
    if can.any() == 1:
        received = can.recv(0)                 # receive message on FIFO 0
        received_msg = 1
    # if there is a message waiting to be sent, send it and drop the flag
    if sending == 1:
        msg = str(force) + str(location) + str(speed)
        can.send(msg, 123)   # send a message with id 123
        sending = 0

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

def run_treadmill(controller):
    # run controller
    '''insert code here'''
    # run stepper driver
    '''insert code here'''
    pass

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
    force = task_share.Share ('f', thread_protect = False, name = "force")      # desired brushless speed
    location = task_share.Share ('f', thread_protect = False, name = "location")      # desired brushless speed
    speed = task_share.Share ('f', thread_protect = False, name = "speed")      # desired brushless speed

    # flags
    init_flag = task_share.Share ('h', thread_protect = False, name = "init_flag")            # flag that says to zero everything

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