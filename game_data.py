import pygame

# General
screen_caption = "Feeding frenzy"
screen_icon_path = './img/logo/fish-512.png'
screen = 0
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TANK_CAPACITY = 10
SPAWN_FREQUENCY = 2  # every 2 seconds fish spawns
general_font_name = 'Comic Sans MS'

# Game screen
SCORE_POSITION_LEFT = 10
SCORE_POSITION_TOP = 550
TASK_POSITION_LEFT = 10
TASK_POSITION_TOP = 0

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
DANGER_FISH_SPAWN_FREQUENCY = 20  # (In seconds)
DANGER_SIGH_INTERVAL = 3  # Time that danger sign will blink before appearance of the danger fish (in seconds)
SPEED_COEF = 10  # Amount of speed that fish will gain from higher levels (in percent)

# Custom type events
GAME_OVER_EVENT = pygame.event.Event(pygame.USEREVENT)
LEVEL_CHANGED_EVENT = pygame.event.Event(pygame.USEREVENT + 1)
GAME_WIN_EVENT = pygame.event.Event(pygame.USEREVENT + 2)

# Npc.py
MIN_DISTANCE = 20  # minimal distance between two fishes (in pixels)
DANGER_FISH_SIZE = 9999

# Levels
NUM_OF_LEVELS = 5

# Image and sound path
background_music_path = './audio/Dan Balan - Lendo Calendo ft. Tany Vander & Brasco (Lyric Video).wav'
eating_sound_path = './audio/eating_sound.wav'
danger_sign_path = './img/npcs/danger-sign1.png'
game_background_properties = ['./img/gif/', 'coral', '.jpg']
other_screens_background_path = './img/background/abstract-dark-blue-polygonal-background-abstraktsiia-geometr.jpg'

player_first_image_properties = ['./img/npcs/downloads/', 'fish', '.png']
player_second_image_properties = ['./img/npcs/', 'YellowFish', '.png']
player_third_image_properties = ['./img/npcs/downloads/', 'frame', '.png']

player_chosen_image_properties = 0  # set after the hero choosing screen


def set_property(name, value):
    if name == 'screen':
        global screen
        screen = value

    if name == 'SCREEN_WIDTH':
        global SCREEN_WIDTH, screen_center
        SCREEN_WIDTH = value
        screen_center = value / 2

    if name == 'SCREEN_HEIGHT':
        global SCREEN_HEIGHT, screen_gap, screen_bottom, SCORE_POSITION_TOP
        SCREEN_HEIGHT = value
        screen_gap = value / 2
        screen_bottom = value - 50
        SCORE_POSITION_TOP = value - 50

    if name == 'player_image':
        global player_chosen_image_properties
        player_chosen_image_properties = value


# ADD MORE IF NEEDED