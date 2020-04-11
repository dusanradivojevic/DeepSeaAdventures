import pygame
from background import Background
from npc import *
import random
import sys
from threading import Thread
from player import Player
from game_controller import *

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


def main():
    pygame.init()

    # Game screen options
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Feeding Frenzy")
    icon = pygame.image.load('./img/logo/fish-512.png')
    pygame.display.set_icon(icon)

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

    player = Player('./img/npcs/YellowFish.png', 0, 0, 350)

    game_controller = GameController(listOfFishes, player)
    components.append(game_controller)

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_threads(components)
                print(f'Score: {game_controller.score}, size: {player.size}, time: {game_controller.played_time}')
                return

            elif event.type == pygame.USEREVENT:
                if event == GAME_OVER_EVENT:
                    running = False
                    stop_threads(components)
                    print(f'Score: {game_controller.score}, size: {player.size}, time: {game_controller.played_time}')
                    continue

        # Screen redraw
        screen.fill([255, 255, 255])
        screen.blit(background.image, background.rect)

        movement_controller.control()
        for fish in listOfFishes:
            if not fish.alive:
                continue

            fish.swim()
            screen.blit(fish.current_image, fish.rect)

            if fish.direction.value < 0:
                fish.current_image = pygame.image.load(fish.image_reverse)
            else:
                fish.current_image = pygame.image.load(fish.image)

        player.move()
        game_controller.start()

        screen.blit(player.current_image, player.rect)

        # Showing score
        score_surface = font.render(game_controller.get_score(), False, text_color)
        screen.blit(score_surface, (SCORE_POSITION_LEFT, SCORE_POSITION_TOP))
        #
        pygame.display.update()
        # End of redraw

main()