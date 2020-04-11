import pygame, sys
from button import Button
from background import Background
import time
import threading

# Font & colors
white_color = (255, 255, 255)
black_color = (0, 0, 0)

# Center of the screen
screen_center = 400
screen_bottom = 550
screen_gap = 400  # space between two group of text


def starting_screen(screen):
    # Font
    font = pygame.font.SysFont('Comic Sans MS', 28)

    # Background
    background = Background('./img/background/background_blue_patterns_.jpg', [0, 0])

    # Buttons
    start_new_game_btn = Button(screen_center, 100, font, white_color,  'Start new game')
    credits_btn = Button(screen_center, 250, font,  white_color, 'Credits')
    quit_btn = Button(screen_center, 400, font,  white_color, 'Quit game')

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

            elif event.type == pygame.MOUSEBUTTONUP:
                if start_new_game_btn.collision(pygame.mouse.get_pos()):
                    return
                elif credits_btn.collision(pygame.mouse.get_pos()):
                    credits_screen(screen)
                elif quit_btn.collision(pygame.mouse.get_pos()):
                    sys.exit(0)

        # Screen redraw
        screen.fill([255, 255, 255])
        screen.blit(background.image, background.rect)
        screen.blit(start_new_game_btn.get_button(), start_new_game_btn.get_position())
        screen.blit(credits_btn.get_button(), credits_btn.get_position())
        screen.blit(quit_btn.get_button(), quit_btn.get_position())

        pygame.display.update()


def credits_screen(screen):
    # Font
    font_size = 28
    font = pygame.font.SysFont('Comic Sans MS', font_size)

    # Background
    background = Background('./img/background/background_blue_patterns_.jpg', [0, 0])

    # Texts
    texts = ['Author:', 'Dusan Radivojevic', 'Year:', '2020']

    text_renders = []
    for i in range(len(texts)):
        text_renders.append(font.render(texts[i], False, white_color))

    text_rects = [
        [text_renders[0], [screen_center - (pygame.font.Font.size(font, texts[0])[0] / 2), screen_bottom]],
        [text_renders[1], [screen_center - (pygame.font.Font.size(font, texts[1])[0] / 2), screen_bottom + font_size]],
        [text_renders[2], [screen_center - (pygame.font.Font.size(font, texts[2])[0] / 2), screen_bottom + (1 * screen_gap)]],
        [text_renders[3], [screen_center - (pygame.font.Font.size(font, texts[3])[0] / 2), screen_bottom + (1 * screen_gap) + font_size]]
        # [text_renders[4], [screen_center - (pygame.font.Font.size(font, texts[4])[0] / 2), screen_bottom + (2 * screen_gap)]],
        # [text_renders[5], [screen_center - (pygame.font.Font.size(font, texts[5])[0] / 2), screen_bottom + (2 * screen_gap) + font_size]]
    ]

    ###

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

            elif event.type == pygame.MOUSEBUTTONUP:
                return  # to start menu

        # Screen redraw
        screen.fill([255, 255, 255])
        screen.blit(background.image, background.rect)

        for i in range(len(text_rects)):
            screen.blit(text_rects[i][0], text_rects[i][1])
            text_rects[i][1][1] -= 2  # speed of rising text

        pygame.display.update()


class BlinkingText:
    def __init__(self, screen, font, text, position, freq):
        self.screen = screen
        self.font = font
        self.text = text
        self.position = position
        self.frequency = freq
        self.active = True
        self.switch = True

    def stop(self):
        self.active = False

    def start(self):
        prepared_text = self.font.render(self.text, False, white_color)
        self.switcher()
        while self.active:
            if self.switch:
                self.screen.blit(prepared_text, self.position)

    def switcher(self):
        if not self.active:
            return

        threading.Timer(self.frequency, self.switcher).start()  # waits self.frequency amount of seconds before it calls itself
        self.switch = not self.switch


def ending_screen(screen, score, time_played, fish_eaten):
    time.sleep(1)

    # Font
    font_size = 28
    font = pygame.font.SysFont('Comic Sans MS', font_size)
    font_size_big = 36
    font_big = pygame.font.SysFont('Comic Sans MS', font_size_big)

    # Background
    background = Background('./img/background/background_blue_patterns_.jpg', [0, 0])

    # Texts

    texts = [
        font.render(f'Score: {score}', False, white_color),
        font.render(f'Fish eaten: {fish_eaten}', False, white_color),
        font.render(f'Time played: {time_played}', False, white_color),
        font.render('Thank you for playing!', False, white_color)
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
                sys.exit(0)

            elif event.type == pygame.MOUSEBUTTONUP:
                blink.stop()
                return  # to start menu

        # Screen redraw
        screen.fill([255, 255, 255])
        screen.blit(background.image, background.rect)

        for i in range(len(texts)):
            # Game over text
            screen.blit(font_big.render('GAME OVER :(', False, white_color), [200, starting_height - (2 * font_size_big)])
            #

            if i == 3:
                screen.blit(texts[i], [200, starting_height + (i * font_size + font_size)])
            else:
                screen.blit(texts[i], [200, starting_height + (i * font_size)])


        pygame.display.update()