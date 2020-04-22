import pygame, sys
from button import Button
from background import Background
import time
import threading
from enum import Enum
import game_data as gd
from player import Player


class Screen(Enum):
    EXIT = 0
    Game = 1
    Start = 2
    Credits = 3
    GameOver = 4
    HeroChoice = 5


def starting_screen(screen):
    # Cursor visibility
    pygame.mouse.set_visible(True)

    # Font
    font_size = 36
    font = pygame.font.SysFont(gd.general_font_name, font_size)

    # Background
    background = Background(gd.other_screens_background_path, [0, 0])

    # Buttons
    start_new_game_btn = Button(gd.screen_center, 0.25 * gd.SCREEN_HEIGHT, font, gd.white_color,  'Start new game')
    credits_btn = Button(gd.screen_center, 0.45 * gd.SCREEN_HEIGHT, font,  gd.white_color, 'Credits')
    quit_btn = Button(gd.screen_center, 0.65 * gd.SCREEN_HEIGHT, font,  gd.white_color, 'Quit game')

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return Screen.EXIT

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return Screen.Game

            if event.type == pygame.MOUSEBUTTONUP:
                if start_new_game_btn.collision(pygame.mouse.get_pos()):
                    # return Screen.Game
                    return Screen.HeroChoice
                if credits_btn.collision(pygame.mouse.get_pos()):
                    return Screen.Credits
                if quit_btn.collision(pygame.mouse.get_pos()):
                    return Screen.EXIT

        # Screen redraw
        screen.fill([255, 255, 255])
        screen.blit(background.image, background.rect)
        screen.blit(start_new_game_btn.get_button(), start_new_game_btn.get_position())
        screen.blit(credits_btn.get_button(), credits_btn.get_position())
        screen.blit(quit_btn.get_button(), quit_btn.get_position())

        pygame.display.update()


def credits_screen(screen):
    # Cursor visibility
    pygame.mouse.set_visible(True)

    # Font
    font_size = 36
    font = pygame.font.SysFont(gd.general_font_name, font_size)

    # Background
    background = Background(gd.other_screens_background_path, [0, 0])

    # Texts
    texts = ['Author:', 'Dusan Radivojevic', 'Year:', '2020']

    text_renders = []
    for i in range(len(texts)):
        text_renders.append(font.render(texts[i], False, gd.white_color))

    text_rects = [
        [text_renders[0], [gd.screen_center - (pygame.font.Font.size(font, texts[0])[0] / 2), gd.screen_bottom]],
        [text_renders[1], [gd.screen_center - (pygame.font.Font.size(font, texts[1])[0] / 2), gd.screen_bottom + font_size]],
        [text_renders[2], [gd.screen_center - (pygame.font.Font.size(font, texts[2])[0] / 2), gd.screen_bottom + (1 * gd.screen_gap)]],
        [text_renders[3], [gd.screen_center - (pygame.font.Font.size(font, texts[3])[0] / 2), gd.screen_bottom + (1 * gd.screen_gap) + font_size]]
        # [text_renders[4], [screen_center - (pygame.font.Font.size(font, texts[4])[0] / 2), screen_bottom + (2 * screen_gap)]],
        # [text_renders[5], [screen_center - (pygame.font.Font.size(font, texts[5])[0] / 2), screen_bottom + (2 * screen_gap) + font_size]]
    ]

    blink = BlinkingText(screen, font, 'Press any key to continue...',
                         [gd.screen_center - (pygame.font.Font.size(font, 'Press any key to continue...')[0] / 2),
                          gd.SCREEN_HEIGHT / 2],
                         0.7)
    ###

    finished_flag = False  # used for starting blinking text at the end of credits
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                blink.stop()
                return Screen.EXIT

            if event.type == pygame.MOUSEBUTTONUP:
                blink.stop()
                return Screen.Start

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    blink.stop()
                    return Screen.Start

        # Screen redraw
        screen.fill([255, 255, 255])
        screen.blit(background.image, background.rect)

        if not finished_flag:
            if text_rects[len(text_rects) - 1][1][1] < -100:
                finished_flag = True
                blink_thread = threading.Thread(target=blink.start)
                blink_thread.start()

            else:
                for i in range(len(text_rects)):
                    screen.blit(text_rects[i][0], text_rects[i][1])
                    text_rects[i][1][1] -= 5  # speed of rising text

        pygame.display.update()


class BlinkingText:
    def __init__(self, screen, font, text, position, freq):
        self.screen = screen
        self.font = font
        self.text = text
        self.position = position
        self.frequency = freq
        self.active = True
        self.switch = False

    def stop(self):
        self.active = False

    def start(self):
        prepared_text = self.font.render(self.text, False, gd.white_color)
        self.switcher()
        while self.active:
            if self.switch:
                self.screen.blit(prepared_text, self.position)

    def switcher(self):
        if not self.active:
            return

        # waits self.frequency amount of seconds before it calls itself
        threading.Timer(self.frequency, self.switcher).start()
        self.switch = not self.switch


