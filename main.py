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
import game_data as gd

components = []  # Objects whose methods were used in threads


def find_index_of_fish(list, fish):
    for i in range(len(list)):
        if fish.id == list[i].id:
            return i

    return -1


def stop_threads(list):
    for item in list:
        item.stop()


def main_screen(screen):
    # Cursor visibility
    pygame.mouse.set_visible(False)

    # Background
    background = Background('./img/background/bottom-of-the-sea-background.jpg', [0, 0])

    # Score text
    text_color = (255, 255, 255)  # White
    font_size = 28
    font = pygame.font.SysFont('Comic Sans MS', font_size)

    listOfFishes = []

    generator = FishGenerator(gd.TANK_CAPACITY, gd.SPAWN_FREQUENCY, listOfFishes)
    generator_thread = Thread(target=generator.start)
    generator_thread.start()
    components.append(generator)

    movement_controller = MovementController(listOfFishes)

    player = Player('./img/npcs/downloads/', 'fish', '.png', (0, 0), 350, -1)
    listOfFishes.append(player)

    game_controller = GameController(listOfFishes, player, generator)
    components.append(game_controller)

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_threads(components)
                return Screen_Enum.EXIT

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    stop_threads(components)
                    return Screen_Enum.Start

            if event.type == pygame.USEREVENT:
                if event == GAME_OVER_EVENT:
                    running = False
                    stop_threads(components)
                    return other_screens.ending_screen(screen, game_controller.score, game_controller.played_time,
                                                       len(game_controller.fish_eaten))

        # Screen redraw
        screen.fill([255, 255, 255])
        screen.blit(background.image, background.rect)

        movement_controller.control()
        for fish in listOfFishes:
            if fish.id != -1 and not fish.alive and fish.size < gd.DANGER_FISH_SIZE:
                listOfFishes.pop(find_index_of_fish(listOfFishes, fish))
                continue

            if fish.size == gd.DANGER_FISH_SIZE and fish.gone_out_of_the_screen:
                listOfFishes.pop(find_index_of_fish(listOfFishes, fish))
                continue

            fish.swim()
            screen.blit(fish.current_image, fish.rect)

        # player.move()
        game_controller.start()

        screen.blit(player.current_image, player.rect)

        # Showing score and level
        level_surface = font.render(game_controller.get_level(), False, text_color)
        score_surface = font.render(game_controller.get_score(), False, text_color)
        screen.blit(level_surface, (gd.SCORE_POSITION_LEFT, gd.SCORE_POSITION_TOP - font_size))
        screen.blit(score_surface, (gd.SCORE_POSITION_LEFT, gd.SCORE_POSITION_TOP))
        #
        pygame.display.update()
        # End of redraw


def main():
    pygame.init()

    # Background sound
    # back_sound = SoundPlayer('./audio/Dan Balan - Lendo Calendo ft. Tany Vander & Brasco (Lyric Video).wav', True)
    # back_sound.play()

    # Game screen options
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    w, h = screen.get_size()
    gd.set_property('SCREEN_WIDTH', w)
    gd.set_property('SCREEN_HEIGHT', h)
    gd.set_property('screen', screen)

    pygame.display.set_caption("Feeding Frenzy")
    icon = pygame.image.load('./img/logo/fish-512.png')
    pygame.display.set_icon(icon)

    try:
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

    except Exception as e:
        print('ERROR: ' + str(e))
        stop_threads(components)


main()