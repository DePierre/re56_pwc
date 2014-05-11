#!/usr/Bin/python
#-*-coding:utf-8 -*

#import pygame lib
import pygame
#use namespace for pygame csts
from pygame.locals import *

#import constants definitions
from Constants import *



class Menu_Item:
	#default coord of the menu_item 1
	abscisse = 770
	ordonnee = 570
	picture = 0 	#this object will contain the picture corresponding to a menu item not selected
	PicturePath_unsel  = ""
	PicturePath_sel = ""
	is_selected = FALSE
	
	#default constructor
	def __init__(self, (width, height), PicturePath_unselected, PicturePath_selected):
		self.abscisse = width
		self.ordonnee = height
		self.PicturePath_unsel = PicturePath_unselected
		self.PicturePath_sel = PicturePath_selected 
		self.picture = pygame.image.load(PicturePath_unselected).convert_alpha()
		
		
	#set the right image to the menu item
	def select(self):
		self.picture.fill( (0,0,0) )
		self.picture = pygame.image.load(self.PicturePath_sel).convert_alpha()
		self.is_selected = TRUE
		
	def unselect(self):
		self.picture.fill( (0,0,0) )
		self.picture = pygame.image.load(self.PicturePath_unsel).convert_alpha()
		self.is_selected = FALSE
	
	#change pictures assigned to this item
	def change_picture_selected(self, PicturePath):
		self.picture.fill( (0,0,0) )
		self.PicturePath_sel = PicturePath
		
	def change_picture_unselected(self, PicturePath):		
		self.picture.fill( (0,0,0) )
		self.PicturePath_unsel = PicturePath
		
	def reload_picture(self):
		self.picture.fill( (0,0,0) )
		if self.is_selected == TRUE :
			self.picture = pygame.image.load(PicturePath_sel).convert_alpha()
		else :
			self.picture = pygame.image.load(PicturePath_unsel).convert_alpha()
			
		
		
class Menu:
	Items = [ Menu_Item((770, 570), PICTURE_PATH + MENU_SELECTION1_IMAGE, PICTURE_PATH + MENU_SELECTION1_SELECTED_IMAGE), Menu_Item((770, 620), PICTURE_PATH + MENU_SELECTION2_IMAGE, PICTURE_PATH + MENU_SELECTION2_SELECTED_IMAGE), Menu_Item((770, 670), PICTURE_PATH + MENU_SELECTION3_IMAGE, PICTURE_PATH + MENU_SELECTION3_SELECTED_IMAGE) ]
	Arrow_selector = pygame.image.load(PICTURE_PATH + ARROW_SELECTOR_IMAGE).convert_alpha()
	surface = pygame.image.load(PICTURE_PATH + RIGHT_PANEL_IMAGE).convert_alpha()
	
	def __init__(self)	:
		#menu item 1 selected by default
#		self.Items[1].select()
		#load each image to the surface
#		for item in self.Items:
#			self.surface.blit(item.picture, (item.abscisse - 720, item.ordonnee))
		#load image of arrow selector beside the menu item selected by default
#		self.surface.blit(self.Arrow_selector, (self.Items[1].abscisse + ARROW_SELECTOR_WIDTH_OFFSET_FROM_MENU_ITEM - 720, self.Items[1].ordonnee + ARROW_SELECTOR_HEIGHT_OFFSET_FROM_MENU_ITEM))
		self.select_menu(MENU1_INDEX)
		
		
	#place the arrow selector beside the menu item indexed 'index'
	def select_menu(self, index):		
		for item in self.Items:
			if item.is_selected == TRUE:
				item.unselect()
		self.Items[index].select()
		self.load()
	
	def load(self):
		self.surface.fill( (0,0,0))
		self.surface = pygame.image.load(PICTURE_PATH + RIGHT_PANEL_IMAGE).convert_alpha()
		#load each image to the surface
		for item in self.Items:
			self.surface.blit(item.picture, (item.abscisse - 720, item.ordonnee))
		#load image of arrow selector beside the menu item selected
		for item in self.Items:
			if item.is_selected == TRUE:
				self.surface.blit(self.Arrow_selector, (item.abscisse + ARROW_SELECTOR_WIDTH_OFFSET_FROM_MENU_ITEM - 720, item.ordonnee + ARROW_SELECTOR_HEIGHT_OFFSET_FROM_MENU_ITEM))
				break
	
	#get index of the menu selected
	def get_index_menu_selected(self):
		for index, item in enumerate(self.Items):
			if item.is_selected :
				return index
				break
		
	#select the next menu item in the list	
	def menu_next(self):
		index = self.get_index_menu_selected()
		index += 1
		if index >= len(self.Items):
			index = 0
		self.select_menu(index)
		
	#select the previous menu item in the list
	def menu_previous(self):
		index = self.get_index_menu_selected()
		index -= 1
		if index < 0:
			index = len(self.Items) - 1
		self.select_menu(index)
				
				
				
