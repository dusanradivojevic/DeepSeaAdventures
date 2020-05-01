import time
import math
import pygame
from sounds import SoundPlayer
import game_data as gd
import threading
import level_data as levels
import npc


# Changes time lapsed from number of seconds to hours : minutes : seconds format
def time_convert(seconds):
    min = (seconds // 60) % 60
    sec = seconds % 60
    hours = min // 60
    return f'{hours} : {min} : {round(sec,2)}'


# Checks whether given array of fish types contains type the same as asked
def has_type(array, given_type):
    if len(array) == 0:
        return False

    if array[0] == npc.NpcSprite:
        return True

    for tp in array:
        if tp == given_type:
            return True
    return False


class TaskController:
    def __init__(self, task):
        self.task = task
        self.fishes = []
        self.score = 0

    def task_update(self, eaten_fish, score):
        if self.task.score_needed != 0:
            self.score += score

        if has_type(self.task.fish_types, type(eaten_fish)):
            self.fishes.append(eaten_fish)

    def get_text_surface(self, font):
        rows = [
            font.render('Tasks:', False, gd.white_color)
        ]

        if self.task.score_needed != 0:
            sc = self.score if self.score < self.task.score_needed else self.task.score_needed
            text = f'{round(sc)}/{self.task.score_needed}' \
                   f' Score'
            rows.append(font.render(text, False, gd.white_color))  # 0/500 Score

        index = 0
        for tp in self.task.fish_types:
            num = self.number_of_eaten_fish_of_type(tp) if self.number_of_eaten_fish_of_type(tp) < \
                self.task.fish_numbers[index] else self.task.fish_numbers[index]
            text = f'{num}/{self.task.fish_numbers[index]}' \
                   f' {levels.get_name_of_type(tp)}'
            rows.append(font.render(text, False, gd.white_color))  # 0/5 BlueFish
            index += 1

        return rows

    def number_of_eaten_fish_of_type(self, tp):
        if tp == npc.NpcSprite:
            return len(self.fishes)

        count = 0
        for fish in self.fishes:
            if type(fish) == tp:
                count += 1
        return count

    def is_completed(self):
        if self.score < self.task.score_needed:
            return False

        # for each type of fish needed checks how much of them player has eaten
        checking_fish_index = 0
        for tp in self.task.fish_types:
            count = self.number_of_eaten_fish_of_type(tp)

            if count < self.task.fish_numbers[checking_fish_index]:
                return False

            checking_fish_index += 1  # next number of eaten fish needed

        return True


class GameController:
    def __init__(self, list, player, generator):
        self.level = 1
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
        self.task_controller = TaskController(levels.get_random_task(self.level))

    def change_level(self):
        if self.task_controller.is_completed():
            self.level += 1
            if self.level > gd.NUM_OF_LEVELS:
                pygame.event.post(gd.GAME_WIN_EVENT)
                return
            self.generator.change_level()
            self.task_controller = TaskController(levels.get_random_task(self.level))
            self.player.change_level_image(self.level)
            pygame.event.post(gd.LEVEL_CHANGED_EVENT)

    def stop(self):
        self.work = False
        self.end_time = time.time()
        time_lapsed = self.end_time - self.start_time
        self.played_time = time_convert(time_lapsed)

    def start(self):
        # x = self.player.rect.centerx
        # y = self.player.rect.centery
        for fish in self.fishes:
            # x2 = fish.rect.centerx
            # y2 = fish.rect.centery
            #
            # min_horizontal_distance = fish.rect.width / 2 + \
            #                           self.player.rect.width / 2 + gd.MIN_DISTANCE
            # min_vertical_distance = fish.rect.height / 2 + \
            #                        self.player.rect.height / 2 + gd.MIN_DISTANCE

            # if abs(x2 - x) < min_horizontal_distance / 2 and abs(y2 - y) < min_vertical_distance / 2:
            #     if self.player.size < ((100 - gd.FISH_SIZE_DIFFERENCE) / 100) * fish.size:
            #         self.game_over()
            #     elif self.player.size > ((100 + gd.FISH_SIZE_DIFFERENCE) / 100) * fish.size:
            #         self.eat(fish)

            if self.player.size < ((100 - gd.FISH_SIZE_DIFFERENCE) / 100) * fish.size \
                    and fish.rect.left < self.player.rect.centerx < fish.rect.right\
                    and fish.rect.top + 0.2 * fish.rect.height < self.player.rect.centery < \
                    fish.rect.bottom - 0.2 * fish.rect.height:
                self.game_over()
            elif self.player.size > ((100 + gd.FISH_SIZE_DIFFERENCE) / 100) * fish.size\
                    and self.player.rect.left < fish.rect.centerx < self.player.rect.right\
                    and self.player.rect.top + 0.2 * self.player.rect.height < fish.rect.centery < \
                    self.player.rect.bottom - 0.2 * self.player.rect.height:
                self.eat(fish)

    def call_danger_fish(self):
        if not self.work:
            return

        if round(time.time() - self.start_time) != 0:
            self.generator.spawn_danger_fish()

        threading.Timer(gd.DANGER_FISH_SPAWN_FREQUENCY, self.call_danger_fish).start()

    def get_score(self):
        return f'Score: {round(self.score)}'

    def get_level(self):
        return f'Level: {self.level}'

    def get_text_surface(self, font):
        return self.task_controller.get_text_surface(font)

    def eat(self, fish):
        SoundPlayer(gd.eating_sound_path, False).play()
        fish.stop()
        score_amount = (gd.SCORE_PERCENT / 100) * fish.size
        self.score += score_amount
        self.fish_eaten.append(fish)
        self.task_controller.task_update(fish, score_amount)
        self.change_level()
        # self.player.size += (gd.SIZE_PERCENT / 100) * fish.size

    def game_over(self):
        # Show end screen
        pygame.event.post(gd.GAME_OVER_EVENT)  # Raises QUIT event (should be changed so it can be
                                                            # distinguished from button interruption)



