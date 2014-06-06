# -*- encoding: utf8 -*-
import pygame
from pygame.locals import *

from copy import copy
from math import log10, sqrt

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
                try:
                    self.start()
                except KeyboardInterrupt:
                    self._running = False
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

    def start(self):
        """Start the simulation according to the distribution scenario."""
        # First start the open loop process.
        self.open_loop()
        # Then the outer loop.
        self.outer_loop()

    def close_distribution(self):
        """Create MAX_DEVICES devices close to the antenna on the grid."""
        pygame.display.set_caption("Close distribution")
        coors = []
        self.ues = []
        while len(self.ues) < MAX_DEVICES + 1:
            # Create the new device
            new_device = UE((0, 0), self.antenna)
            while True:
                new_device.set_coor_close()
                if not (new_device.x, new_device.y) in coors:
                    break
            coors.append((new_device.x, new_device.y))
            # Set its image.
            new_device.set_device_trying_to_connect()
            # Add the new device to the list of devices
            self.ues.append(new_device)

    def far_distribution(self):
        """Create MAX_DEVICES devices far from the antenna on the grid."""
        pygame.display.set_caption("Far distribution")
        coors = []
        self.ues = []
        while len(self.ues) < MAX_DEVICES + 1:
            # Create the new device
            new_device = UE((0, 0), self.antenna)
            while True:
                new_device.set_coor_far()
                if not (new_device.x, new_device.y) in coors:
                    break
            coors.append((new_device.x, new_device.y))
            # Set its image.
            new_device.set_device_trying_to_connect()
            # Add the new device to the list of devices
            self.ues.append(new_device)

    def random_distribution(self):
        """Create MAX_DEVICES devices randomly on the grid."""
        pygame.display.set_caption("Random distribution")
        coors = []
        self.ues = []
        while len(self.ues) < MAX_DEVICES + 1:
            # Create the new device
            new_device = UE((0, 0), self.antenna)
            while True:
                new_device.set_coor_random()
                if not (new_device.x, new_device.y) in coors:
                    break
            coors.append((new_device.x, new_device.y))
            # Set its image.
            new_device.set_device_trying_to_connect()
            # Add the new device to the list of devices
            self.ues.append(new_device)

    def open_loop(self):
        """Implementation of the open loop.

        This loop is in charge of the initial setting of the emitted power for any
        User Equipment in UMTS.
        
        To compute the initial emitted power of the UE :
        
            - We "measure" the RxLev at the UE from the NodeB.
            As we cannot measure the RxLev we consider only the distance between
            the two objects as a replacement measurement.
            To compute it we use a Friis formula with a coefficient N = 1.4
            
            - From this RxLev and the real Ep of the NodeB we compute a new 
            distance but using a Friis formula with a coefficient N = 1.3.
            As the NodeB Ep is much more higher than UE's Ep the signal from the
            NodeB can cross obstacles whereas UE signal will be reflected and
            therefore cover a greater distance.
            
            - From the second distance using a Friis formula with a coefficient
            N = 1.3 we can compute the real RxLev of the UE at the NodeB
            
            - From the first distance using a Friis formula with a corefficient 
            N = 1.3 the UE estimates its own initial Ep.

        Reminder :
            Friis Formula : Pr = Pe + Ge + Gr - (20log(f in MHz) + 20Nlog(d in m) - 27.55)
            with Pr, Pe, Gr, Ge in dB

            Since the gains are null the free space loss corresponds to the part
            between parenthesis.

        """
        # Iterates over the devices (but not the antenna)
        for device in self.ues:
            # Computation of initial emitted_power for the device
            # Compute RxLev
            RxLevNodeB = self.antenna.emitted_power + UE_GAIN + ANTENNA_GAIN - (20*log10(UMTS_FREQ) + 20*(FRIIS_OBSTACLE_CONSTANT+0.1)*log10(device.distance_from_antenna) - 27.55)
            # Compute the new distance covered by UE's signal
            new_distance = 10**( (-RxLevNodeB + self.antenna.emitted_power + UE_GAIN + ANTENNA_GAIN - 20 * log10(UMTS_FREQ) + 27.55)/(20*FRIIS_OBSTACLE_CONSTANT) )
            # Set the initial UE's Ep
            initial_ep = ANTENNA_SENSITIVITY - UE_GAIN - ANTENNA_GAIN + 20*log10(UMTS_FREQ) + 20*FRIIS_OBSTACLE_CONSTANT*log10(device.distance_from_antenna) - 27.55
            if initial_ep <= UE_MAX_EMITTED_POWER:
                device.emitted_power = initial_ep
            else :
                device.emitted_power = UE_MAX_EMITTED_POWER
            # Compute the UE's Ep to reach to be connected
            emitted_power_to_reach = ANTENNA_SENSITIVITY - UE_GAIN - ANTENNA_GAIN + 20*log10(UMTS_FREQ) + 20*FRIIS_OBSTACLE_CONSTANT*log10(new_distance) - 27.55
            
            print "------ new device ------"
            print "UE Ep (dBm) : ", device.emitted_power
            print "UE shortest path (m) : ", device.distance_from_antenna
            print "UE real path (m) : ", new_distance
            print "Ep to reach (dBm) : ", emitted_power_to_reach
            print ""
            
            # Retry MAX_PREAMBLE_CYCLE times before considering the UE connected or not
            i = 0
            while i < MAX_PREAMBLE_CYCLE:            
                prev_cmd = device.command
                prev_status = device.status
                # Increase PREAMBLE_RETRANS_MAX times
                j = 0
                while j < PREAMBLE_RETRANS_MAX:
                    with device.mutex:
                        # If the current emitted power isn't sufficient then increase
                        # it by a step.
                        if device.emitted_power >= emitted_power_to_reach:
                            device.set_device_connected()
                        else:
                            if device.emitted_power < UE_MAX_EMITTED_POWER:
                                device.emitted_power += POWER_CONTROL_STEP
                                device.set_command_up()
                            else:
                                device.set_device_disconnected()
                        j += 1
                if not (prev_cmd == device.command and
                        prev_status == device.status):
                    self.on_render()
                i += 1
        for device in self.ues:
            device.open_looped = True
            if device.status != CONNECTED:
                prev_cmd = device.command
                prev_status = device.status
                device.set_device_disconnected()
                # Only render if changed.
                if not (prev_cmd == device.command and
                        prev_status == device.status):
                    self.on_render()

    def outer_loop(self):
        """Implementation of the outer loop.

        This loop is in charge of the computation of the BER. This BER is used
        to set the target received power of the antenna from which the antenna
        can take a decision about the command to send to the UE.

        This BER is obtained thanks to a table. This table contains the
        corresponding C/I for a specific BER.
        From that we can obtain our BER from a computation of a C/I.

        This C/I is computed for each device as follows :
        C/I = (Pm + Gm) / (sum(Gi + Pj) + TN)
        TN can be neglicted in our case !
        With :
            Pi emitted power of the mobile i
            Gi gain of the mobile i
            TN = thermal noise at the base station
                TN=kTB
                k : Boltzmann constant 1.3806504×10-23 J/K
                T : Temperature in Kalvin here 290 °K (20 °C)
                B : Bandwith in Hz

        """
        for device in self.ues:
            # Compute C/I.
            if device.emitted_power + UE_GAIN + ANTENNA_GAIN - self.compute_free_space_loss(self.antenna,device) >= ANTENNA_SENSITIVITY:
                #print "-------- outer_loop --------"
                #print "Dist (m): ", str(device.compute_distance(self.antenna))
                #print "FSL : ", str(self.compute_free_space_loss(self.antenna,device))
                #print "RxLev (dBm): ", device.emitted_power + UE_GAIN + ANTENNA_GAIN - self.compute_free_space_loss(self.antenna,device)
                #print "RxLev (W): ", 10**((device.emitted_power + UE_GAIN + ANTENNA_GAIN - self.compute_free_space_loss(self.antenna,device) -30)/10)
                #print "TOT intereferences (W): ", self.compute_interference(device)
                
                c_over_i = ( 10**((device.emitted_power + UE_GAIN + ANTENNA_GAIN - self.compute_free_space_loss(self.antenna,device) - 30)/10) )/ self.compute_interference(device)
                device.snr = 10 * log10(c_over_i)
                #print "SNR : ", c_over_i
                #print "SNR (dB): ", device.snr
                #print ""
                # TODO: Find the associated BLER and compare with target.

    def inner_loop(self):
        """Implementation of the Inner loop.

        This loop is in charge of sending the correct command to the UEs
        according to the target from the outer loop.

        """
        for device in self.ues:
            # Compute the received power
            fsl = 20 * log10(UMTS_FREQ) + 20 * FRIIS_OBSTACLE_CONSTANT * log10(
            device.distance_from_antenna
            ) - 27.55
            received_power = device.emitted_power - fsl
            # If the received power is under the target then send command up
            if received_power < self.antenna.target:
                device.set_command_up()
            else:
                device.set_command_down()

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
            Pi: neighboor emitted power
            FSL: free space loss (friis formula) between device and a neighboor
            Gi: neighboor gain

        """
        interference = .0
        # Compute received power from every neighboor device.
        for neighboor in self.ues:
            if device == neighboor:
                continue
            if neighboor.emitted_power - self.compute_free_space_loss(self.antenna,neighboor) + UE_GAIN >= ANTENNA_SENSITIVITY:
                interference += 10**((neighboor.emitted_power - self.compute_free_space_loss(self.antenna,neighboor) + UE_GAIN-30)/10)
        return interference

    def compute_free_space_loss(self, device, neighboor):
        """Compute the free space loss between two devices.

        free space loss = 20*log10(F in MHz) + 20*N*log10(distance(UE,EUi)
        /1000) - 27.55

        """
        return 20 * log10(UMTS_FREQ) + 20 * FRIIS_OBSTACLE_CONSTANT * log10(
            device.compute_distance(neighboor)
            ) - 27.55
            
    def add_new_device_to_simulation(self, number):
        """Add some new devices to the simulation in order to force a new state
        
        """
        coors = []
        # Get index of menu selected to know how to generate the new
        # coordinates.
        index = self._menu.get_index_menu_selected()
        # index 1 = close distrib
        # index 2 = far distrib
        # index 3 = random distrib
        if index == MENU1_INDEX:
            i = 0
            while i < number:
                # Create the new device
                new_device = UE((0, 0), self.antenna)
                while True:
                    new_device.set_coor_close()
                    if not (new_device.x, new_device.y) in coors:
                        break
                coors.append((new_device.x, new_device.y))
                # Set its image.
                new_device.set_device_trying_to_connect()
                # Add the new device to the list of devices
                self.ues.append(new_device)
                i++  
        elif index == MENU2_INDEX:
            i = 0
            while i < number:
                # Create the new device
                new_device = UE((0, 0), self.antenna)
                while True:
                    new_device.set_coor_far()
                    if not (new_device.x, new_device.y) in coors:
                        break
                coors.append((new_device.x, new_device.y))
                # Set its image.
                new_device.set_device_trying_to_connect()
                # Add the new device to the list of devices
                self.ues.append(new_device)
                i++
        elif index == MENU3_INDEX:
            i = 0
            while i < number:
                # Create the new device
                new_device = UE((0, 0), self.antenna)
                while True:
                    new_device.set_coor_random()
                    if not (new_device.x, new_device.y) in coors:
                        break
                coors.append((new_device.x, new_device.y))
                # Set its image.
                new_device.set_device_trying_to_connect()
                # Add the new device to the list of devices
                self.ues.append(new_device)
                i++
