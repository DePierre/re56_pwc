#!/usr/bin/python2
#-*-coding:utf-8 -*

import os

import copy
import thread
import workers
import pygame
from pygame.locals import *

from shared_resources import devices
from constants import *

pygame.init()

# Declare a variable window and create a new window of 1220x720 this window is
# not sizable.
window = pygame.display.set_mode((MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT))

from device import Device
from menu import Menu

# Variable used to stop the window.
stop = False

# Initialize background image.
background = pygame.image.load(PICTURE_PATH + BACKGROUND_SCALED_IMAGE).convert_alpha()
# Place antenna at the very center.
antenna = Device(
    (ANTENNA_LOC_WIDTH,ANTENNA_LOC_HEIGHT))
antenna.set_picture(PICTURE_PATH + ANTENNA_IMAGE)
antenna.current_emitted_power = ANTENNA_EMITTED_POWER
background.blit(antenna.current_picture, (antenna.abscisse, antenna.ordonnee))
#declare a copy of bakground which will be used to update the screen
tmp_background = copy.copy(background)

# List of devices which is used to manage connection and display
devices.append(antenna)

# Initialize the menu and select the first menu item.
menu = Menu()

#initialize the worker thread
try:
    worker = thread.start_new_thread(workers.open_loop, ())
except Exception as errtxt:
    print errtxt
    stop = True


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
                # Raise exception to distribute again the devices into the
                # grid.
                #print "Feature not implemented yet. Sorry."
                menu.select_menu(menu.menu_pointed)
                
    # Reload window
    tmp_background = copy.copy(background) # Reset tmp_background to initial background
    for device in devices:
        tmp_background.blit(device.current_picture,
                            (device.abscisse, device.ordonnee))
    window.fill((0,0,0))
    window.blit(tmp_background, (0,0))
    window.blit(menu.surface, (GRID_WIDTH,0))

    # Refresh
    pygame.display.flip()

