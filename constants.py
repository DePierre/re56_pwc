"""

    constants.py

    Define the constants that will be used in the rest of the project.
    The images, the initial values, etc.

"""


COMMAND_UP = 1
COMMAND_DOWN = 0

CONNECTED = 1
TRY_CONNECT = 2
NOT_CONNECTED = 0

MENU1_INDEX = 0
MENU2_INDEX = 1
MENU3_INDEX = 2

PICTURE_PATH = "pictures/"
# Picture names.
BACKGROUND_IMAGE = PICTURE_PATH + "background.png"
BACKGROUND_SCALED_IMAGE = PICTURE_PATH + "background_scale.png"
CELL_IMAGE = PICTURE_PATH + "empty_cell.png"
RIGHT_PANEL_IMAGE = PICTURE_PATH + "right_pane.png"
ANTENNA_IMAGE = PICTURE_PATH + "antenna2.png"
MENU_CLOSE1_IMAGE = PICTURE_PATH + "menu_selection_1.png"
MENU_FAR2_IMAGE = PICTURE_PATH + "menu_selection_2.png"
MENU_RANDOM3_IMAGE = PICTURE_PATH + "menu_selection_3.png"
MENU_CLOSE1_SELECTED_IMAGE = PICTURE_PATH + "menu_selection_1_selected.png"
MENU_FAR2_SELECTED_IMAGE = PICTURE_PATH + "menu_selection_2_selected.png"
MENU_RANDOM3_SELECTED_IMAGE = PICTURE_PATH + "menu_selection_3_selected.png"
ARROW_IMAGE = PICTURE_PATH + "arrow_selector.png"
# Default device
DEVICE_CONNECTED_UP_IMAGE = PICTURE_PATH + "connected_up.png"
DEVICE_CONNECTED_DOWN_IMAGE = PICTURE_PATH + "connected_down.png"
DEVICE_TRY_TO_CONNECT_UP_IMAGE = PICTURE_PATH + "try_up.png"
DEVICE_TRY_TO_CONNECT_DOWN_IMAGE = PICTURE_PATH + "try_down.png"
DEVICE_DISCONNECTED_IMAGE = PICTURE_PATH + "disconnected.png"
# Voice call device
VOICE_CONNECTED_UP_IMAGE = PICTURE_PATH + "connected_up_voice.png"
VOICE_CONNECTED_DOWN_IMAGE = PICTURE_PATH + "connected_down_voice.png"
VOICE_TRY_TO_CONNECT_UP_IMAGE = PICTURE_PATH + "try_up_voice.png"
VOICE_TRY_TO_CONNECT_DOWN_IMAGE = PICTURE_PATH + "try_down_voice.png"
VOICE_DISCONNECTED_IMAGE = PICTURE_PATH + "disconnected_voice.png"
# 3G Low troughput device
A3GLT_CONNECTED_UP_IMAGE = PICTURE_PATH + "connected_up_3GLT.png"
A3GLT_CONNECTED_DOWN_IMAGE = PICTURE_PATH + "connected_down_3GLT.png"
A3GLT_TRY_TO_CONNECT_UP_IMAGE = PICTURE_PATH + "try_up_3GLT.png"
A3GLT_TRY_TO_CONNECT_DOWN_IMAGE = PICTURE_PATH + "try_down_3GLT.png"
A3GLT_DISCONNECTED_IMAGE = PICTURE_PATH + "disconnected_3GLT.png"
# 3G Medium troughput device
A3GMT_CONNECTED_UP_IMAGE = PICTURE_PATH + "connected_up_3GMT.png"
A3GMT_CONNECTED_DOWN_IMAGE = PICTURE_PATH + "connected_down_3GMT.png"
A3GMT_TRY_TO_CONNECT_UP_IMAGE = PICTURE_PATH + "try_up_3GMT.png"
A3GMT_TRY_TO_CONNECT_DOWN_IMAGE = PICTURE_PATH + "try_down_3GMT.png"
A3GMT_DISCONNECTED_IMAGE = PICTURE_PATH + "disconnected_3GMT.png"
# 3G High troughput device
A3GHT_CONNECTED_UP_IMAGE = PICTURE_PATH + "connected_up_3GHT.png"
A3GHT_CONNECTED_DOWN_IMAGE = PICTURE_PATH + "connected_down_3GHT.png"
A3GHT_TRY_TO_CONNECT_UP_IMAGE = PICTURE_PATH + "try_up_3GHT.png"
A3GHT_TRY_TO_CONNECT_DOWN_IMAGE = PICTURE_PATH + "try_down_3GHT.png"
A3GHT_DISCONNECTED_IMAGE = PICTURE_PATH + "disconnected_3GHT.png"
# HLT device
HLT_CONNECTED_UP_IMAGE = PICTURE_PATH + "connected_up_HLT.png"
HLT_CONNECTED_DOWN_IMAGE = PICTURE_PATH + "connected_down_HLT.png"
HLT_TRY_TO_CONNECT_UP_IMAGE = PICTURE_PATH + "try_up_HLT.png"
HLT_TRY_TO_CONNECT_DOWN_IMAGE = PICTURE_PATH + "try_down_HLT.png"
HLT_DISCONNECTED_IMAGE = PICTURE_PATH + "disconnected_HLT.png"
# HHT device
HHT_CONNECTED_UP_IMAGE = PICTURE_PATH + "connected_up_HHT.png"
HHT_CONNECTED_DOWN_IMAGE = PICTURE_PATH + "connected_down_HHT.png"
HHT_TRY_TO_CONNECT_UP_IMAGE = PICTURE_PATH + "try_up_HHT.png"
HHT_TRY_TO_CONNECT_DOWN_IMAGE = PICTURE_PATH + "try_down_HHT.png"
HHT_DISCONNECTED_IMAGE = PICTURE_PATH + "disconnected_HHT.png"