def ending_screen(screen, header_text, score, time_played, fish_eaten):
    time.sleep(1)   # for smoother screen transition

    # Cursor visibility
    pygame.mouse.set_visible(True)

    # Font
    font_size = 28
    font = pygame.font.SysFont(gd.general_font_name, font_size)
    font_size_big = 36
    font_big = pygame.font.SysFont(gd.general_font_name, font_size_big)

    # Background
    background = Background(gd.other_screens_background_path, [0, 0])

    # Texts
    texts = [
        font.render(f'Score: {score}', False, gd.white_color),
        font.render(f'Fish eaten: {fish_eaten}', False, gd.white_color),
        font.render(f'Time played: {time_played}', False, gd.white_color),
        font.render('Thank you for playing!', False, gd.white_color)
    ]

    # Screen location
    starting_height = round(gd.SCREEN_HEIGHT / 3)
    width = gd.screen_center - 200

    blink = BlinkingText(screen, font, 'Press any key to continue...', [width, starting_height + (8 * font_size)], 0.7)
    blink_thread = threading.Thread(target=blink.start)
    blink_thread.start()
    ###

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                blink.stop()
                return Screen.EXIT

            if event.type == pygame.MOUSEBUTTONUP:
                blink.stop()
                time.sleep(0.5)  # for smoother transition
                return Screen.Start

        # Screen redraw
        screen.fill([255, 255, 255])
        screen.blit(background.image, background.rect)

        for i in range(len(texts)):
            # Game over text
            screen.blit(font_big.render(header_text, False, gd.white_color), [width, starting_height - (2 * font_size_big)])
            #

            if i == 3:
                screen.blit(texts[i], [width, starting_height + (i * font_size + font_size)])
            else:
                screen.blit(texts[i], [width, starting_height + (i * font_size)])

        pygame.display.update()


def hero_choosing_screen(screen):
    # Cursor visibility
    pygame.mouse.set_visible(True)

    # Font
    font_size = 36
    font = pygame.font.SysFont(gd.general_font_name, font_size)

    # Fish image size
    image = pygame.image.load(gd.player_first_image_properties[0] + gd.player_first_image_properties[1] + '0' +
                    gd.player_first_image_properties[2])
    w, h = image.get_rect().size

    # Text
    text_surface = font.render('Choose your hero!', False, gd.white_color)
    text_pos = [gd.SCREEN_WIDTH / 2 - text_surface.get_rect().size[0] / 2, gd.SCREEN_HEIGHT / 2 - 2 * h]

    # Background
    background = Background(gd.game_background_path, [0, 0])

    # Positions
    y = gd.SCREEN_HEIGHT / 2 - h / 2
    pos1 = [gd.SCREEN_WIDTH / 3 - 2 * w, y]
    pos2 = [2 * gd.SCREEN_WIDTH / 3 - 2 * w, y]
    pos3 = [3 * gd.SCREEN_WIDTH / 3 - 2 * w, y]

    # Hero images
    player1 = Player(gd.player_first_image_properties[0], gd.player_first_image_properties[1],
                    gd.player_first_image_properties[2], pos1, 350, -1)
    player2 = Player(gd.player_second_image_properties[0], gd.player_second_image_properties[1],
                     gd.player_second_image_properties[2], pos2, 350, -1)
    player3 = Player(gd.player_third_image_properties[0], gd.player_third_image_properties[1],
                     gd.player_third_image_properties[2], pos3, 350, -1)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return Screen.EXIT

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return Screen.Start

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if player1.rect.collidepoint(mouse_pos):
                    gd.player_chosen_image_properties = gd.player_first_image_properties
                    return Screen.Game
                if player2.rect.collidepoint(mouse_pos):
                    gd.player_chosen_image_properties = gd.player_second_image_properties
                    return Screen.Game
                if player3.rect.collidepoint(mouse_pos):
                    gd.player_chosen_image_properties = gd.player_third_image_properties
                    return Screen.Game

        # Screen redraw
        screen.fill([255, 255, 255])
        screen.blit(background.image, background.rect)
        screen.blit(text_surface, text_pos)
        screen.blit(player1.current_image, player1.rect)
        screen.blit(player2.current_image, player2.rect)
        screen.blit(player3.current_image, player3.rect)
        ###
        # Image animation
        player1.pickImage()
        player2.pickImage()
        player3.pickImage()
        ###

        pygame.display.update()