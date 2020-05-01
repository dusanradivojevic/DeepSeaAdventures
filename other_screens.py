import pygame
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
    AboutGame = 6
    Intro = 7


def starting_screen(screen):
    # Cursor visibility
    pygame.mouse.set_visible(True)

    # Font
    # font_size = 36
    # font = pygame.font.SysFont(gd.general_font_name, font_size)

    # Background
    background = Background(gd.other_screens_background_path, [0, 0])

    # Buttons
    # start_new_game_btn = Button(gd.screen_center, 0.20 * gd.SCREEN_HEIGHT, font, gd.white_color,  'Start new game')
    # instr_btn = Button(gd.screen_center, 0.40 * gd.SCREEN_HEIGHT, font, gd.white_color, 'About game')
    # credits_btn = Button(gd.screen_center, 0.60 * gd.SCREEN_HEIGHT, font,  gd.white_color, 'Credits')
    # quit_btn = Button(gd.screen_center, 0.80 * gd.SCREEN_HEIGHT, font,  gd.white_color, 'Quit game')
    start_new_game_btn = pygame.image.load(gd.start_new_game_img)
    instr_btn = pygame.image.load(gd.about_img)
    credits_btn = pygame.image.load(gd.credits_img)
    quit_btn = pygame.image.load(gd.quit_game_img)

    # Positions
    start_pos = [gd.screen_center - start_new_game_btn.get_rect().width / 2, 0.2 * gd.SCREEN_HEIGHT]
    instr_pos = [gd.screen_center - instr_btn.get_rect().width / 2, 0.4 * gd.SCREEN_HEIGHT]
    credits_pos = [gd.screen_center - credits_btn.get_rect().width / 2, 0.6 * gd.SCREEN_HEIGHT]
    quit_pos = [gd.screen_center - quit_btn.get_rect().width / 2, 0.8 * gd.SCREEN_HEIGHT]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return Screen.EXIT

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return Screen.Game

            if event.type == pygame.MOUSEBUTTONUP:
                if start_new_game_btn.get_rect(left=start_pos[0], top=start_pos[1]).collidepoint(pygame.mouse.get_pos()):
                    return Screen.HeroChoice
                if instr_btn.get_rect(left=instr_pos[0], top=instr_pos[1]).collidepoint(pygame.mouse.get_pos()):
                    return Screen.AboutGame
                if credits_btn.get_rect(left=credits_pos[0], top=credits_pos[1]).collidepoint(pygame.mouse.get_pos()):
                    return Screen.Credits
                if quit_btn.get_rect(left=quit_pos[0], top=quit_pos[1]).collidepoint(pygame.mouse.get_pos()):
                    return Screen.EXIT

        # Screen redraw
        screen.fill([255, 255, 255])
        # screen.blit(background.image, background.rect)
        screen.blit(background.image, ((0.5 * gd.SCREEN_WIDTH) - (0.5 * background.image.get_width()),
                                       (0.5 * gd.SCREEN_HEIGHT) - (0.5 * background.image.get_height())))
        # screen.blit(start_new_game_btn.get_button(), start_new_game_btn.get_position())
        # screen.blit(instr_btn.get_button(), instr_btn.get_position())
        # screen.blit(credits_btn.get_button(), credits_btn.get_position())
        # screen.blit(quit_btn.get_button(), quit_btn.get_position())
        screen.blit(start_new_game_btn, start_pos)
        screen.blit(instr_btn, instr_pos)
        screen.blit(credits_btn, credits_pos)
        screen.blit(quit_btn, quit_pos)

        pygame.display.update()


