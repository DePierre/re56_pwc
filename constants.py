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
RIGHT_PANEL_IMAGE = PICTURE_PATH + "right_pane.png"
ANTENNA_IMAGE = PICTURE_PATH + "antenna2.png"
MENU_SELECTION1_IMAGE = PICTURE_PATH + "menu_selection_1.png"
MENU_SELECTION2_IMAGE = PICTURE_PATH + "menu_selection_2.png"
MENU_SELECTION3_IMAGE = PICTURE_PATH + "menu_selection_3.png"
MENU_SELECTION1_SELECTED_IMAGE = PICTURE_PATH + "menu_selection_1_selected.png"
MENU_SELECTION2_SELECTED_IMAGE = PICTURE_PATH + "menu_selection_2_selected.png"
MENU_SELECTION3_SELECTED_IMAGE = PICTURE_PATH + "menu_selection_3_selected.png"
ARROW_SELECTOR_IMAGE = PICTURE_PATH + "arrow_selector.png"
DEVICE_CONNECTED_UP_IMAGE = PICTURE_PATH + "connected_up.png"
DEVICE_CONNECTED_DOWN_IMAGE = PICTURE_PATH + "connected_down.png"
DEVICE_TRY_TO_CONNECT_UP_IMAGE = PICTURE_PATH + "try_up.png"
DEVICE_TRY_TO_CONNECT_DOWN_IMAGE = PICTURE_PATH + "try_down.png"
DEVICE_DISCONNECTED_IMAGE = PICTURE_PATH + "disconnected.png"

# Maximum number of devices
MAX_DEVICES = 2000

# UMTS frequency in MHz
UMTS_FREQ = 2200

# Antenna and UE gain in dB
ANTENNA_GAIN = 0
UE_GAIN = 0

# Receivers sensitivity in dBm
ANTENNA_SENSITIVITY = -110
UE_SENSITIVITY = -100

# Power control steps in dB
POWER_CONTROL_STEP = 1

# Antenna emitted powerin dBm
ANTENNA_EMITTED_POWER = 50.0

# UE max & min emitted power in dBm
UE_MAX_EMITTED_POWER = 20.0

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
CELL_RES = 150

# Size in pixels of the main window.
MAIN_WINDOW_HEIGHT = 720  # Max which could be used: 1366 x 768 screen (16:9).
MAIN_WINDOW_WIDTH = 1220
GRID_HEIGHT = MAIN_WINDOW_HEIGHT
GRID_WIDTH = GRID_HEIGHT

CELL_HEIGHT = 20.0  # Pixels.
CELL_WIDTH = 20.0  # Pixels.

# 1 pixel unit will correspond to the following value in meter
PIX_IN_METERS = CELL_RES / CELL_HEIGHT



# Antenna location
ANTENNA_LOC_HEIGHT = GRID_HEIGHT / 2 - CELL_HEIGHT
ANTENNA_LOC_WIDTH = GRID_WIDTH / 2 - CELL_WIDTH

# Menu item sizes
MENU_ITEM_HEIGHT = 50
MENU_ITEM_WIDTH = 150

# Menu items positions inside right panel
MENU_ITEM_OFFSET_FROM_LEFT_RIGHT_PANEL_SIDE = 50
MENU_OFFSET_FROM_TOP_RIGHT_PANEL = 570

# Offset of the arrow_selector from menu item (width, height).
ARROW_SELECTOR_WIDTH_OFFSET_FROM_MENU_ITEM = 150  # Pixels.
ARROW_SELECTOR_HEIGHT_OFFSET_FROM_MENU_ITEM = 15  # Pixels.
