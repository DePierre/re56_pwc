#-*-coding:utf-8 -*

import os

import math
import copy
import thread
from device import Device
from shared_resources import devices
from constants import *

# this a tmp import used only to make an example of execution on this worker
import time


def do_work():
    """This function is used in an independant thread to simulate the evolution
    of the UE emitted power among the grid according to Open, Inner & Outer
    loops in UMTS.
    """
    # Waiting loop
    while 1:
        # Implement the Open, Inner & Outer loops here
        print("i'm the worker and i'm processing")  # This is just an example
        time.sleep(1)   # This is just an example
        
        
def open_loop():
    """implementation of the open loop.
        
    This loop is in charge of the initial setting of the emitted power for any
    User Equipment in UMTS.
    
    The initial emitted power is deduced from a comparison between a 
    measurement of the received power from the antenna (computed from Friis 
    formula) and the real emitted power from a broadcast packet.
    This comparison gives us the free space path loss between the antenna and 
    this UE.
    Then from this loss according to friis formula and sensitivity of the Node B 
    we can compute the initial emitted power to use with this UE .
    
    reminder :
        Friis Formula : Pr = Pe + Ge + Gr - (20log(f) + 20log(d in km) + 32.44)
        with Pr, Pe, Gr, Ge in dB
        
        Since the gains are null the free space loss corresponds to the part 
        between parenthesis.
    """
    # Retry MAX_PREAMBLE_CYCLE times before considering the UE connected or not
    while i < MAX_PREAMBLE_CYCLE:
        for index, device in enumerate(devices):
            if index != 0:
                device.set_device_trying_to_connect()
                # Increase PREAMBLE_RETRANS_MAX times
                while j < PREAMBLE_RETRANS_MAX:
                    # computation of the free space path loss.
                    free_space_loss = 20*log10(UMTS_FREQUENCY) + 20*log10(device.distance_from_antenna/1000) + 32.44
                    # Computation of the emitted power to reach to be sure the 
                    # NodeB will receive the signal.
                    emitted_power_to_reach = ANTENNA_SENSITIVITY - ANTENNA_GAIN - UE_GAIN + free_space_loss
                    # If the current emitted power isn't sufficient then
                    # increase it by a step
                    if device.current_emitted_power >= emitted_power_to_reach:
                        device.set_device_connected()
                    elif device.current_emitted_power < UE_MAX_EMITTED_POWER:
                        device.current_emitted_power += POWER_CONTROL_STEP
                        device.set_command_up()
                    else :
                        device.set_device_disconnected()                   
                    j += 1
        i += 1
        
        
        
        
