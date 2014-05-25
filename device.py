#-*-coding:utf-8 -*

from threading import Lock
import random
import pygame
from pygame.locals import *

from shared_resources import devices
from constants import *

from math import *

#TODO : inherit device class to differentiate the antenna device from
#the UE devices

class Device(object):

    def __init__(self, (x, y)):
        self.mutex = Lock()
        self.abscisse = x
        self.ordonnee = y
        self.distance_from_antenna = 0.0
        self.current_emitted_power = 0.0
        self.current_command = COMMAND_UP
        self.connexion_status = NOT_CONNECTED
        # Object which will contain the picture descriptor assigned to the
        # device.
        self.current_picture = None

    def set_picture(self, picturepath):
        """To be used to assign the antenna picture
        """
        self.current_picture = pygame.image.load(picturepath).convert_alpha()


class Antenna(Device):
    """Antenna."""

    def __init(self, (x, y)):
        Device.__init__(self, (x, y))


class UE(Device):
    """User Equipment."""

    def __init(self, (x, y)):
        Device.__init__(self, (x, y))
        self.distance_from_antenna = self.compute_distance_from_antenna()
        # Set the initial emitted power to the min.
        self.current_emitted_power = UE_MIN_EMITTED_POWER
        self.current_command = COMMAND_UP
        self.connexion_status = TRY_CONNECT
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
        distance_x = abs(devices[0].abscisse - self.abscisse) * PIX_IN_METERS
        distance_y = abs(devices[0].ordonnee - self.ordonnee) * PIX_IN_METERS
        return sqrt(pow(distance_x,2) + pow(distance_y,2))

    def set_coor_random(self):
        """Randomly set the coordinates of the UE."""
        while True:
            # Randomly generate the (x, y) coordinates of the new device.
            x_coor = random.randint(0, GRID_HEIGHT)
            x_coor -= x_coor % CELL_HEIGHT
            y_coor = random.randint(0, GRID_HEIGHT)
            y_coor -= y_coor % CELL_WIDTH
            # A mobile device cannot be onto the antenna
            if (x_coor == devices[0].abscisse and
                    y_coor == devices[0].ordonnee):
                continue
            break
        self.abscisse = x_coor
        self.ordonnee = y_coor
        self.distance_from_antenna = self.compute_distance_from_antenna()

    def set_coor_close(self):
        """Set coordinates close from the antenna."""
        MAX_DISTANCE = 200
        while True:
            # Randomly generate the (x, y) coordinates of the new device.
            x_coor = random.randint(0, GRID_HEIGHT)
            x_coor -= x_coor % CELL_HEIGHT
            y_coor = random.randint(0, GRID_HEIGHT)
            y_coor -= y_coor % CELL_WIDTH
            # A mobile device cannot be onto the antenna
            if (x_coor == devices[0].abscisse and
                    y_coor == devices[0].ordonnee):
                continue
            # Circle: (x - a)^2 + (y - b)^2 = r^2
            if ((x_coor - devices[0].abscisse) ** 2 +
                    (y_coor - devices[0].ordonnee) ** 2 > MAX_DISTANCE ** 2):
                continue
            break
        self.abscisse = x_coor
        self.ordonnee = y_coor
        self.distance_from_antenna = self.compute_distance_from_antenna()

    def set_coor_far(self):
        """Set coordinates far from the antenna."""
        MIN_DISTANCE = 200
        while True:
            # Randomly generate the (x, y) coordinates of the new device.
            x_coor = random.randint(0, GRID_HEIGHT)
            x_coor -= x_coor % CELL_HEIGHT
            y_coor = random.randint(0, GRID_HEIGHT)
            y_coor -= y_coor % CELL_WIDTH
            # A mobile device cannot be onto the antenna
            if (x_coor == devices[0].abscisse and
                    y_coor == devices[0].ordonnee):
                continue
            # Circle: (x - a)^2 + (y - b)^2 = r^2
            if ((x_coor - devices[0].abscisse) ** 2 +
                    (y_coor - devices[0].ordonnee) ** 2 < MIN_DISTANCE ** 2):
                continue
            break
        self.abscisse = x_coor
        self.ordonnee = y_coor
        self.distance_from_antenna = self.compute_distance_from_antenna()

    def set_command_up(self):
        """Set the current_command of the device to COMMAND_UP.

        Update the image assigned to the device.

        """
        self.current_command = COMMAND_UP
        if self.connexion_status == TRY_CONNECT:
            self.current_picture = pygame.image.load(
                PICTURE_PATH + DEVICE_TRY_TO_CONNECT_UP_IMAGE).convert_alpha()
        elif self.connexion_status == CONNECTED:
            self.current_picture = pygame.image.load(
                PICTURE_PATH + DEVICE_CONNECTED_UP_IMAGE).convert_alpha()
        else :
            self.current_picture = pygame.image.load(
                PICTURE_PATH + DEVICE_DISCONNECTED_IMAGE).convert_alpha()

    def set_command_down(self):
        """Set the current_command of the device to COMMAND_DOWN.

        Update the image assigned to the device.

        """
        self.current_command = COMMAND_DOWN
        if self.connexion_status == TRY_CONNECT:
            self.current_picture = pygame.image.load(
                PICTURE_PATH + DEVICE_TRY_TO_CONNECT_DOWN_IMAGE).convert_alpha()
        elif self.connexion_status == CONNECTED:
            self.current_picture = pygame.image.load(
                PICTURE_PATH + DEVICE_CONNECTED_DOWN_IMAGE).convert_alpha()
        else :
            self.current_picture = pygame.image.load(
                PICTURE_PATH + DEVICE_DISCONNECTED_IMAGE).convert_alpha()

    def set_device_connected(self):
        """Set the connexion_status of the device to CONNECTED.

        Update the image assigned to the device.

        """
        self.connexion_status = CONNECTED
        if self.current_command == COMMAND_UP:
            self.current_picture = pygame.image.load(
                PICTURE_PATH + DEVICE_CONNECTED_UP_IMAGE).convert_alpha()
        else :
            self.current_picture = pygame.image.load(
                PICTURE_PATH + DEVICE_CONNECTED_DOWN_IMAGE).convert_alpha()

    def set_device_trying_to_connect(self):
        """Set the connexion_status of the device to TRY_CONNECT.

        Update the image assigned to the device.

        """
        self.connexion_status = TRY_CONNECT
        if self.current_command == COMMAND_UP:
            self.current_picture = pygame.image.load(
                PICTURE_PATH + DEVICE_TRY_TO_CONNECT_UP_IMAGE).convert_alpha()
        else :
            self.current_picture = pygame.image.load(
                PICTURE_PATH + DEVICE_TRY_TO_CONNECT_DOWN_IMAGE).convert_alpha()

    def set_device_disconnected(self):
        """Set the connexion_status of the device to NOT_CONNECTED.

        Update the image assigned to the device.

        """
        self.connexion_status = NOT_CONNECTED
        self.current_picture = pygame.image.load(
            PICTURE_PATH + DEVICE_DISCONNECTED_IMAGE
        ).convert_alpha()

    def reload(self):
        """Reload the current picture.

        According to connection status and current command.

        """
        if self.connexion_status == TRY_CONNECT:
            if self.current_command == COMMAND_UP:
                self.current_picture = pygame.image.load(
                    PICTURE_PATH + DEVICE_TRY_TO_CONNECT_UP_IMAGE
                ).convert_alpha()
            else :
                self.current_picture = pygame.image.load(
                    PICTURE_PATH + DEVICE_TRY_TO_CONNECT_DOWN_IMAGE
                ).convert_alpha()
        elif self.connexion_status == CONNECTED:
            if self.current_command == COMMAND_UP:
                self.current_picture = pygame.image.load(
                    PICTURE_PATH + DEVICE_CONNECTED_UP_IMAGE).convert_alpha()
            else :
                self.current_picture = pygame.image.load(
                    PICTURE_PATH + DEVICE_CONNECTED_DOWN_IMAGE).convert_alpha()
        else :
            self.current_picture = pygame.image.load(
                PICTURE_PATH + DEVICE_DISCONNECTED_IMAGE).convert_alpha()
