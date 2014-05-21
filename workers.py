#-*-coding:utf-8 -*

import os

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
