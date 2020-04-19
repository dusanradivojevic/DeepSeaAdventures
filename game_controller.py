import time
import math
import pygame
from sounds import SoundPlayer
import game_data as gd

# Event custom types
GAME_OVER_EVENT = pygame.event.Event(pygame.USEREVENT)


# Changes time lapsed from number of seconds to hours : minutes : seconds format
def time_convert(seconds):
    min = (seconds // 60) % 60
    sec = seconds % 60
    hours = min // 60
    return f'{hours} : {min} : {round(sec,2)}'


def find_index_of_fish(list, fish):
    for i in range(len(list)):
        if fish.id == list[i].id:
            return i

    return -1


class GameController:
    def __init__(self, list, player):
        self.score = 0
        self.fish_eaten = 0
        self.start_time = time.time()
        self.end_time = time.time()
        self.played_time = "0"
        self.fishes = list
        self.player = player

    def stop(self):
        self.end_time = time.time()
        time_lapsed = self.end_time - self.start_time
        self.played_time = time_convert(time_lapsed)

    def start(self):
        for fish in self.fishes:
            x = self.player.rect.centerx
            y = self.player.rect.centery

            x2 = fish.rect.centerx
            y2 = fish.rect.centery
            if math.sqrt(pow((x2 - x), 2) + pow((y2 - y), 2)) < gd.IMAGE_SIZE_MISMATCH:
                if self.player.size < ((100 - gd.FISH_SIZE_DIFFERENCE) / 100) * fish.size:
                    self.game_over()
                elif self.player.size > ((100 + gd.FISH_SIZE_DIFFERENCE) / 100) * fish.size:
                    self.eat(fish)

        # time.sleep(0.1)

    def get_score(self):
        return f'Score: {self.score}'

    def eat(self, fish):
        SoundPlayer('./audio/eating_sound.wav', False).play()
        fish.stop()
        self.fishes.pop(find_index_of_fish(self.fishes, fish))
        self.score += (gd.SCORE_PERCENT / 100) * fish.size
        self.fish_eaten += 1
        self.player.size += (gd.SIZE_PERCENT / 100) * fish.size

    def game_over(self):
        # Show end screen
        pygame.event.post(GAME_OVER_EVENT)  # Raises QUIT event (should be changed so it can be
                                                            # distinguished from button interruption)