# Maximum number of devices
MAX_DEVICES = 150
MAX_NEW_DEVICES = 50

# UMTS frequency in MHz
UMTS_FREQ = 2200

# Antenna and UE gain in dB
ANTENNA_GAIN = 0
UE_GAIN = 0

# Receivers sensitivity in dBm
ANTENNA_SENSITIVITY = -110
UE_SENSITIVITY = -100

# Power control steps in dB
POWER_CONTROL_STEP = 3
TARGET_STEP = 1

# Antenna emitted powerin dBm
ANTENNA_EMITTED_POWER = 50.0

# UE max & min emitted power in dBm
UE_MAX_EMITTED_POWER = 20.0

# UE SINR target in dB
VOICE_SNR_TARGET = -20.0
A3GLT_SNR_TARGET = -18.0
A3GMT_SNR_TARGET = -15.0
A3GHT_SNR_TARGET = -10.0
HLT_SNR_TARGET = 0
HHT_SNR_TARGET = 3

# Open loop constants
PREAMBLE_RETRANS_MAX = 8
MAX_PREAMBLE_CYCLE = 4

# Outer loop constants
BOLTZMANN_CONSTANT = 1.3806504E-23
TEMPERATURE_IN_KELVIN = 290
BANDWIDTH = 5000000 #UMTS bandwidth is 5MHz
# This constants is used to define a variant of the friis formula taking into
# account the obstacles existing between Tx and Rx
FRIIS_OBSTACLE_CONSTANT = 1.3

# Resolution of a cell of the grid in meters.
# The cell dimension is CELL_RES x CELL_RES
CELL_RES = 100

# Size in pixels of the main window.
MAIN_WINDOW_HEIGHT = 720  # Max which could be used: 1366 x 768 screen (16:9).
MAIN_WINDOW_WIDTH = 1220
GRID_HEIGHT = MAIN_WINDOW_HEIGHT
GRID_WIDTH = GRID_HEIGHT

CELL_HEIGHT = 20.0  # Pixels.
CELL_WIDTH = 20.0  # Pixels.

# 1 pixel unit will correspond to the following value in meter
PIX_IN_METERS = CELL_RES / CELL_HEIGHT

# Radius of the circle for close/far distribution algo.
MAX_DISTANCE = 200

# Antenna location
ANTENNA_LOC_HEIGHT = GRID_HEIGHT / 2 - CELL_HEIGHT
ANTENNA_LOC_WIDTH = GRID_WIDTH / 2 - CELL_WIDTH

# Menu item sizes
MENU_ITEM_HEIGHT = 50
MENU_ITEM_WIDTH = 150

# Menu items positions inside right panel
MENU_ITEM_OFFSET = 50
MENU_OFFSET = 570

# Offset of the arrow_selector from menu item (width, height).
ARROW_WIDTH_OFFSET = 150  # Pixels.
ARROW_HEIGHT_OFFSET = 15  # Pixels.
