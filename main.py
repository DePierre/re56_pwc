#!/usr/bin/python3
#-*-coding:utf-8 -*

import os

#import pygame lib
import pygame
#use namespace for pygame csts
from pygame.locals import *

from Constants import *

#initialize modules
pygame.init()

#declare a variable window and create a new window of 800x800
#this window is not sizable
window = pygame.display.set_mode((MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT))

from Device import *
from Menu import *


#variable used to stop the window
stop = 0

#initialize background image
background = pygame.image.load(PICTURE_PATH + BACKGROUND_IMAGE).convert_alpha()
#place antenna at the very center
Antenna = Device((GRID_WIDTH / 2 - CELL_WIDTH,GRID_HEIGHT / 2 - CELL_HEIGHT), PICTURE_PATH + ANTENNA_IMAGE)
background.blit(Antenna.current_picture, (Antenna.abscisse, Antenna.ordonnee))
#initialize the menu and select the first menu item
Menu = Menu()


#waiting loop 
while not stop:
	#foreach event from pygame window
	for event in pygame.event.get():
		#if event is of type quit (ALT + F4 or click on quit)
		if event.type == QUIT :
			stop = 1
		
		#manage selection of the menu item
		if event.type == KEYDOWN:
			if event.key == K_DOWN:
				Menu.menu_next()
			elif event.key == K_UP:
				Menu.menu_previous()
			
			#keypad enter or enter
			elif event.key == K_KP_ENTER or K_RETURN:
				#raise exception to distribute again the devices into the grid
				print "Feature not implemented yet. Sorry."
	
	#reload window
	window.fill( (0,0,0) )
	window.blit(background, (0,0))
	window.blit(Menu.surface, (GRID_WIDTH,0))

	#refresh
	pygame.display.flip()
	
	
	#TODO
	#implement generation of each distribution from list of devices
	
