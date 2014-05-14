#-*-coding:utf-8 -*

import pygame
from pygame.locals import *

from constants import *

from math import *


class Device:
        abscisse = 0
        ordonnee = 0
        distance_from_antenna = 0.0
        current_emitted_power = 0.0
        current_command = COMMAND_UP
        connexion_status = NOT_CONNECTED
        # Object which will contain the picture descriptor assigned to the
        # device.
        current_picture = 0

        def __init__(self, (x, y), PicturePath):
            self.abscisse = x
            self.ordonnee = y
            self.current_emitted_power = 0.0
            self.current_command = COMMAND_UP
            self.connexion_status = NOT_CONNECTED
            self.current_picture = pygame.image.load(
                PicturePath).convert_alpha()
        
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
            distance_x = abs(ANTENNA_LOC_WIDTH - self.abscisse)
            distance_y = abs(ANTENNA_LOC_HEIGHT - self.ordonnee)
            return sqrt(pow(distance_x,2) + pow(distance_y,2))
            
            
            
        def set_command_up(self):
            """Set the current_command of the device to COMMAND_UP.

            Update the image assigned to the device.

            """
            self.current_command = COMMAND_UP
            if self.connexion_status == TRY_CONNECT:
                self.current_picture = pygame.image.load(
                    DEVICE_TRY_TO_CONNECT_UP_IMAGE).convert_alpha()
            elif self.connexion_status == CONNECTED:
                self.current_picture = pygame.image.load(
                    DEVICE_CONNECTED_UP_IMAGE).convert_alpha()
            else :
                self.current_picture = pygame.image.load(
                    DEVICE_DISCONNECTED_IMAGE).convert_alpha()

        def set_command_down(self):
            """Set the current_command of the device to COMMAND_DOWN.

            Update the image assigned to the device.

            """
            self.current_command = COMMAND_DOWN
            if self.connexion_status == TRY_CONNECT:
                self.current_picture = pygame.image.load(
                    DEVICE_TRY_TO_CONNECT_DOWN_IMAGE).convert_alpha()
            elif self.connexion_status == CONNECTED:
                self.current_picture = pygame.image.load(
                    DEVICE_CONNECTED_DOWN_IMAGE).convert_alpha()
            else :
                self.current_picture = pygame.image.load(
                    DEVICE_DISCONNECTED_IMAGE).convert_alpha()

        def set_device_connected(self):
            """Set the connexion_status of the device to CONNECTED.

            Update the image assigned to the device.

            """
            self.connexion_status = CONNECTED
            if self.current_command == COMMAND_UP:
                self.current_picture = pygame.image.load(
                    DEVICE_CONNECTED_UP_IMAGE).convert_alpha()
            else :
                self.current_picture = pygame.image.load(
                    DEVICE_CONNECTED_DOWN_IMAGE).convert_alpha()

        def set_device_trying_to_connect(self):
            """Set the connexion_status of the device to TRY_CONNECT.

            Update the image assigned to the device.

            """
            self.connexion_status = TRY_CONNECT
            if self.current_command == COMMAND_UP:
                self.current_picture = pygame.image.load(
                    DEVICE_TRY_TO_CONNECT_UP_IMAGE).convert_alpha()
            else :
                self.current_picture = pygame.image.load(
                    DEVICE_TRY_TO_CONNECT_DOWN_IMAGE).convert_alpha()

        def set_device_disconnected(self):
            """Set the connexion_status of the device to NOT_CONNECTED.

            Update the image assigned to the device.

            """
            self.connexion_status = NOT_CONNECTED
            self.current_picture = pygame.image.load(
                DEVICE_DISCONNECTED_IMAGE).convert_alpha()
