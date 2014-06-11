# -*-coding:utf-8 -*


import pygame
from pygame.locals import *

import random
from threading import Lock
from math import sqrt

from constants import *


class Device(object):
    def __init__(self, (x, y)):
        self.mutex = Lock()
        self.x = x
        self.y = y
        self.distance_from_antenna = 0.0
        self.emitted_power = 0.0
        self.open_looped = False
        self.snr = 0
        self.command = COMMAND_UP
        self.status = NOT_CONNECTED
        # Object which will contain the image descriptor assigned to the
        # device.
        self.image = None

    def set_image(self, imagepath):
        """To be used to assign the antenna image
        """
        self.image = pygame.image.load(imagepath).convert_alpha()

    def compute_distance(self, neighboor):
        """Distance between two devices.

        The distance is needed by the free space loss formula.

        """
        distance_x = abs(self.x - neighboor.x) * PIX_IN_METERS
        distance_y = abs(self.y - neighboor.y) * PIX_IN_METERS
        return sqrt(pow(distance_x,2) + pow(distance_y,2))


class Antenna(Device):
    """Antenna."""
    
    def __init__(self, (x, y)):
        Device.__init__(self, (x, y))
        self.emitted_power = ANTENNA_EMITTED_POWER
        self.image = pygame.image.load(ANTENNA_IMAGE).convert_alpha()


class UE(Device):
    """User Equipment."""

    def __init__(self, (x, y), antenna):
        Device.__init__(self, (x, y))
        self.antenna = antenna
        self.distance_from_antenna = self.compute_distance(antenna)
        # Set the initial emitted power to the min.
        self.emitted_power = UE_MAX_EMITTED_POWER
        self.snr = SINR_TARGET  # SNR in dB
        self.target = 0.0
        self.command = COMMAND_UP
        self.status = TRY_CONNECT
        self.reload()

    def compute_distance_from_antenna(self):
        """Compute the distance between the mobile device and the antenna
        using coordinates of the UE and the antenna as it is defined in
        constants.py.

        match between pixels and meters is defined by PIX_IN_METERS in
        constants.py.

        Any distance computation is down considering only the left bottom
        corner of both device and antenna which corresponds to the direct
        coordinate of them.
        """
        distance_x = abs(self.antenna.x - self.x) * PIX_IN_METERS
        distance_y = abs(self.antenna.y - self.y) * PIX_IN_METERS
        return sqrt(pow(distance_x,2) + pow(distance_y,2))

    def set_coor_random(self, free_coors=[]):
        """Randomly set the coordinates of the UE.

        Randomly pick a free coordinate from `free_coors`.

        """
        if not free_coors:
            print "No more available coordinates."
            return
        index = random.randint(0, len(free_coors) - 1)
        self.x, self.y = free_coors[index]
        del free_coors[index]
        self.distance_from_antenna = self.compute_distance(self.antenna)

    def set_command_up(self):
        """Set the command of the device to COMMAND_UP.

        Apply a step on the emitted power of this UE.
        Update the image assigned to the device.

        """
        self.command = COMMAND_UP
        if self.status == TRY_CONNECT:
            self.image = pygame.image.load(
                DEVICE_TRY_TO_CONNECT_UP_IMAGE).convert_alpha()
        elif self.status == CONNECTED:
            self.image = pygame.image.load(
                DEVICE_CONNECTED_UP_IMAGE).convert_alpha()
        else :
            self.image = pygame.image.load(
                DEVICE_DISCONNECTED_IMAGE).convert_alpha()
        if not self.emitted_power + POWER_CONTROL_STEP > UE_MAX_EMITTED_POWER:
            self.emitted_power += POWER_CONTROL_STEP
        elif self.emitted_power < UE_MAX_EMITTED_POWER and self.emitted_power + POWER_CONTROL_STEP > UE_MAX_EMITTED_POWER:
            self.emitted_power = UE_MAX_EMITTED_POWER
        else:
            self.set_device_disconnected()

    def set_command_down(self):
        """Set the command of the device to COMMAND_DOWN.

        Apply a step on the emitted power of this UE.
        Update the image assigned to the device.

        """
        self.command = COMMAND_DOWN
        if self.status == TRY_CONNECT:
            self.image = pygame.image.load(
                DEVICE_TRY_TO_CONNECT_DOWN_IMAGE).convert_alpha()
        elif self.status == CONNECTED:
            self.image = pygame.image.load(
                DEVICE_CONNECTED_DOWN_IMAGE).convert_alpha()
        else :
            self.image = pygame.image.load(
                DEVICE_DISCONNECTED_IMAGE).convert_alpha()
        self.emitted_power -= POWER_CONTROL_STEP

    def set_device_connected(self):
        """Set the status of the device to CONNECTED.

        Update the image assigned to the device.

        """
        self.status = CONNECTED
        if self.command == COMMAND_UP:
            self.image = pygame.image.load(
                DEVICE_CONNECTED_UP_IMAGE).convert_alpha()
        else :
            self.image = pygame.image.load(
                DEVICE_CONNECTED_DOWN_IMAGE).convert_alpha()

    def set_device_trying_to_connect(self):
        """Set the status of the device to TRY_CONNECT.

        Update the image assigned to the device.

        """
        self.status = TRY_CONNECT
        if self.command == COMMAND_UP:
            self.image = pygame.image.load(
                DEVICE_TRY_TO_CONNECT_UP_IMAGE).convert_alpha()
        else :
            self.image = pygame.image.load(
                DEVICE_TRY_TO_CONNECT_DOWN_IMAGE).convert_alpha()

    def set_device_disconnected(self):
        """Set the status of the device to NOT_CONNECTED.

        Update the image assigned to the device.

        """
        self.status = NOT_CONNECTED
        self.image = pygame.image.load(
            DEVICE_DISCONNECTED_IMAGE
        ).convert_alpha()

    def reload(self):
        """Reload the current image.

        According to connection status and current command.

        """
        if self.status == TRY_CONNECT:
            if self.command == COMMAND_UP:
                self.image = pygame.image.load(
                    DEVICE_TRY_TO_CONNECT_UP_IMAGE
                ).convert_alpha()
            else :
                self.image = pygame.image.load(
                    DEVICE_TRY_TO_CONNECT_DOWN_IMAGE
                ).convert_alpha()
        elif self.status == CONNECTED:
            if self.command == COMMAND_UP:
                self.image = pygame.image.load(
                    DEVICE_CONNECTED_UP_IMAGE).convert_alpha()
            else :
                self.image = pygame.image.load(
                    DEVICE_CONNECTED_DOWN_IMAGE).convert_alpha()
        else :
            self.image = pygame.image.load(
                DEVICE_DISCONNECTED_IMAGE).convert_alpha()
