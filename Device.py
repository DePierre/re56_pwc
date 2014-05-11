#!/usr/bin/python
#-*-coding:utf-8 -*

#import pygame lib
import pygame
#use namespace for pygame csts
from pygame.locals import *

#import constants
from Constants import *


class Device:
	abscisse = 0
	ordonnee = 0
	current_emitted_power = 0.0
	current_command = COMMAND_UP
	connexion_status = NOT_CONNECTED
	current_picture = 0	#object which will contain the picture descriptor assigned to the device
	
	#default constructor
	def __init__(self, (x, y), PicturePath):
		self.abscisse = x
		self.ordonnee = y
		self.current_emitted_power = 0.0
		self.current_command = COMMAND_UP
		self.connexion_status = NOT_CONNECTED
		self.current_picture = pygame.image.load(PicturePath).convert_alpha()
	
	#set the current_command of the device to COMMAND_UP & update the image assigned to the device
	def set_command_up(self):
		self.current_command = COMMAND_UP
		#didn't find any switch/case statements so i used if/elif instead of switch/case
		if self.connexion_status == TRY_CONNECT:
			self.current_picture = pygame.image.load(DEVICE_TRY_TO_CONNECT_UP_IMAGE).convert_alpha()
		elif self.connexion_status == CONNECTED:
			self.current_picture = pygame.image.load(DEVICE_CONNECTED_UP_IMAGE).convert_alpha()
		else :
			self.current_picture = pygame.image.load(DEVICE_DISCONNECTED_IMAGE).convert_alpha()
			
	#set the current_command of the device to COMMAND_DOWN & update the image assigned to the device
	def set_command_down(self):
		self.current_command = COMMAND_DOWN
		#didn't find any switch/case statements so i used if/elif instead of switch/case
		if self.connexion_status == TRY_CONNECT:
			self.current_picture = pygame.image.load(DEVICE_TRY_TO_CONNECT_DOWN_IMAGE).convert_alpha()
		elif self.connexion_status == CONNECTED:
			self.current_picture = pygame.image.load(DEVICE_CONNECTED_DOWN_IMAGE).convert_alpha()
		else :
			self.current_picture = pygame.image.load(DEVICE_DISCONNECTED_IMAGE).convert_alpha()
	
	#set the connexion_status of the device to CONNECTED & update the image assigned to the device
	def set_device_connected(self):
		self.connexion_status = CONNECTED
		if self.current_command == COMMAND_UP:
			self.current_picture = pygame.image.load(DEVICE_CONNECTED_UP_IMAGE).convert_alpha()
		else :
			self.current_picture = pygame.image.load(DEVICE_CONNECTED_DOWN_IMAGE).convert_alpha()
	
	#set the connexion_status of the device to TRY_CONNECT & update the image assigned to the device			
	def set_device_trying_to_connect(self):
		self.connexion_status = TRY_CONNECT
		if self.current_command == COMMAND_UP:
			self.current_picture = pygame.image.load(DEVICE_TRY_TO_CONNECT_UP_IMAGE).convert_alpha()
		else :
			self.current_picture = pygame.image.load(DEVICE_TRY_TO_CONNECT_DOWN_IMAGE).convert_alpha()
	
	#set the connexion_status of the device to NOT_CONNECTED & update the image assigned to the device	
	def set_device_disconnected(self):
		self.connexion_status = NOT_CONNECTED
		self.current_picture = pygame.image.load(DEVICE_DISCONNECTED_IMAGE).convert_alpha()
		
	
