#!/usr/bin/python2
#-*-coding:utf-8 -*

import os
from copy import copy

import pygame
from pygame.locals import *

from shared_resources import devices
from workers import Worker
from constants import *

pygame.init()

# Declare a variable window and create a new window of 1220x720 this window is
# not sizable.
window = pygame.display.set_mode((MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT))

from device import Antenna
from menu import Menu

# Variable used to stop the window.
stop = False

# Initialize background image.
background = pygame.image.load(PICTURE_PATH + BACKGROUND_SCALED_IMAGE).convert_alpha()
# Place antenna at the very center.
antenna = Antenna((ANTENNA_LOC_WIDTH, ANTENNA_LOC_HEIGHT))
antenna.set_picture(PICTURE_PATH + ANTENNA_IMAGE)
antenna.current_emitted_power = ANTENNA_EMITTED_POWER
background.blit(antenna.current_picture, (antenna.abscisse, antenna.ordonnee))
#declare a copy of bakground which will be used to update the screen
tmp_background = copy(background)

# List of devices which is used to manage connection and display
devices.append(antenna)

# Initialize the menu and select the first menu item.
menu = Menu()


worker = Worker()
worker.start()


# Waiting loop.
while not stop:
    for event in pygame.event.get():
        # quit (ALT + F4 or click on quit).
        if event.type == QUIT :
            stop = True
        # Manage selection of the menu item
        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                menu.menu_next()
            elif event.key == K_UP:
                menu.menu_previous()
            # keypad enter or enter
            elif event.key == K_KP_ENTER or K_RETURN:
                # Update the selected item of the menu.
                worker.join()
                menu.select_menu(menu.menu_pointed)
                worker = Worker()
                worker.start()

    # Reload window
    tmp_background = copy(background) # Reset tmp_background to initial background
    for device in devices:
        tmp_background.blit(
            device.current_picture,
            (device.abscisse, device.ordonnee))
    window.fill((0,0,0))
    window.blit(tmp_background, (0,0))
    window.blit(menu.surface, (GRID_WIDTH,0))

    # Refresh
    pygame.display.flip()
