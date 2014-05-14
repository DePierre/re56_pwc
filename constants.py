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
BACKGROUND_IMAGE= "background.png"
BACKGROUND_SCALED_IMAGE = "background_scale.png"
RIGHT_PANEL_IMAGE= "right_pane.png"
ANTENNA_IMAGE ="antenna2.png"
MENU_SELECTION1_IMAGE = "menu_selection_1.png"
MENU_SELECTION2_IMAGE = "menu_selection_2.png"
MENU_SELECTION3_IMAGE  = "menu_selection_3.png"
MENU_SELECTION1_SELECTED_IMAGE  = "menu_selection_1_selected.png"
MENU_SELECTION2_SELECTED_IMAGE  = "menu_selection_2_selected.png"
MENU_SELECTION3_SELECTED_IMAGE  = "menu_selection_3_selected.png"
ARROW_SELECTOR_IMAGE = "arrow_selector.png"
DEVICE_CONNECTED_UP_IMAGE = "connected_up.png"
DEVICE_CONNECTED_DOWN_IMAGE = "connected_down.png"
DEVICE_TRY_TO_CONNECT_UP_IMAGE = "try_up.png"
DEVICE_TRY_TO_CONNECT_DOWN_IMAGE = "try_down.png"
DEVICE_DISCONNECTED_IMAGE = "disconnected.png"

# For every constant defined hereafter 1 pixel unit will correspond to the
# following value in meter
PIX_IN_METERS = 100

# Size in pixels of the main window.
MAIN_WINDOW_HEIGHT = 720  # Max which could be used: 1366 x 768 screen (16:9).
MAIN_WINDOW_WIDTH = 1220
GRID_HEIGHT = MAIN_WINDOW_HEIGHT
GRID_WIDTH = GRID_HEIGHT

CELL_HEIGHT = 20  # Pixels.
CELL_WIDTH = 20  # Pixels.

# Maximum number of devices
MAX_DEVICS = 100

# Antenna location
ANTENNA_LOC_HEIGHT = GRID_HEIGHT / 2 - CELL_HEIGHT
ANTENNA_LOC_WIDTH = GRID_WIDTH / 2 - CELL_WIDTH

# Offset of the arrow_selector from menu item (width, height).
ARROW_SELECTOR_WIDTH_OFFSET_FROM_MENU_ITEM = 150  # Pixels.
ARROW_SELECTOR_HEIGHT_OFFSET_FROM_MENU_ITEM = 15  # Pixels.
