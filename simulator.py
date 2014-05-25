import pygame
from pygame.locals import *

from copy import copy
from math import log10

from constants import *
from device import Antenna, UE
from menu import Menu


class Simulator(object):
    def __init__(self):
        self._running = True
        self._window = None
        self._bg_original = None
        self._bg = None
        self._menu = None
        self._clock = None
        self.ues = []
        self.weight = MAIN_WINDOW_WIDTH
        self.height = MAIN_WINDOW_HEIGHT
        self.size = (self.weight, self.height)

    def on_init(self):
        pygame.init()
        # Window init.
        self._window = pygame.display.set_mode(self.size)
        # Background init.
        self._bg_original = pygame.image.load(
            BACKGROUND_SCALED_IMAGE)
        self._bg = copy(self._bg_original)
        # Devices init.
        self.antenna = Antenna((ANTENNA_LOC_WIDTH, ANTENNA_LOC_HEIGHT))
        # Menu init.
        self._menu = Menu(self)
        # Clock init
        self._clock = pygame.time.Clock()
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self._menu.menu_next()
            elif event.key == pygame.K_UP:
                self._menu.menu_previous()
            elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                self._menu.select_menu(self._menu.menu_pointed)
                self.open_loop()
            elif event.key == pygame.K_ESCAPE:
                self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        self._bg = copy(self._bg_original)
        self._bg.blit(
            self.antenna.image,
            (self.antenna.x, self.antenna.y))
        for device in self.ues:
            self._bg.blit(
                device.image,
                (device.x, device.y))
        self._window.blit(self._bg, (0, 0))
        self._window.blit(self._menu.surface, (GRID_WIDTH, 0))
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() is False:
            self._running = False

        while self._running:
            self._clock.tick(60)
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def close_distribution(self):
        """Create MAX_DEVICES devices close to the antenna on the grid."""
        pygame.display.set_caption("Close distribution")
        self.ues = []
        while len(self.ues) < MAX_DEVICES + 1:
            # Create the new device
            new_device = UE((0, 0), self.antenna)
            new_device.set_coor_close()
            # Set its image.
            new_device.set_device_trying_to_connect()
            # Add the new device to the list of devices
            self.ues.append(new_device)

    def far_distribution(self):
        """Create MAX_DEVICES devices far from the antenna on the grid."""
        pygame.display.set_caption("Far distribution")
        self.ues = []
        while len(self.ues) < MAX_DEVICES + 1:
            # Create the new device
            new_device = UE((0, 0), self.antenna)
            new_device.set_coor_far()
            # Set its image.
            new_device.set_device_trying_to_connect()
            # Add the new device to the list of devices
            self.ues.append(new_device)

    def random_distribution(self):
        """Create MAX_DEVICES devices randomly on the grid."""
        pygame.display.set_caption("Random distribution")
        self.ues = []
        while len(self.ues) < MAX_DEVICES + 1:
            # Create the new device
            new_device = UE((0, 0), self.antenna)
            new_device.set_coor_random()
            # Set its image.
            new_device.set_device_trying_to_connect()
            # Add the new device to the list of devices
            self.ues.append(new_device)

    def open_loop(self):
        """Implementation of the open loop.

        This loop is in charge of the initial setting of the emitted power for any
        User Equipment in UMTS.

        The initial emitted power is deduced from a comparison between a
        measurement of the received power from the antenna (computed from Friis
        formula) and the real emitted power from a broadcast packet.
        This comparison gives us the free space path loss between the antenna and
        this UE.
        Then from this loss according to friis formula and sensitivity of the Node
        B we can compute the initial emitted power to use with this UE .

        Reminder :
            Friis Formula : Pr = Pe + Ge + Gr - (20log(f) + 20log(d in km) + 32.44)
            with Pr, Pe, Gr, Ge in dB

            Since the gains are null the free space loss corresponds to the part
            between parenthesis.

        """
        # Retry MAX_PREAMBLE_CYCLE times before considering the UE connected or not
        i = 0
        while i < MAX_PREAMBLE_CYCLE:
            # Iterates over the devices (but not the antenna)
            for device in self.ues:
                # Increase PREAMBLE_RETRANS_MAX times
                j = 0
                while j < PREAMBLE_RETRANS_MAX:
                    with device.mutex:
                        # computation of the free space path loss.
                        free_space_loss = 20*log10(UMTS_FREQ/1000) + 20*log10(device.distance_from_antenna/1000) + 32.44
                        # Computation of the emitted power to reach to be sure the
                        # NodeB will receive the signal.
                        emitted_power_to_reach = ANTENNA_SENSITIVITY - ANTENNA_GAIN - UE_GAIN + free_space_loss
                        # If the current emitted power isn't sufficient then increase
                        # it by a step.
                        if device.emitted_power >= emitted_power_to_reach:
                            prev_cmd = device.command
                            prev_status = device.status
                            device.set_device_connected()
                            # Only render if changed.
                            if not (prev_cmd == device.command and
                                    prev_status == device.status):
                                self.on_render()
                        else:
                            if device.emitted_power < UE_MAX_EMITTED_POWER:
                                device.emitted_power += POWER_CONTROL_STEP
                                prev_cmd = device.command
                                prev_status = device.status
                                device.set_command_up()
                                # Only render if changed.
                                if not (prev_cmd == device.command and
                                        prev_status == device.status):
                                    self.on_render()
                            else:
                                prev_cmd = device.command
                                prev_status = device.status
                                device.set_device_disconnected()
                                # Only render if changed.
                                if not (prev_cmd == device.command and
                                        prev_status == device.status):
                                    self.on_render()
                        j += 1
            i += 1
        for device in self.ues:
            if device.status != CONNECTED:
                prev_cmd = device.command
                prev_status = device.status
                device.set_device_disconnected()
                # Only render if changed.
                if not (prev_cmd == device.command and
                        prev_status == device.status):
                    self.on_render()
