# -*-coding:utf-8 -*-

import pygame
from pygame.locals import *


from constants import *


class Menu_Item(object):
    # Default coord of the menu_item 1.
    x = MENU_ITEM_OFFSET_FROM_LEFT_RIGHT_PANEL_SIDE
    y = MENU_OFFSET_FROM_TOP_RIGHT_PANEL
    # This object will contain the image corresponding to a menu item not
    # selected.
    image = 0
    image_path_unsel  = ""
    image_path_sel = ""
    is_selected = False

    def __init__(self,
                 (width, height),
                 image_path_unselected,
                 image_path_selected):
        self.x = width
        self.y = height
        self.image_path_unsel = image_path_unselected
        self.image_path_sel = image_path_selected
        self.image = pygame.image.load(
            image_path_unselected)

    def select(self):
        """Set the right image to the menu item."""
        self.image.fill((0,0,0))
        self.image = pygame.image.load(self.image_path_sel)
        self.is_selected = True

    def unselect(self):
        self.image.fill((0,0,0))
        self.image = pygame.image.load(
            self.image_path_unsel)
        self.is_selected = False

    def change_image_selected(self, image_path):
        """Change images assigned to this item."""
        self.image.fill((0,0,0))
        self.image_path_sel = image_path

    def change_image_unselected(self, image_path):
        self.image.fill((0,0,0))
        self.image_path_unsel = image_path

    def reload_image(self):
        self.image.fill((0,0,0))
        if self.is_selected:
            self.image = pygame.image.load(image_path_sel)
        else :
            self.image = pygame.image.load(image_path_unsel)


class Menu(object):
    items = [
        Menu_Item(
            (MENU_ITEM_OFFSET_FROM_LEFT_RIGHT_PANEL_SIDE, MENU_OFFSET_FROM_TOP_RIGHT_PANEL),
            MENU_SELECTION1_IMAGE,
            MENU_SELECTION1_SELECTED_IMAGE),
        Menu_Item(
            (MENU_ITEM_OFFSET_FROM_LEFT_RIGHT_PANEL_SIDE, MENU_OFFSET_FROM_TOP_RIGHT_PANEL + MENU_ITEM_HEIGHT),
            MENU_SELECTION2_IMAGE,
            MENU_SELECTION2_SELECTED_IMAGE),
        Menu_Item(
            (MENU_ITEM_OFFSET_FROM_LEFT_RIGHT_PANEL_SIDE, MENU_OFFSET_FROM_TOP_RIGHT_PANEL + 2*MENU_ITEM_HEIGHT),
            MENU_SELECTION3_IMAGE,
            MENU_SELECTION3_SELECTED_IMAGE)]
    arrow_selector = pygame.image.load(
        ARROW_SELECTOR_IMAGE)
    surface = pygame.image.load(
        RIGHT_PANEL_IMAGE)
    menu_pointed = MENU3_INDEX

    def __init__(self, simulator):
        self.simu = simulator
        self.init = False
        self.select_menu(MENU3_INDEX)

    def select_menu(self, index):
        """Place the arrow selector beside the menu item indexed 'index'."""
        for item in self.items:
            if item.is_selected:
                item.unselect()
        self.items[index].select()
        if self.init:
            self.force_distribution(index)
        self.init = True
        self.refresh()

    def force_distribution(self, index):
        """Regenerate the mobile distribution according to the selected
        scenario.

        index = 1: Close distribution
        index = 2: Far distribution
        index = 3: Random distribution

        """
        if index == MENU1_INDEX:
            self.simu.close_distribution()
        elif index == MENU2_INDEX:
            self.simu.far_distribution()
        else:
            self.simu.random_distribution()

    def refresh(self):
        """Reload each image of menu."""
        self.surface.fill((0,0,0))
        self.surface = pygame.image.load(RIGHT_PANEL_IMAGE)
        # Load each image to the surface.
        for item in self.items:
            self.surface.blit(
                item.image,
                (item.x, item.y))
        # Load image of arrow selector beside the menu item selected.
        self.surface.blit(
            self.arrow_selector, (
                self.items[self.menu_pointed].x +
                ARROW_SELECTOR_WIDTH_OFFSET_FROM_MENU_ITEM,
                self.items[self.menu_pointed].y +
                ARROW_SELECTOR_HEIGHT_OFFSET_FROM_MENU_ITEM
            ))

    def get_index_menu_selected(self):
        """Get index of the menu selected."""
        for index, item in enumerate(self.items):
            if item.is_selected :
                return index

    def menu_next(self):
        """Select the next menu item in the list."""
        self.menu_pointed += 1
        if self.menu_pointed >= len(self.items):
            self.menu_pointed = 0
        self.refresh()

    def menu_previous(self):
        """Select the previous menu item in the list."""
        self.menu_pointed -= 1
        if self.menu_pointed < 0:
            self.menu_pointed = len(self.items) - 1
        self.refresh()
