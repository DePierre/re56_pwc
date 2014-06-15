# -*-coding:utf-8 -*-
"""

    menu.py

    Define the different element composing the menu of the GUI.

    MenuItem: an item of the menu (i.e. an image and a label).
    Menu: the complete menu of the GUI (i.e. the legend, the images, etc.)

"""


import pygame
from pygame.locals import *

from constants import *


class MenuItem(object):
    """Describe an item of the GUI menu."""

    def __init__(self, id, im_path_unselected, im_path_selected):
        self.x = MENU_ITEM_OFFSET
        self.y = MENU_OFFSET + id * MENU_ITEM_HEIGHT
        self.image_path_unsel = im_path_unselected
        self.image_path_sel = im_path_selected
        self.image = pygame.image.load(im_path_unselected)
        self.is_selected = False

    def select(self):
        """Update the image and the status of the item to selected."""
        self.image.fill((0,0,0))
        self.image = pygame.image.load(self.image_path_sel)
        self.is_selected = True

    def unselect(self):
        """Update the image and the status of the item to unselected."""
        self.image.fill((0,0,0))
        self.image = pygame.image.load(self.image_path_unsel)
        self.is_selected = False


class Menu(object):
    """Describe the complete menu of the GUI."""

    def __init__(self, simulator):
        self.simu = simulator
        self.init = False
        # Create the menu items.
        self.items = [
            MenuItem(0, MENU_CLOSE1_IMAGE, MENU_CLOSE1_SELECTED_IMAGE),
            MenuItem(1, MENU_FAR2_IMAGE, MENU_FAR2_SELECTED_IMAGE),
            MenuItem(2, MENU_RANDOM3_IMAGE, MENU_RANDOM3_SELECTED_IMAGE)]
        self.selected = MENU3_INDEX
        self.arrow_selector = pygame.image.load(ARROW_IMAGE)
        # Create the image legend.
        self.surface = pygame.image.load(RIGHT_PANEL_IMAGE)
        # Create the text legend.
        font = pygame.font.Font(None, 18)
        self.resolution = font.render(
            "1 Squarre : " + str(CELL_RES) + "x" + str(CELL_RES) + " meters",
            1,
            (255, 255, 255))
        font = pygame.font.Font(None, 24)
        self.legend_add = font.render(
            "Press 'a' to add " + str(MAX_NEW_DEVICES) + ' new devices.',
            1,
            (255, 255, 255))
        self.select_menu(self.selected)

    def select_menu(self, index):
        """Place the arrow selector beside the selected item."""
        for item in self.items:
            if item.is_selected:
                item.unselect()
        self.items[index].select()
        if self.init:
            self.force_distribution(index)
        self.init = True
        self.refresh()

    def force_distribution(self, index):
        """Regenerate the distribution according to the selected scenario.

        index = 1: Close distribution.
        index = 2: Far distribution.
        index = 3: Random distribution.

        """
        if index == MENU1_INDEX:
            self.simu.close_distribution()
        elif index == MENU2_INDEX:
            self.simu.far_distribution()
        else:
            self.simu.random_distribution()

    def refresh(self):
        """Reload each image of menu."""
        # Reset.
        self.surface.fill((0,0,0))
        # Image legend.
        self.surface = pygame.image.load(RIGHT_PANEL_IMAGE)
        # Text legend.
        self.surface.blit(self.resolution, (300, 700))
        self.surface.blit(self.legend_add, (40, 300))
        # Load each image to the surface.
        for item in self.items:
            self.surface.blit(item.image, (item.x, item.y))
        # Load image of arrow selector beside the menu item selected.
        self.surface.blit(
            self.arrow_selector, (
            self.items[self.selected].x + ARROW_WIDTH_OFFSET,
            self.items[self.selected].y + ARROW_HEIGHT_OFFSET))

    def menu_next(self):
        """Select the next menu item in the list."""
        self.selected += 1
        if self.selected >= len(self.items):
            self.selected = 0
        self.refresh()

    def menu_previous(self):
        """Select the previous menu item in the list."""
        self.selected -= 1
        if self.selected < 0:
            self.selected = len(self.items) - 1
        self.refresh()
