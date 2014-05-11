# -*-coding:utf-8 -*-

import pygame
from pygame.locals import *

from constants import *


class Menu_Item(object):
    # Default coord of the menu_item 1.
    abscisse = 770
    ordonnee = 570
    # This object will contain the picture corresponding to a menu item not
    # selected.
    picture = 0
    PicturePath_unsel  = ""
    PicturePath_sel = ""
    is_selected = False

    def __init__(self,
                 (width, height),
                 PicturePath_unselected,
                 PicturePath_selected):
        self.abscisse = width
        self.ordonnee = height
        self.PicturePath_unsel = PicturePath_unselected
        self.PicturePath_sel = PicturePath_selected
        self.picture = pygame.image.load(
            PicturePath_unselected).convert_alpha()

    def select(self):
        """Set the right image to the menu item."""
        self.picture.fill((0,0,0))
        self.picture = pygame.image.load(self.PicturePath_sel).convert_alpha()
        self.is_selected = True

    def unselect(self):
        self.picture.fill((0,0,0))
        self.picture = pygame.image.load(
            self.PicturePath_unsel).convert_alpha()
        self.is_selected = False

    def change_picture_selected(self, PicturePath):
        """Change pictures assigned to this item."""
        self.picture.fill((0,0,0))
        self.PicturePath_sel = PicturePath

    def change_picture_unselected(self, PicturePath):
        self.picture.fill((0,0,0))
        self.PicturePath_unsel = PicturePath

    def reload_picture(self):
        self.picture.fill((0,0,0))
        if self.is_selected:
            self.picture = pygame.image.load(PicturePath_sel).convert_alpha()
        else :
            self.picture = pygame.image.load(PicturePath_unsel).convert_alpha()



class Menu(object):
    items = [
        Menu_Item(
            (770, 570),
            PICTURE_PATH + MENU_SELECTION1_IMAGE,
            PICTURE_PATH + MENU_SELECTION1_SELECTED_IMAGE),
        Menu_Item(
            (770, 620),
            PICTURE_PATH + MENU_SELECTION2_IMAGE,
            PICTURE_PATH + MENU_SELECTION2_SELECTED_IMAGE),
        Menu_Item(
            (770, 670),
            PICTURE_PATH + MENU_SELECTION3_IMAGE,
            PICTURE_PATH + MENU_SELECTION3_SELECTED_IMAGE)]
    arrow_selector = pygame.image.load(
        PICTURE_PATH + ARROW_SELECTOR_IMAGE).convert_alpha()
    surface = pygame.image.load(
        PICTURE_PATH + RIGHT_PANEL_IMAGE).convert_alpha()

    def __init__(self)	:
        self.select_menu(MENU1_INDEX)


    def select_menu(self, index):
        """Place the arrow selector beside the menu item indexed 'index'."""
        for item in self.items:
            if item.is_selected:
                item.unselect()
            self.items[index].select()
            self.load()

    def load(self):
        self.surface.fill((0,0,0))
        self.surface = pygame.image.load(
            PICTURE_PATH + RIGHT_PANEL_IMAGE).convert_alpha()
        # Load each image to the surface.
        for item in self.items:
            self.surface.blit(
                item.picture,
                (item.abscisse - 720, item.ordonnee))
        # Load image of arrow selector beside the menu item selected.
        for item in self.items:
            if item.is_selected:
                self.surface.blit(
                    self.arrow_selector, (
                        item.abscisse +
                        ARROW_SELECTOR_WIDTH_OFFSET_FROM_MENU_ITEM -
                        720,
                        item.ordonnee +
                        ARROW_SELECTOR_HEIGHT_OFFSET_FROM_MENU_ITEM
                    ))
                break

    def get_index_menu_selected(self):
        """Get index of the menu selected."""
        for index, item in enumerate(self.items):
            if item.is_selected :
                return index
            break

    def menu_next(self):
        """Select the next menu item in the list."""
        index = self.get_index_menu_selected()
        index += 1
        if index >= len(self.items):
            index = 0
        self.select_menu(index)

    def menu_previous(self):
        """Select the previous menu item in the list."""
        index = self.get_index_menu_selected()
        index -= 1
        if index < 0:
            index = len(self.items) - 1
        self.select_menu(index)
