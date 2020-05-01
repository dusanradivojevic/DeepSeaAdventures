import pygame

# General
screen_caption = "Deep-Sea Adventures"
screen_icon_path = './img/logo/fish-512.png'
screen = 0
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TANK_CAPACITY = 12
SPAWN_FREQUENCY = 2  # every 2 seconds fish spawns
general_font_name = 'Comic Sans MS'

# Game screen
SCORE_POSITION_LEFT = 10
SCORE_POSITION_TOP = 550
TASK_POSITION_LEFT = 10
TASK_POSITION_TOP = 0

# Intro screen
press_any_key_text_delay = 2  # blinking text after amount of time (in seconds)
start_screen_delay = 10  # after this amount of time of player's inactivity screen automatically changes to start screen

# Other screens
white_color = (255, 255, 255)
black_color = (0, 0, 0)

# Center of the screen
screen_center = 400
screen_bottom = 550
screen_gap = 400  # space between two group of text in credits screen

# Game_controller.py
IMAGE_SIZE_MISMATCH = 50  # Used for better representation of player eating other fishes (in pixels)
FISH_SIZE_DIFFERENCE = 10  # It does not make sense if player with size of 401 can eat fish with 402 size (in percent)
SCORE_PERCENT = 5  # Percent of fish size that will be added to player's SCORE after eating (in percent)
SIZE_PERCENT = 5  # Percent of fish size that will be added to player's SIZE after eating (in percent)
DANGER_FISH_SPAWN_FREQUENCY = 20  # (In seconds)
DANGER_SIGH_INTERVAL = 3  # Time that danger sign will blink before appearance of the danger fish (in seconds)
SPEED_COEF = 10  # Amount of speed that fish will gain from higher levels (in percent)

# Custom type events
GAME_OVER_EVENT = pygame.event.Event(pygame.USEREVENT)
LEVEL_CHANGED_EVENT = pygame.event.Event(pygame.USEREVENT + 1)
GAME_WIN_EVENT = pygame.event.Event(pygame.USEREVENT + 2)
SKIP_INTRO_EVENT = pygame.event.Event(pygame.USEREVENT + 3)

# Npc.py
MIN_DISTANCE = 30 # minimal distance between two fishes (in pixels)
DANGER_FISH_SIZE = 9999
PLAYER_BASE_SIZE = 200

# Levels
NUM_OF_LEVELS = 4

# Image and sound path
background_music_path = './audio/background_soundtrack.wav'
eating_sound_path = './audio/eating_sound.wav'
danger_sign_path = './img/npcs/danger/danger-sign1.png'
game_background_path = './img/background/background.jpg'
other_screens_background_path = './img/mywork/other_background.jpg'
intro_screen_background_path = './img/mywork/intro.jpg'

player_first_image_properties = ['./img/player/lvl1/', 'blue', '.png']
player_second_image_properties = ['./img/player/lvl1/', 'light', '.png']
player_third_image_properties = ['./img/player/lvl1/', 'shark', '.png']

player_chosen_image_properties = 0  # set after the hero choosing screen

# Starting screen images
choose_your_hero_img = './img/mywork/choose_your_fish_text.png'
start_new_game_img = './img/mywork/new_game_text.png'
about_img = './img/mywork/about_text.png'
credits_img = './img/mywork/credits_text.png'
quit_game_img = './img/mywork/quit_game_text.png'


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