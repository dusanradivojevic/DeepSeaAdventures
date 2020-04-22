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
from fish_generator import FishGenerator
from movement_controller import MovementController

components = []  # Objects whose methods were used in threads


def moving_text(screen, font, text, color, speed, direction, other):
    text_width, text_height = pygame.font.Font.size(font, text)
    text_surface = font.render(text, False, color)

    if direction == Direction.West:
        position = [gd.SCREEN_WIDTH + text_width, gd.SCREEN_HEIGHT / 2 - text_height / 2]
    elif direction == Direction.East:
        position = [0 - text_width, gd.SCREEN_HEIGHT / 2 - text_height / 2]
    elif direction == Direction.South:
        position = [gd.SCREEN_WIDTH / 2 - text_width / 2, 0 - text_height]
    elif direction == Direction.North:
        position = [gd.SCREEN_WIDTH / 2 - text_width / 2, gd.SCREEN_HEIGHT + text_height]

    gone_off = False
    while not gone_off:
        # other items
        for item in other:
            screen.blit(item[0], item[1])
        #####

        position = [round(position[0]), round(position[1])]
        screen.blit(text_surface, position)
        pygame.display.update()

        if direction == Direction.West:
            if position[0] < 0 - text_width:
                gone_off = True
            position[0] -= speed
        elif direction == Direction.East:
            if position[0] > gd.SCREEN_WIDTH + text_width:
                gone_off = True
            position[0] += speed
        elif direction == Direction.South:
            if position[1] > gd.SCREEN_HEIGHT + text_height:
                gone_off = True
            position[1] += speed
        elif direction == Direction.North:
            if position[1] < 0 - text_height:
                gone_off = True
            position[1] -= speed


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
    background = Background(gd.game_background_path, [0, 0])

    # Score text
    font_size = 28
    font = pygame.font.SysFont(gd.general_font_name, font_size)
    level_font = pygame.font.SysFont(gd.general_font_name, 2 * font_size)

    listOfFishes = []

    generator = FishGenerator(gd.TANK_CAPACITY, gd.SPAWN_FREQUENCY, listOfFishes)
    generator_thread = Thread(target=generator.start)
    generator_thread.start()
    components.append(generator)

    movement_controller = MovementController(listOfFishes)

    player = Player(gd.player_chosen_image_properties[0], gd.player_chosen_image_properties[1],
                    gd.player_chosen_image_properties[2], (0, 0), 350, -1)
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

            if event == gd.GAME_OVER_EVENT:
                running = False
                stop_threads(components)
                return other_screens.ending_screen(screen, 'GAME OVER :(', game_controller.score,
                                                   game_controller.played_time, len(game_controller.fish_eaten))
            if event == gd.GAME_WIN_EVENT:
                running = False
                stop_threads(components)
                return other_screens.ending_screen(screen, 'YOU WIN :)', game_controller.score,
                                                   game_controller.played_time, len(game_controller.fish_eaten))
            if event == gd.LEVEL_CHANGED_EVENT:
                generator.stop()
                # Clearing the tank
                generator.clear_tank()
                #
                # Text
                others = [  # items that stay on screen while changig level
                    [background.image, background.rect],
                    [player.current_image, player.rect]
                ]
                moving_text(screen, level_font, 'LEVEL UP!', gd.white_color, 10, Direction.North, others)
                moving_text(screen, level_font, game_controller.get_level(), gd.white_color, 10, Direction.West, others)
                #
                # Speeding up fish
                for fish in listOfFishes:
                    fish.speed_up()
                #
                Thread(target=generator.start).start()

        # Screen redraw
        screen.fill(gd.black_color)
        screen.blit(background.image, background.rect)

        movement_controller.control()
        for fish in listOfFishes:
            if fish.id != -1 and not fish.alive and fish.size < gd.DANGER_FISH_SIZE:
                listOfFishes.pop(find_index_of_fish(listOfFishes, fish))
                continue

            if fish.size == gd.DANGER_FISH_SIZE and fish.gone_out_of_the_screen:
                listOfFishes.pop(find_index_of_fish(listOfFishes, fish))
                continue

            fish.swim()  # this calls player's method too
            screen.blit(fish.current_image, fish.rect)

        # player.move()
        game_controller.start()

        # Showing score and level
        level_surface = font.render(game_controller.get_level(), False, gd.white_color)
        score_surface = font.render(game_controller.get_score(), False, gd.white_color)
        screen.blit(level_surface, (gd.SCORE_POSITION_LEFT, gd.SCORE_POSITION_TOP - font_size))
        screen.blit(score_surface, (gd.SCORE_POSITION_LEFT, gd.SCORE_POSITION_TOP))
        #####

        # Showing task
        task_surfaces = game_controller.get_text_surface(font)
        for i in range(len(task_surfaces)):
            screen.blit(task_surfaces[i], (gd.TASK_POSITION_LEFT, gd.TASK_POSITION_TOP + (i * font_size)))
        #####

        # Player
        screen.blit(player.current_image, player.rect)

        pygame.display.update()
        # End of redraw


def main():
    pygame.init()

    # Background sound
    # back_sound = SoundPlayer(gd.background_music_path, True)
    # back_sound.play()

    # Game screen options
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    w, h = screen.get_size()
    gd.set_property('SCREEN_WIDTH', w)
    gd.set_property('SCREEN_HEIGHT', h)
    gd.set_property('screen', screen)

    pygame.display.set_caption(gd.screen_caption)
    icon = pygame.image.load(gd.screen_icon_path)
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

            if signal == Screen_Enum.HeroChoice:
                signal = other_screens.hero_choosing_screen(screen)

            # if signal == Screen_Enum.GameOver:
            #     signal = other_screens.ending_screen()

    except Exception as e:
        print('ERROR: ' + str(e))
        stop_threads(components)


main()