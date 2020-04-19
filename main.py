import pygame
from background import Background
from npc import *
import random
import sys
from threading import Thread
from player import Player
from game_controller import *
import other_screens
from sounds import SoundPlayer
from other_screens import Screen as Screen_Enum

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TANK_CAPACITY = 10
SPAWN_FREQUENCY = 2  # every 2 seconds fish spawns
SCORE_POSITION_LEFT = 0
SCORE_POSITION_TOP = 550


def stop_threads(list):
    for item in list:
        item.stop()


def main_screen(screen):
    # Cursor visibility
    pygame.mouse.set_visible(False)

    # Background
    background = Background('./img/background/6riverrock.jpg', [0, 0])

    # Score text
    text_color = (255, 255, 255)  # White
    font = pygame.font.SysFont('Comic Sans MS', 28)

    listOfFishes = []
    components = []  # Objects whose methods were used in threads

    generator = FishGenerator(TANK_CAPACITY, SPAWN_FREQUENCY, listOfFishes)
    generator_thread = Thread(target=generator.start)
    generator_thread.start()
    components.append(generator)

    movement_controller = MovementController(listOfFishes)

    player = Player('./img/npcs/YellowFish0.png', 0, 0, 350)

    game_controller = GameController(listOfFishes, player)
    components.append(game_controller)

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_threads(components)
                return Screen_Enum.EXIT

            elif event.type == pygame.USEREVENT:
                if event == GAME_OVER_EVENT:
                    running = False
                    stop_threads(components)
                    return other_screens.ending_screen(screen, game_controller.score, game_controller.played_time, game_controller.fish_eaten)

        # Screen redraw
        screen.fill([255, 255, 255])
        screen.blit(background.image, background.rect)

        movement_controller.control()
        for fish in listOfFishes:
            if not fish.alive:
                continue

            fish.swim()
            screen.blit(fish.current_image, fish.rect)

        player.move()
        game_controller.start()

        screen.blit(player.current_image, player.rect)

        # Showing score
        score_surface = font.render(game_controller.get_score(), False, text_color)
        screen.blit(score_surface, (SCORE_POSITION_LEFT, SCORE_POSITION_TOP))
        #
        pygame.display.update()
        # End of redraw


def main():
    pygame.init()

    # Background sound
    # back_sound = SoundPlayer('./audio/Dan Balan - Lendo Calendo ft. Tany Vander & Brasco (Lyric Video).wav', True)
    # back_sound.play()

    # Game screen options
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Feeding Frenzy")
    icon = pygame.image.load('./img/logo/fish-512.png')
    pygame.display.set_icon(icon)

    signal = Screen_Enum.Start
    while True:
        if signal == Screen_Enum.EXIT:
            # back_sound.stop()
            return

        if signal == Screen_Enum.Start:
            signal = other_screens.starting_screen(screen)

        if signal == Screen_Enum.Game:
            signal = main_screen(screen)

        if signal == Screen_Enum.Credits:
            signal = other_screens.credits_screen(screen)

        # if signal == Screen_Enum.GameOver:
        #     signal = other_screens.ending_screen()


main()