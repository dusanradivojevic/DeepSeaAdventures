import pygame
from background import Background
from npc import *
import random
import sys
from threading import Thread
from player import Player
from game_controller import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def stop_threads(list, fishes):
    for item in list:
        item.stop()

    for fish in fishes:
        fish.stop()

def main():
    pygame.init()

    # Game screen options
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Feeding Frenzy")
    icon = pygame.image.load('./img/logo/fish-512.png')
    pygame.display.set_icon(icon)

    background = Background('./img/background/6riverrock.jpg', [0, 0])


    listOfFishes = []
    components = []  # Objects whose methods were used in threads

    generator = FishGenerator(5, 2, listOfFishes)
    generator_thread = Thread(target=generator.start)
    generator_thread.start()
    components.append(generator)

    movement_controller = MovementController(listOfFishes)
    movement_thread = Thread(target=movement_controller.start_control)
    movement_thread.start()
    components.append(movement_controller)

    player = Player('./img/npcs/YellowFish.png', 0, 0, 350)
    player_thread = Thread(target=player.start)
    player_thread.start()
    components.append(player)

    game_controller = GameController(listOfFishes, player)
    game_controller_thread = Thread(target=game_controller.start)
    game_controller_thread.start()
    components.append(game_controller)

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_threads(components, listOfFishes)
                print(f'Score: {game_controller.score}, size: {player.size}, time: {game_controller.played_time}')
                return

            elif event.type == pygame.USEREVENT:
                if event == GAME_OVER_EVENT:
                    running = False
                    stop_threads(components, listOfFishes)
                    print(f'Score: {game_controller.score}, size: {player.size}, time: {game_controller.played_time}')
                    continue

        # Screen redraw
        screen.fill([255, 255, 255])
        screen.blit(background.image, background.rect)

        for fish in listOfFishes:
            if not fish.alive:
                continue

            screen.blit(fish.current_image, fish.rect)

            if fish.direction.value < 0:
                fish.current_image = pygame.image.load(fish.image_reverse)
            else:
                fish.current_image = pygame.image.load(fish.image)

        screen.blit(player.current_image, player.rect)
        pygame.display.update()
        # End of redraw

main()