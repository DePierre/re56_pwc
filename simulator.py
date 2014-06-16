# -*- encoding: utf8 -*-
"""

    simulator.py

    Define the simulation of the project.

"""


import pygame
from pygame.locals import *

from copy import copy
from math import log10, sqrt
from random import choice, randint
from threading import Lock

from constants import *
from menu import Menu
from device import Antenna, \
                   UeVoice, \
                   UePS64, UePS128, UePS384, \
                   UeHSDPA768, UeHSDPA2000


class Simulator(object):
    """Manage the simulation of the power control in UMTS."""

    def __init__(self):
        self._running = True
        # Surfaces of the GUI.
        self._window = None
        self._bg_original = None
        self._bg = None
        self._menu = None
        self._clock = None
        # List of User equipments.
        self.ues = []
        self.open_looped_ues = []
        # List of free coordinates on the grid.
        self.free_coors = []
        self.mutex = Lock()
        # Coordinates of the grid.
        self.weight = MAIN_WINDOW_WIDTH
        self.height = MAIN_WINDOW_HEIGHT
        self.size = (self.weight, self.height)

    def init_free_coors(self, radius=MAX_DISTANCE):
        """Generates the free coordinates available on the grid.

        random_coors: contains all possible coordinates.
        circle_coors: contains all coordinates that are included in a circle
                      with radius=`radius`.
        out_circle_coors: contains all coordinates outside of the previous
                          circle.

        """
        self.random_coors = []
        self.circle_coors = []
        self.out_circle_coors = []
        for x in range(0, int(GRID_WIDTH), int(CELL_WIDTH)):
            for y in range(0, int(GRID_HEIGHT), int(CELL_HEIGHT)):
                # The antenna already occupies a cell.
                if (x == self.antenna.x and y == self.antenna.y):
                    continue
                self.random_coors.append((x, y))
                # Circle: (x - a)^2 + (y - b)^2 = r^2
                if ((x - self.antenna.x) ** 2 +
                        (y - self.antenna.y) ** 2 < radius ** 2):
                    self.circle_coors.append((x, y))
                else:
                    self.out_circle_coors.append((x, y))

    def on_init(self):
        """Initialize the simulation right before starting the render loop."""
        pygame.init()
        # Initialize the main window.
        self._window = pygame.display.set_mode(self.size)
        # Create the antenna.
        self.antenna = Antenna((ANTENNA_LOC_WIDTH, ANTENNA_LOC_HEIGHT))
        # Generate the background of the grid.
        self._bg_original = pygame.image.load(BACKGROUND_SCALED_IMAGE)
        self._bg = copy(self._bg_original)
        self._bg.blit(self.antenna.image, (self.antenna.x, self.antenna.y))
        # Instantiate the menu.
        self._menu = Menu(self)
        # Generate the free available coordinates.
        self.init_free_coors()
        # Internal mechanisms
        self._clock = pygame.time.Clock()
        self._running = True
        return True

    def reset_display(self):
        """Reset the grid to its original image (i.e. an empty grid)."""
        self._bg = copy(self._bg_original)
        self._bg.blit(self.antenna.image, (self.antenna.x, self.antenna.y))

    def on_event(self, event):
        """Manage the events sent to the window (e.g. a key pressed)."""
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self._menu.menu_next()
            elif event.key == pygame.K_UP:
                self._menu.menu_previous()
            # The user wants to run a new simulation.
            elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                self.ues = []  # Reset the user equipments for the new simu.
                with self.mutex:
                    self.open_looped_ues = []
                self.reset_display()
                self._menu.select_menu(self._menu.selected)
            # The user wants to add new devices.
            elif event.key == pygame.K_a:
                self.add_new_devices(MAX_NEW_DEVICES)
            elif event.key == pygame.K_ESCAPE:
                self._running = False

    def on_render(self):
        """Manage the rendering system of the window."""
        self._window.blit(self._bg, (0, 0))
        self._window.blit(self._menu.surface, (GRID_WIDTH, 0))
        pygame.display.flip()

    def update_device(self, device):
        """Update the status of a device.

        Blit an empty cell on the older status and blit the new status on this
        empty cell.
        This avoids possible problems with the alpha component of PNG files.

        """
        # Erase older display with an empty cell because of the alpha.
        empty_cell = pygame.image.load(CELL_IMAGE).convert_alpha()
        self._bg.blit(empty_cell, (device.x, device.y))
        # Blit the new device image.
        self._bg.blit(device.image, (device.x, device.y))

    def on_cleanup(self):
        """Manage a clean exit when the user close the GUI."""
        pygame.quit()

    def on_execute(self):
        """Main rendering loop of the simulation.

        Manage the render, the events and the simulation loops.

        """
        if self.on_init() is False:
            self._running = False

        self.on_render()
        while self._running:
            self._clock.tick(60)
            # Manage the events.
            for event in pygame.event.get():
                self.on_event(event)
            # Core of the simulation.
            self.open_loop()
            self.outer_loop()
            self.inner_loop()
            # Update the display
            for device in self.ues:
                self.update_device(device)
            self.on_render()
        self.on_cleanup()

    def close_distribution(self):
        """Create MAX_DEVICES devices close to the antenna on the grid."""
        pygame.display.set_caption("Close distribution")
        self.free_coors = copy(self.circle_coors)
        self.distribution(self.free_coors)
        self.on_render()

    def far_distribution(self):
        """Create MAX_DEVICES devices far from the antenna on the grid."""
        pygame.display.set_caption("Far distribution")
        self.free_coors = copy(self.out_circle_coors)
        self.distribution(self.free_coors)

    def random_distribution(self):
        """Create MAX_DEVICES devices randomly on the grid."""
        pygame.display.set_caption("Random distribution")
        self.free_coors = copy(self.random_coors)
        self.distribution(self.free_coors)

    def distribution(self, free_coors, nb_devices=MAX_DEVICES):
        """Place `nb_devices` new devices on the grid.

        Randomly select the type of device according to the `dist` table.

        """
        if nb_devices < 0:
            return
        # Distribution table in %
        dist = [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 70% CS-12,2
            1, 1,  # 10% PS-64
            2,  # 5% PS-128
            3,  # 5% PS-384
            4,  # 5% HSDPA-768
            5,]  # 5% HSDPA-2000
        possible_ues = [
            UeVoice,
            UePS64, UePS128, UePS384,
            UeHSDPA768, UeHSDPA2000]
        while nb_devices:
            nb_devices -= 1
            # Create the new device
            new_device = possible_ues[choice(dist)]((0, 0), self.antenna)
            new_device.set_coor_random(free_coors)
            # Default behavior set to trying to connect.
            new_device.set_device_trying_to_connect()
            # Update the different lists of the devices.
            self.ues.append(new_device)
            with self.mutex:
                self.open_looped_ues.append(new_device)
            if not len(free_coors):  # No more free cells.
                break

    def open_loop(self):
        """Implementation of the open loop.

        This loop is in charge of the initial setting of the emitted power for
        any User Equipment in UMTS.

        To compute the initial emitted power of the UE:

            - We "measure" the RxLev at the UE from the NodeB.
              As we cannot measure the RxLev we consider only the distance
              between the two objects as a replacement measurement.
              To compute it we use a Friis formula with a coefficient N = 1.4

            - From this RxLev and the real Ep of the NodeB we compute a new
              distance but using a Friis formula with a coefficient N = 1.3.
              As the NodeB Ep is much more higher than UE's Ep the signal from
              the NodeB can cross obstacles whereas UE signal will be reflected
              and therefore cover a greater distance.

            - From the second distance using a Friis formula with a coefficient
              N = 1.3 we can compute the real RxLev of the UE at the NodeB

            - From the first distance using a Friis formula with a corefficient
              N = 1.3 the UE estimates its own initial Ep.

        Reminder:
            Friis Formula : Pr = Pe + Ge + Gr - (20log(f in MHz) + 20Nlog(d in m) - 27.55)
            with Pr, Pe, Gr, Ge in dB

            Since the gains are null the free space loss corresponds to the
            part between parenthesis.

        """
        with self.mutex:
            if not len(self.open_looped_ues):
                return
            # Randomly select a device from the list of
            # not-already-open-looped-devices.
            index = randint(0, len(self.open_looped_ues) - 1)
            device = self.open_looped_ues[index]
            del self.open_looped_ues[index]
        with device.mutex:
            # A device is only open-looped once.
            if device.open_looped:
                return
            # Computation of initial emitted_power for the device
            # Compute RxLev
            RxLevNodeB = self.antenna.emitted_power + \
                         UE_GAIN + ANTENNA_GAIN - \
                         (20 * log10(UMTS_FREQ) + \
                         20 * (FRIIS_OBSTACLE_CONSTANT + 0.1) * \
                         log10(device.distance_from_antenna) - 27.55)
            # Compute the new distance covered by UE's signal
            new_distance = 10**(
                (-RxLevNodeB + self.antenna.emitted_power + \
                UE_GAIN + ANTENNA_GAIN - 20 * log10(UMTS_FREQ) + 27.55) /
                (20*FRIIS_OBSTACLE_CONSTANT)
                )
            # Set the initial UE's Ep
            initial_ep = ANTENNA_SENSITIVITY - UE_GAIN - ANTENNA_GAIN + \
                         20 * log10(UMTS_FREQ) + \
                         20 * FRIIS_OBSTACLE_CONSTANT * \
                         log10(device.distance_from_antenna) - 27.55
            if initial_ep <= UE_MAX_EMITTED_POWER:
                device.emitted_power = initial_ep
            else :
                device.emitted_power = UE_MAX_EMITTED_POWER
            # Compute the UE's Ep to reach to be connected
            emitted_power_to_reach = ANTENNA_SENSITIVITY - UE_GAIN - \
                                     ANTENNA_GAIN + \
                                     20 * log10(UMTS_FREQ) + \
                                     20 * FRIIS_OBSTACLE_CONSTANT * \
                                     log10(new_distance) - 27.55
            # Retry MAX_PREAMBLE_CYCLE times before considering the UE
            # connected or not.
            i = 0
            while i < MAX_PREAMBLE_CYCLE:
                # Increase PREAMBLE_RETRANS_MAX times
                j = 0
                while j < PREAMBLE_RETRANS_MAX:
                    # If the current emitted power isn't sufficient then
                    # increase it by a step.
                    if device.emitted_power >= emitted_power_to_reach:
                        device.set_device_connected()
                        fsl = 20 * log10(UMTS_FREQ) + \
                              20 * FRIIS_OBSTACLE_CONSTANT * \
                              log10(device.distance_from_antenna) - \
                              27.55
                        device.target = device.emitted_power + \
                                        UE_GAIN + ANTENNA_GAIN - fsl
                        j = PREAMBLE_RETRANS_MAX
                        i = MAX_PREAMBLE_CYCLE
                        print "------ new device ------"
                        print "UE Ep (dBm) : ", device.emitted_power
                        print "UE fsl (dB) : ", fsl
                        print "UE target (dBm) : ", device.target
                        print ""
                    else:
                        device.set_command_up()
                    j += 1
                i += 1
            device.open_looped = True
            if device.status != CONNECTED:
                device.set_device_disconnected()
                print "Device disconnected : end of open loop"

    def outer_loop(self):
        """Implementation of the outer loop.

        This loop is in charge of the computation of the SINR. This SINR is
        used to set the target received power of the antenna from which the
        antenna can take a decision about the command to send to the UE.

        This C/I is computed for each device as follows :
        C/I = (Pm + Gm) / (sum(Gi + Pj) + TN)
        TN can be neglicted in our case!
        With:
            Pi emitted power of the mobile i
            Gi gain of the mobile i
            TN = thermal noise at the base station
                TN=kTB
                k: Boltzmann constant 1.3806504×10-23 J/K
                T: Temperature in Kalvin here 290 °K (20 °C)
                B: Bandwith in Hz

        """
        if not self.ues:
            return
        device = choice(self.ues)
        with device.mutex:
            # The outer loop cannot process a non-open-looped-yet device.
            if not device.open_looped:
                return
            # Compute C/I.
            needed_power = device.emitted_power + UE_GAIN + ANTENNA_GAIN - \
                           self.compute_free_space_loss(self.antenna,device)
            if needed_power >= ANTENNA_SENSITIVITY:
                snr = (10**((
                    device.emitted_power + UE_GAIN + ANTENNA_GAIN -
                    self.compute_free_space_loss(self.antenna,device) - 30) /
                    10)) / self.compute_interference(device)
                snr = 10 * log10(snr)
                if snr < device.snr:
                    device.target += TARGET_STEP
                else:
                    device.target -= TARGET_STEP

    def inner_loop(self):
        """Implementation of the Inner loop.

        This loop is in charge of sending the correct command to the UEs
        according to the target from the outer loop.

        """
        if not self.ues:
            return
        device = choice(self.ues)
        with device.mutex:
            # The inner loop cannot process a non-open-looped-yet device.
            if not device.open_looped:
                return
            if not device.status == NOT_CONNECTED:
                # Compute the received power
                fsl = 20 * log10(UMTS_FREQ) + 20 * FRIIS_OBSTACLE_CONSTANT * \
                      log10(device.distance_from_antenna) - 27.55
                received_power = device.emitted_power + UE_GAIN + \
                                 ANTENNA_GAIN - fsl
                # If the received power is under the target then send command
                # up.
                if received_power < device.target:
                    device.set_command_up()
                    print "inner loop : command up (RxLev = " + \
                          str(received_power) + ", target = " + \
                          str(device.target) + ")"
                else:
                    device.set_command_down()
                    print "inner loop : command down (RxLev = " + \
                           str(received_power) + ", target = " + \
                           str(device.target) + ")"

    def compute_interference(self, device):
        """Interference computation for a given device.

        Interference noted I equals the sum of non targeted emission power
        received plus the thermal noise.
        Here the received power from others UE will be considered as the non
        targeted received power.

        A free space loss calculation will be done in order to estimate the
        power received from each UE.

        Iue= sum(Pi-FSL(ue,i)+Gi)

        With:
            Pi: neighbor emitted power
            FSL: free space loss (friis formula) between device and a neighbor
            Gi: neighbor gain

        """
        interference = .0
        # Compute received power from each neighbor device.
        for neighbor in self.ues:
            if device == neighbor:
                continue
            needed_power = neighbor.emitted_power - \
                           self.compute_free_space_loss(
                                self.antenna, neighbor) + \
                           UE_GAIN
            if needed_power >= ANTENNA_SENSITIVITY:
                interference += 10**((
                    neighbor.emitted_power -
                    self.compute_free_space_loss(self.antenna, neighbor) +
                    UE_GAIN - 30) / 10)
        return interference

    def compute_free_space_loss(self, device, neighbor):
        """Compute the free space loss between two devices.

        free space loss = 20*log10(F in MHz) + 20*N*log10(distance(UE,EUi)
        /1000) - 27.55

        """
        return 20 * log10(UMTS_FREQ) + \
               20 * FRIIS_OBSTACLE_CONSTANT * \
               log10(device.compute_distance(neighbor)) - 27.55

    def add_new_devices(self, nb_new_devices):
        """Add new devices to the current simulation without stopping it."""
        # TODO: Maybe pause before adding new devices?
        pygame.display.set_caption(
            "Adding new devices to the current simulation")
        self.distribution(self.free_coors, nb_devices=nb_new_devices)
