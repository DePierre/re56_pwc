#!/usr/bin/python2
#-*-coding:utf-8 -*

import os

import pygame
from pygame.locals import *

from constants import *

pygame.init()

# Declare a variable window and create a new window of 800x800 this window is
# not sizable.
window = pygame.display.set_mode((MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT))

from device import *
from menu import *


# Variable used to stop the window.
stop = False

# Initialize background image.
background = pygame.image.load(PICTURE_PATH + BACKGROUND_IMAGE).convert_alpha()
# Place antenna at the very center.
antenna = Device(
    (GRID_WIDTH / 2 - CELL_WIDTH,GRID_HEIGHT / 2 - CELL_HEIGHT),
    PICTURE_PATH + ANTENNA_IMAGE)
background.blit(antenna.current_picture, (antenna.abscisse, antenna.ordonnee))
# Initialize the menu and select the first menu item.
menu = Menu()


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
                print "Feature not implemented yet. Sorry."
    # Reload window
    window.fill((0,0,0))
    window.blit(background, (0,0))
    window.blit(menu.surface, (GRID_WIDTH,0))

    # Refresh
    pygame.display.flip()
    # TODO: Implement generation of each distribution from list of devices.
