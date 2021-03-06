# -*-coding:utf-8 -*
"""

    device.py

    Declare the classes representing a device in a mobile network.

    Device: the abstract class for all other devices.
        Antenna: the class corresponding to the UMTS antenna.
        Ue: the mother class of an user equipment.
            UeCall: the Ue sub-class simulating a voice call (i.e low thoughput
                    needed).
            UePS64: the Ue sub-class simulating a small 3G data exchange.
            UePS128: the Ue sub-class simulating a medium 3G data exchange.
            UePS384: the Ue sub-class simulating a high 3G data exchange.
            UeHSDPA768: the Ue sub-class simulating a 3G+ medium data exchange.
            UeHSDPA2000: the Ue sub-class simulating a 3G+ high data exchange.

"""


import pygame
from pygame.locals import *

import random
from threading import Lock
from math import sqrt

from constants import *


class Device(object):
    """Abstract class representing a device on the mobile network."""

    def __init__(self, (x, y)):
        self.mutex = Lock()  # Mutex needed when running threaded loops.
        self.x = x
        self.y = y
        self.distance_from_antenna = 0.0
        self.emitted_power = 0.0
        self.open_looped = False  # Does the device finished its open loop?
        self.snr = 0
        self.command = COMMAND_UP
        self.status = NOT_CONNECTED
        self.image = None  # Image representing the device.

    def compute_distance(self, neighboor):
        """Distance between two devices.

        The distance is needed by the free space loss formula.

        """
        distance_x = abs(self.x - neighboor.x) * PIX_IN_METERS
        distance_y = abs(self.y - neighboor.y) * PIX_IN_METERS
        return sqrt(pow(distance_x,2) + pow(distance_y,2))


class Antenna(Device):
    """Class representing an Antenna with its characteristics."""

    def __init__(self, (x, y)):
        Device.__init__(self, (x, y))
        self.emitted_power = ANTENNA_EMITTED_POWER
        self.image = pygame.image.load(ANTENNA_IMAGE).convert_alpha()


class Ue(Device):
    """Class representing an User equipment."""

    # Images
    img_co_up = DEVICE_CONNECTED_UP_IMAGE
    img_co_down = DEVICE_CONNECTED_DOWN_IMAGE
    img_try_up = DEVICE_TRY_TO_CONNECT_UP_IMAGE
    img_try_down = DEVICE_TRY_TO_CONNECT_DOWN_IMAGE
    img_disco = DEVICE_DISCONNECTED_IMAGE
    SNR = 100  # Default SNR value for an UE in dB

    def __init__(self, (x, y), antenna):
        Device.__init__(self, (x, y))
        self.antenna = antenna
        self.distance_from_antenna = self.compute_distance(antenna)
        self.emitted_power = UE_MAX_EMITTED_POWER
        self.snr = self.SNR  # SNR in dB
        self.target = 0.0
        self.command = COMMAND_UP
        self.status = TRY_CONNECT
        self.reload()

    def set_coor_random(self, free_coors=[]):
        """Randomly set the coordinates of the UE.

        Randomly pick a free coordinate from `free_coors`.

        """
        if not free_coors:
            print "No more available coordinates."
            return
        index = random.randint(0, len(free_coors) - 1)
        self.x, self.y = free_coors[index]
        del free_coors[index]  # The cell is not free anymore.
        self.distance_from_antenna = self.compute_distance(self.antenna)

    def set_command_up(self):
        """Set the command of the device to COMMAND_UP.

        Apply a step on the emitted power of this UE.
        Update the image assigned to the device.

        """
        self.command = COMMAND_UP
        if self.status == TRY_CONNECT:
            self.image = pygame.image.load(self.img_try_up).convert_alpha()
        elif self.status == CONNECTED:
            self.image = pygame.image.load(self.img_co_up).convert_alpha()
        else :
            self.image = pygame.image.load(self.img_disco).convert_alpha()
        if self.emitted_power < UE_MAX_EMITTED_POWER:
            if not self.emitted_power + POWER_CONTROL_STEP > UE_MAX_EMITTED_POWER:
                self.emitted_power += POWER_CONTROL_STEP
            else:
                self.emitted_power = UE_MAX_EMITTED_POWER
        else:
            self.set_device_disconnected()
            print "Device disconnected : can't command up"

    def set_command_down(self):
        """Set the command of the device to COMMAND_DOWN.

        Apply a step on the emitted power of this UE.
        Update the image assigned to the device.

        """
        self.command = COMMAND_DOWN
        if self.status == TRY_CONNECT:
            self.image = pygame.image.load(self.img_try_down).convert_alpha()
        elif self.status == CONNECTED:
            self.image = pygame.image.load(self.img_co_down).convert_alpha()
        else :
            self.image = pygame.image.load(self.img_disco).convert_alpha()
        self.emitted_power -= POWER_CONTROL_STEP

    def set_device_connected(self):
        """Set the status of the device to CONNECTED.

        Update the image assigned to the device.

        """
        self.status = CONNECTED
        if self.command == COMMAND_UP:
            self.image = pygame.image.load(self.img_co_up).convert_alpha()
        else :
            self.image = pygame.image.load(self.img_co_down).convert_alpha()

    def set_device_trying_to_connect(self):
        """Set the status of the device to TRY_CONNECT.

        Update the image assigned to the device.

        """
        self.status = TRY_CONNECT
        if self.command == COMMAND_UP:
            self.image = pygame.image.load(self.img_try_up).convert_alpha()
        else :
            self.image = pygame.image.load(self.img_try_down).convert_alpha()

    def set_device_disconnected(self):
        """Set the status of the device to NOT_CONNECTED.

        Update the image assigned to the device.

        """
        self.status = NOT_CONNECTED
        self.image = pygame.image.load(self.img_disco).convert_alpha()

    def reload(self):
        """Reload the current image.

        According to connection status and current command.

        """
        if self.status == TRY_CONNECT:
            if self.command == COMMAND_UP:
                self.image = pygame.image.load(self.img_try_up).convert_alpha()
            else :
                self.image = pygame.image.load(self.img_try_down).convert_alpha()
        elif self.status == CONNECTED:
            if self.command == COMMAND_UP:
                self.image = pygame.image.load(self.img_co_up).convert_alpha()
            else :
                self.image = pygame.image.load(self.img_co_down).convert_alpha()
        else :
            self.image = pygame.image.load(self.img_disco).convert_alpha()


