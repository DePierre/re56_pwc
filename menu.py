# -*-coding:utf-8 -*-

import random
import pygame
from pygame.locals import *


from shared_resources import devices
from constants import *
from device import Device


class Menu_Item(object):
    # Default coord of the menu_item 1.
    abscisse = MENU_ITEM_OFFSET_FROM_LEFT_RIGHT_PANEL_SIDE
    ordonnee = MENU_OFFSET_FROM_TOP_RIGHT_PANEL
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
            (MENU_ITEM_OFFSET_FROM_LEFT_RIGHT_PANEL_SIDE, MENU_OFFSET_FROM_TOP_RIGHT_PANEL),
            PICTURE_PATH + MENU_SELECTION1_IMAGE,
            PICTURE_PATH + MENU_SELECTION1_SELECTED_IMAGE),
        Menu_Item(
            (MENU_ITEM_OFFSET_FROM_LEFT_RIGHT_PANEL_SIDE, MENU_OFFSET_FROM_TOP_RIGHT_PANEL + MENU_ITEM_HEIGHT),
            PICTURE_PATH + MENU_SELECTION2_IMAGE,
            PICTURE_PATH + MENU_SELECTION2_SELECTED_IMAGE),
        Menu_Item(
            (MENU_ITEM_OFFSET_FROM_LEFT_RIGHT_PANEL_SIDE, MENU_OFFSET_FROM_TOP_RIGHT_PANEL + 2*MENU_ITEM_HEIGHT),
            PICTURE_PATH + MENU_SELECTION3_IMAGE,
            PICTURE_PATH + MENU_SELECTION3_SELECTED_IMAGE)]
    arrow_selector = pygame.image.load(
        PICTURE_PATH + ARROW_SELECTOR_IMAGE).convert_alpha()
    surface = pygame.image.load(
        PICTURE_PATH + RIGHT_PANEL_IMAGE).convert_alpha()
    menu_pointed = MENU1_INDEX

    def __init__(self):
        self.select_menu(MENU3_INDEX)
        self.force_distribution(MENU3_INDEX)

    def select_menu(self, index):
        """Place the arrow selector beside the menu item indexed 'index'."""
        for item in self.items:
            if item.is_selected:
                item.unselect()
        self.items[index].select()
        self.force_distribution(index)
        self.refresh()

    def force_distribution(self, index):
        """Regenerate the mobile distribution according to the selected
        scenario.

        index = 1: Close distribution
        index = 2: Far distribution
        index = 3: Random distribution

        """
        # HACK: Clean the previous list while keeping the reference
        while True:
            if len(devices) == 1:
                break
            devices.pop()
        if index == MENU1_INDEX:
            self.close_distribution()
            pygame.display.set_caption("close distribution")
        elif index == MENU2_INDEX:
            self.far_distribution()
            pygame.display.set_caption("far distribution")
        else:
            self.random_distribution()
            pygame.display.set_caption("random distribution")

    def close_distribution(self):
        """Create MAX_DEVICES devices close to the antenna on the grid."""
        MAX_DISTANCE = 200
        while len(devices) < MAX_DEVICES + 1:
            # Randomly generate the (x, y) coordinates of the new device.
            x_coor = random.randint(0, GRID_HEIGHT)
            x_coor -= x_coor % CELL_HEIGHT
            y_coor = random.randint(0, GRID_HEIGHT)
            y_coor -= y_coor % CELL_WIDTH
            # A mobile device cannot be onto the antenna
            if (x_coor == devices[0].abscisse and
                    y_coor == devices[0].ordonnee):
                continue
            # Circle: (x - a)^2 + (y - b)^2 = r^2
            if ((x_coor - devices[0].abscisse) ** 2 +
                    (y_coor - devices[0].ordonnee) ** 2 > MAX_DISTANCE ** 2):
                continue
            # Create the new device
            new_device = Device(
                (x_coor, y_coor))
            # set the initial emitted power to the min
            new_device.current_emitted_power = UE_MIN_EMITTED_POWER
            # Add the new device to the list of devices
            devices.append(new_device)

    def far_distribution(self):
        """Create MAX_DEVICES devices far from the antenna on the grid."""
        MIN_DISTANCE = 200
        while len(devices) < MAX_DEVICES + 1:
            # Randomly generate the (x, y) coordinates of the new device.
            x_coor = random.randint(0, GRID_HEIGHT)
            x_coor -= x_coor % CELL_HEIGHT
            y_coor = random.randint(0, GRID_HEIGHT)
            y_coor -= y_coor % CELL_WIDTH
            # A mobile device cannot be onto the antenna
            if (x_coor == devices[0].abscisse and
                    y_coor == devices[0].ordonnee):
                continue
            # Circle: (x - a)^2 + (y - b)^2 = r^2
            if ((x_coor - devices[0].abscisse) ** 2 +
                    (y_coor - devices[0].ordonnee) ** 2 < MIN_DISTANCE ** 2):
                continue
            # Create the new device
            new_device = Device(
                (x_coor, y_coor))
            # set the initial emitted power to the min
            new_device.current_emitted_power = UE_MIN_EMITTED_POWER
            # Add the new device to the list of devices
            devices.append(new_device)

    def random_distribution(self):
        """Create MAX_DEVICES devices randomly on the grid."""
        while len(devices) < MAX_DEVICES + 1:
            # Randomly generate the (x, y) coordinates of the new device.
            x_coor = random.randint(0, GRID_HEIGHT)
            x_coor -= x_coor % CELL_HEIGHT
            y_coor = random.randint(0, GRID_HEIGHT)
            y_coor -= y_coor % CELL_WIDTH
            # A mobile device cannot be onto the antenna
            if (x_coor == devices[0].abscisse and
                    y_coor == devices[0].ordonnee):
                continue
            # Create the new device
            new_device = Device(
                (x_coor, y_coor))
            # set the initial emitted power to the min
            new_device.current_emitted_power = UE_MIN_EMITTED_POWER
            # Add the new device to the list of devices
            devices.append(new_device)

    def refresh(self):
        """Reload each image of menu."""
        self.surface.fill((0,0,0))
        self.surface = pygame.image.load(
            PICTURE_PATH + RIGHT_PANEL_IMAGE).convert_alpha()
        # Load each image to the surface.
        for item in self.items:
            self.surface.blit(
                item.picture,
                (item.abscisse, item.ordonnee))
        # Load image of arrow selector beside the menu item selected.
        self.surface.blit(
            self.arrow_selector, (
                self.items[self.menu_pointed].abscisse +
                ARROW_SELECTOR_WIDTH_OFFSET_FROM_MENU_ITEM,
                self.items[self.menu_pointed].ordonnee +
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
