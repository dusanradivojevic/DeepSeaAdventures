import time
import math
import pygame
from sounds import SoundPlayer
import game_data as gd
import threading

# Event custom types
GAME_OVER_EVENT = pygame.event.Event(pygame.USEREVENT)


# Changes time lapsed from number of seconds to hours : minutes : seconds format
def time_convert(seconds):
    min = (seconds // 60) % 60
    sec = seconds % 60
    hours = min // 60
    return f'{hours} : {min} : {round(sec,2)}'


class GameController:
    def __init__(self, list, player, generator):
        self.score = 0
        self.fish_eaten = []
        self.start_time = time.time()
        self.end_time = time.time()
        self.played_time = "0"
        self.fishes = list
        self.player = player
        self.generator = generator
        self.work = True
        self.call_danger_fish()

    def stop(self):
        self.work = False
        self.end_time = time.time()
        time_lapsed = self.end_time - self.start_time
        self.played_time = time_convert(time_lapsed)

    def start(self):
        x = self.player.rect.centerx
        y = self.player.rect.centery
        for fish in self.fishes:
            x2 = fish.rect.centerx
            y2 = fish.rect.centery

            min_horizontal_distance = fish.current_image.get_rect().size[0] / 2 + \
                                      self.player.current_image.get_rect().size[0] / 2 + gd.MIN_DISTANCE
            min_vertical_distance = fish.current_image.get_rect().size[1] / 2 + \
                                   self.player.current_image.get_rect().size[1] / 2 + gd.MIN_DISTANCE

            if abs(x2 - x) < min_horizontal_distance / 2 and abs(y2 - y) < min_vertical_distance / 2:
                if self.player.size < ((100 - gd.FISH_SIZE_DIFFERENCE) / 100) * fish.size:
                    self.game_over()
                elif self.player.size > ((100 + gd.FISH_SIZE_DIFFERENCE) / 100) * fish.size:
                    self.eat(fish)

    def call_danger_fish(self):
        if not self.work:
            return

        if round(time.time() - self.start_time) != 0:
            self.generator.spawn_danger_fish()

        threading.Timer(gd.DANGER_FISH_SPAWN_FREQUENCY, self.call_danger_fish).start()

    def get_score(self):
        return f'Score: {self.score}'

    def eat(self, fish):
        SoundPlayer('./audio/eating_sound.wav', False).play()
        fish.stop()
        # self.fishes.pop(find_index_of_fish(self.fishes, fish))
        self.score += (gd.SCORE_PERCENT / 100) * fish.size
        self.fish_eaten.append(fish)
        self.player.size += (gd.SIZE_PERCENT / 100) * fish.size

    def game_over(self):
        # Show end screen
        pygame.event.post(GAME_OVER_EVENT)  # Raises QUIT event (should be changed so it can be
                                                            # distinguished from button interruption)



