# General
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TANK_CAPACITY = 10
SPAWN_FREQUENCY = 2  # every 2 seconds fish spawns
SCORE_POSITION_LEFT = 0
SCORE_POSITION_TOP = 550

# Other screens
white_color = (255, 255, 255)
black_color = (0, 0, 0)

# Center of the screen
screen_center = 400
screen_bottom = 550
screen_gap = 400  # space between two group of text in credits screen

# Game_controller.py
IMAGE_SIZE_MISMATCH = 50  # Used for better representation of player eating other fishes (in pixels)
FISH_SIZE_DIFFERENCE = 20  # It does not make sense if player with size of 401 can eat fish with 402 size (in percent)
SCORE_PERCENT = 5  # Percent of fish size that will be added to player's SCORE after eating (in percent)
SIZE_PERCENT = 5  # Percent of fish size that will be added to player's SIZE after eating (in percent)

# Npc.py
MIN_DISTANCE = 50  # minimal distance between two fishes (in pixels)


def set_property(name, value):
    if name == 'SCREEN_WIDTH':
        global SCREEN_WIDTH, screen_center
        SCREEN_WIDTH = value
        screen_center = value / 2

    if name == 'SCREEN_HEIGHT':
        global SCREEN_HEIGHT, screen_gap, screen_bottom
        SCREEN_HEIGHT = value
        screen_gap = value / 2
        screen_bottom = value - 50


# ADD MORE IF NEEDED