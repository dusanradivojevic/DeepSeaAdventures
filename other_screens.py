import pygame, sys
from button import Button
from background import Background
import time
import threading
from enum import Enum
import game_data as gd


class Screen(Enum):
    EXIT = 0
    Game = 1
    Start = 2
    Credits = 3
    GameOver = 4


def starting_screen(screen):
    # Cursor visibility
    pygame.mouse.set_visible(True)

    # Font
    font = pygame.font.SysFont('Comic Sans MS', 28)

    # Background
    background = Background('./img/background/abstract-dark-blue-polygonal-background-abstraktsiia-geometr.jpg', [0, 0])

    # Buttons
    start_new_game_btn = Button(gd.screen_center, 0.25 * gd.SCREEN_HEIGHT, font, gd.white_color,  'Start new game')
    credits_btn = Button(gd.screen_center, 0.45 * gd.SCREEN_HEIGHT, font,  gd.white_color, 'Credits')
    quit_btn = Button(gd.screen_center, 0.65 * gd.SCREEN_HEIGHT, font,  gd.white_color, 'Quit game')

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return Screen.EXIT
            elif event.type == pygame.MOUSEBUTTONUP:
                if start_new_game_btn.collision(pygame.mouse.get_pos()):
                    return Screen.Game
                elif credits_btn.collision(pygame.mouse.get_pos()):
                    return Screen.Credits
                elif quit_btn.collision(pygame.mouse.get_pos()):
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
    font_size = 28
    font = pygame.font.SysFont('Comic Sans MS', font_size)

    # Background
    background = Background('./img/background/abstract-dark-blue-polygonal-background-abstraktsiia-geometr.jpg', [0, 0])

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

            elif event.type == pygame.MOUSEBUTTONUP:
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


def ending_screen(screen, score, time_played, fish_eaten):
    time.sleep(1)   # for smoother screen transition

    # Cursor visibility
    pygame.mouse.set_visible(True)

    # Font
    font_size = 28
    font = pygame.font.SysFont('Comic Sans MS', font_size)
    font_size_big = 36
    font_big = pygame.font.SysFont('Comic Sans MS', font_size_big)

    # Background
    background = Background('./img/background/background_blue_patterns_.jpg', [0, 0])

    # Texts
    texts = [
        font.render(f'Score: {score}', False, gd.white_color),
        font.render(f'Fish eaten: {fish_eaten}', False, gd.white_color),
        font.render(f'Time played: {time_played}', False, gd.white_color),
        font.render('Thank you for playing!', False, gd.white_color)
    ]

    starting_height = 200

    blink = BlinkingText(screen, font, 'Press any key to continue...', [200, starting_height + (8 * font_size)], 0.7)
    blink_thread = threading.Thread(target=blink.start)
    blink_thread.start()
    ###

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                blink.stop()
                return Screen.EXIT

            elif event.type == pygame.MOUSEBUTTONUP:
                blink.stop()
                time.sleep(0.5)  # for smoother transition
                return Screen.Start

        # Screen redraw
        screen.fill([255, 255, 255])
        screen.blit(background.image, background.rect)

        for i in range(len(texts)):
            # Game over text
            screen.blit(font_big.render('GAME OVER :(', False, gd.white_color), [200, starting_height - (2 * font_size_big)])
            #

            if i == 3:
                screen.blit(texts[i], [200, starting_height + (i * font_size + font_size)])
            else:
                screen.blit(texts[i], [200, starting_height + (i * font_size)])

        pygame.display.update()
