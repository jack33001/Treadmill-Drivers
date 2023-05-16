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

if __name__ == '__main__':

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