def about_the_game_screen(screen):
    # Cursor visibility
    pygame.mouse.set_visible(True)

    # Font
    font_size = 24
    font = pygame.font.SysFont(gd.general_font_name, font_size)

    # Background
    background = Background(gd.other_screens_background_path, [0, 0])

    # Positions
    desc_x = round(1/4 * gd.SCREEN_WIDTH)
    desc_y = 100

    instr_x = round(3/4 * gd.SCREEN_WIDTH)
    instr_y = desc_y

    # Texts
    desc_lines = [
        "It's survival of the biggest in",
        "this action packed deep-sea challenge.",
        "Eat your way to the top of the food chain",
        "as you swim through stunning underwater environments",
        "and encounter deadly predators.",
        "In Deep-Sea Adventures, players control",
        "a hungry marine predator",
        "intent on munching as many other fish as possible.",
        "The player chooses between 3 aquatic",
        "species each trying to move up",
        "the food chain as the game progresses.",
        "As smaller fish are eaten, the player's",
        "own fish grows in size",
        "and becomes capable of eating somewhat larger fish.",
        "By the end of level 4,",
        "the fish is sufficiently large enough",
        "that it can eat almost anything on-screen.",
        "Players must be vigilant for danger signs",
        "as the ultimate shark predator",
        "might end their adventures."
    ]

    instr_lines = [
        "Players will move their fish using the mouse,",
        "trying to catch other smaller fish",
        "while avoiding bigger fish.",
        "If bigger fish is to catch player's fish,",
        "the game will be over.",
        "Player can pause the game at any point",
        "by pressing the key \"P\"",
        "or exit the game at any point ",
        "by pressing the key \"ESC\".",
        "The danger sign will randomly appear",
        "at the higher levels",
        "and the ultimate shark predator will pass the screen.",
        "If the player's fish gets caught by the",
        "ultimate shark predator, the game will be over.",
        "Completing the tasks will make player's fish bigger",
        "which will give the player the ability ",
        "to eat somewhat larger fish.",
        "Complete all tasks and have fun adventures!"
    ]

    # Surfaces and their positions
    desc_renders = []
    for i in range(len(desc_lines)):
        desc_renders.append(font.render(desc_lines[i], False, gd.white_color))

    desc_rects = []
    for i in range(len(desc_renders)):
        desc_rects.append(
            [
                desc_renders[i], [desc_x - font.size(desc_lines[i])[0] / 2, desc_y + i * font_size * 1.2]
            ]
        )

    instr_renders = []
    for i in range(len(instr_lines)):
        instr_renders.append(font.render(instr_lines[i], False, gd.white_color))

    instr_rects = []
    for i in range(len(instr_renders)):
        instr_rects.append(
            [
                instr_renders[i], [instr_x - font.size(instr_lines[i])[0] / 2, instr_y + i * font_size * 1.2]
            ]
        )

    # Headings
    heading_y = 50
    desc_text = 'Description:'
    instr_text = 'Instruction:'
    desc_heading = [font.render(desc_text, False, gd.white_color), [desc_x - font.size(desc_text)[0] / 2, heading_y]]
    instr_heading = [font.render(instr_text, False, gd.white_color), [instr_x - font.size(instr_text)[0] / 2, heading_y]]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return Screen.EXIT

            if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.KEYUP:
                return Screen.Start

        # Screen redraw
        screen.fill([255, 255, 255])
        screen.blit(background.image, background.rect)

        screen.blit(desc_heading[0], desc_heading[1])
        screen.blit(instr_heading[0], instr_heading[1])

        for i in range(len(desc_rects)):
            screen.blit(desc_rects[i][0], desc_rects[i][1])

        for i in range(len(instr_rects)):
            screen.blit(instr_rects[i][0], instr_rects[i][1])

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
    texts = ['DEEP-SEA ADVENTURES', 'All rights reserved.', 'Author:', 'Milos Djordjevic', 'Created on:',
             '30th of April, 2020', 'Version:', 'Beta 1.1.1']

    text_renders = []
    for i in range(len(texts)):
        text_renders.append(font.render(texts[i], False, gd.white_color))

    text_rects = [
        [text_renders[0], [gd.screen_center - (pygame.font.Font.size(font, texts[0])[0] / 2), gd.screen_bottom]],
        [text_renders[1], [gd.screen_center - (pygame.font.Font.size(font, texts[1])[0] / 2), gd.screen_bottom + font_size]],
        [text_renders[2], [gd.screen_center - (pygame.font.Font.size(font, texts[2])[0] / 2), gd.screen_bottom + (1 * gd.screen_gap)]],
        [text_renders[3], [gd.screen_center - (pygame.font.Font.size(font, texts[3])[0] / 2), gd.screen_bottom + (1 * gd.screen_gap) + font_size]],
        [text_renders[4], [gd.screen_center - (pygame.font.Font.size(font, texts[4])[0] / 2), gd.screen_bottom + (2 * gd.screen_gap)]],
        [text_renders[5], [gd.screen_center - (pygame.font.Font.size(font, texts[5])[0] / 2), gd.screen_bottom + (2 * gd.screen_gap) + font_size]],
        [text_renders[6], [gd.screen_center - (pygame.font.Font.size(font, texts[6])[0] / 2), gd.screen_bottom + (3 * gd.screen_gap)]],
        [text_renders[7], [gd.screen_center - (pygame.font.Font.size(font, texts[7])[0] / 2), gd.screen_bottom + (3 * gd.screen_gap) + font_size]]
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
                # blink.stop()
                return Screen.EXIT

            if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.KEYUP:
                # blink.stop()
                return Screen.Start

        # Screen redraw
        screen.fill([255, 255, 255])
        screen.blit(background.image, background.rect)

        if not finished_flag:
            if text_rects[len(text_rects) - 1][1][1] < -100:
                finished_flag = True
                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP)) # this is instead of blinking text
                # blink_thread = threading.Thread(target=blink.start)
                # blink_thread.start()

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
    font_size = 36
    font = pygame.font.SysFont(gd.general_font_name, font_size)
    font_size_big = 42
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

            if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.KEYUP:
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

    # Hero images
    p1 = ['./img/player/lvl2/', 'blue', '.png']
    p2 = ['./img/player/lvl2/', 'light', '.png']
    p3 = ['./img/player/lvl2/', 'shark', '.png']

    # Font
    # font_size = 36
    # font = pygame.font.SysFont(gd.general_font_name, font_size)

    # Fish image size
    image = pygame.image.load(p1[0] + p1[1] + '0' + p1[2])
    w, h = image.get_rect().size

    # Text
    # text_surface = font.render('Choose your hero!', False, gd.white_color)
    text_surface = pygame.image.load(gd.choose_your_hero_img)
    text_pos = [gd.SCREEN_WIDTH / 2 - text_surface.get_rect().size[0] / 2, gd.SCREEN_HEIGHT / 2 - 1.5 * h]

    # Background
    background = Background(gd.other_screens_background_path, [0, 0])

    # Positions
    y = gd.SCREEN_HEIGHT / 2 - h / 2
    pos1 = [gd.SCREEN_WIDTH / 3 - 1.5 * w, y]
    pos2 = [2 * gd.SCREEN_WIDTH / 3 - 1.5 * w, y]
    pos3 = [3 * gd.SCREEN_WIDTH / 3 - 1.5 * w, y - 50]

    # Player as images
    player1 = Player(p1[0], p1[1], p1[2], pos1, -1)
    player2 = Player(p2[0], p2[1], p2[2], pos2, -1)
    player3 = Player(p3[0], p3[1], p3[2], pos3, -1)

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
        # background.pickImage()
        player1.pickImage()
        player2.pickImage()
        player3.pickImage()
        ###

        pygame.display.update()


def intro_screen(screen):
    # Cursor visibility
    pygame.mouse.set_visible(True)

    # Font
    font_size = 36
    font = pygame.font.SysFont(gd.general_font_name, font_size)

    # Background
    background = Background(gd.intro_screen_background_path, [0, 0])

    blink = BlinkingText(screen, font, 'Press any key to continue...',
                         [gd.screen_center - (pygame.font.Font.size(font, 'Press any key to continue...')[0] / 2),
                          gd.SCREEN_HEIGHT - 3 * font_size], 0.7)
    ###

    blink_thread = threading.Thread(target=blink.start)
    threading.Timer(gd.press_any_key_text_delay, blink_thread.start).start()
    threading.Timer(gd.start_screen_delay, raise_change_screen_event).start()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                blink.stop()
                return Screen.EXIT

            if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.KEYUP:
                blink.stop()
                return Screen.Start

            if event == gd.SKIP_INTRO_EVENT:
                blink.stop()
                return Screen.Start

        # Screen redraw
        screen.fill([255, 255, 255])
        screen.blit(background.image, background.rect)

        pygame.display.update()


# Used for changing screens due to player's inactivity
def raise_change_screen_event():
    pygame.event.post(gd.SKIP_INTRO_EVENT)