class UeVoice(Ue):
    """User Equipment simulating a voice call."""

    # Images
    img_co_up = VOICE_CONNECTED_UP_IMAGE
    img_co_down = VOICE_CONNECTED_DOWN_IMAGE
    img_try_up = VOICE_TRY_TO_CONNECT_UP_IMAGE
    img_try_down = VOICE_TRY_TO_CONNECT_DOWN_IMAGE
    img_disco = VOICE_DISCONNECTED_IMAGE
    SNR = VOICE_SNR_TARGET


class UePS64(Ue):
    """User Equipment simulating a PS-64."""

    # Images
    img_co_up = A3GLT_CONNECTED_UP_IMAGE
    img_co_down = A3GLT_CONNECTED_DOWN_IMAGE
    img_try_up = A3GLT_TRY_TO_CONNECT_UP_IMAGE
    img_try_down = A3GLT_TRY_TO_CONNECT_DOWN_IMAGE
    img_disco = A3GLT_DISCONNECTED_IMAGE
    SNR = A3GLT_SNR_TARGET


class UePS128(Ue):
    """User Equipment simulating a PS-128."""

    # Images
    img_co_up = A3GMT_CONNECTED_UP_IMAGE
    img_co_down = A3GMT_CONNECTED_DOWN_IMAGE
    img_try_up = A3GMT_TRY_TO_CONNECT_UP_IMAGE
    img_try_down = A3GMT_TRY_TO_CONNECT_DOWN_IMAGE
    img_disco = A3GMT_DISCONNECTED_IMAGE
    SNR = A3GMT_SNR_TARGET


class UePS384(Ue):
    """User Equipment simulating a PS-384."""

    # Images
    img_co_up = A3GLT_CONNECTED_UP_IMAGE
    img_co_down = A3GLT_CONNECTED_DOWN_IMAGE
    img_try_up = A3GLT_TRY_TO_CONNECT_UP_IMAGE
    img_try_down = A3GLT_TRY_TO_CONNECT_DOWN_IMAGE
    img_disco = A3GLT_DISCONNECTED_IMAGE
    SNR = A3GHT_SNR_TARGET


class UeHSDPA768(Ue):
    """User Equipment simulating a HSDPA-768."""

    # Images
    img_co_up = HLT_CONNECTED_UP_IMAGE
    img_co_down = HLT_CONNECTED_DOWN_IMAGE
    img_try_up = HLT_TRY_TO_CONNECT_UP_IMAGE
    img_try_down = HLT_TRY_TO_CONNECT_DOWN_IMAGE
    img_disco = HLT_DISCONNECTED_IMAGE
    SNR = HLT_SNR_TARGET


class UeHSDPA2000(Ue):
    """User Equipment simulating a HSDPA-2000."""

    # Images
    img_co_up = HHT_CONNECTED_UP_IMAGE
    img_co_down = HHT_CONNECTED_DOWN_IMAGE
    img_try_up = HHT_TRY_TO_CONNECT_UP_IMAGE
    img_try_down = HHT_TRY_TO_CONNECT_DOWN_IMAGE
    img_disco = HHT_DISCONNECTED_IMAGE
    SNR = HHT_SNR_TARGET
