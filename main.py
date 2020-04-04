import pygame
from background import Background
from npc import *
import random
from threading import Thread

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def main():
    pygame.init()

    # Game screen options
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Feeding Frenzy")
    icon = pygame.image.load('./img/logo/fish-512.png')
    pygame.display.set_icon(icon)

    background = Background('./img/background/6riverrock.jpg', [0, 0])


    listOfFishes = []
    generator = FishGenerator(5, 2, listOfFishes)
    thread = Thread(target=generator.start)
    thread.start()
    movement_controller = MovementController(listOfFishes)
    thread = Thread(target=movement_controller.start_control)
    thread.start()

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                generator.work = False
                movement_controller.work = False
                for fish in listOfFishes:
                    fish.alive = False
                continue

        screen.fill([255, 255, 255])
        screen.blit(background.image, background.rect)

        for fish in listOfFishes:
            screen.blit(fish.current_image, fish.rect)

            if fish.direction.value < 0:
                fish.current_image = pygame.image.load(fish.image_reverse)
            else:
                fish.current_image = pygame.image.load(fish.image)

        pygame.display.update()


main()