import pygame
import random, time
import threading
from direction import Direction, DirectionChanger
import math
import game_data as gd


# Non Player Character
class NpcSprite(pygame.sprite.Sprite):
    def __init__(self, location, id):
        self.id = id
        pygame.sprite.Sprite.__init__(self)
        self.image_array = self.load_images()
        self.reverse_image_array = self.load_images('Reverse')
        self.image_index = 0  # tracking index of image in image array (for gifs)
        self.pace_tracker = 0  # for smoother transition of frames
        self.pace_maker = 1 / len(self.image_array) * 2  # (speed of animation) greater the value greater the speed
        self.current_image = self.image_array[0]
        self.rect = self.current_image.get_rect()
        self.rect.left, self.rect.top = location[0], location[1]
        self.direction = self.get_direction()
        self.alive = True
        self.endangered = False

        if location == (-1, -1):
            self.rect.left, self.rect.top = self.set_location()

    def change_endangered_status(self):
        self.endangered = not self.endangered

    def set_location(self):
        y = random.randint(self.current_image.get_rect().size[1] / 2,
                           gd.SCREEN_HEIGHT - self.current_image.get_rect().size[1] / 2)

        if self.direction == Direction.West:
            x = gd.SCREEN_WIDTH + self.current_image.get_rect().size[0]
        else:
            x = -1 * self.current_image.get_rect().size[0]

        return x, y

    def get_location(self):
        y = self.rect.top + self.current_image.get_rect().size[1]

        if self.direction == Direction.West:
            x = self.rect.left - self.current_image.get_rect().size[0]
        else:
            x = self.rect.left + self.current_image.get_rect().size[0]

        return x, y

    def get_direction(self):
        randDir = random.randint(-4, 4)  # Direction values: [-4 , 4]
        while randDir == 0:
            randDir = random.randint(-4, 4)
        return Direction(randDir)

    def stop(self):
        self.alive = False

    def swim(self):
        if not self.alive:
            return

        # How many times will this function be executed before changing direction
        dirChangeTimer = DirectionChanger(round(gd.SCREEN_HEIGHT / 10), round(gd.SCREEN_HEIGHT / 2))
        self.move()

        if dirChangeTimer.value >= dirChangeTimer.max_value:
            dirChangeTimer.resetChanger()
            self.changeDirection()
        else:
            dirChangeTimer.value += self.movement_speed

            # time.sleep(1 / self.speed)

    def move(self):
        if self.direction == Direction.Default:
            self.changeDirection()
            return
        if self.direction == Direction.North:
            self.rect.top -= self.movement_speed
        if self.direction == Direction.NorthEast:
            self.rect.top -= self.movement_speed
            self.rect.left += self.movement_speed
        if self.direction == Direction.East:
            self.rect.left += self.movement_speed
        if self.direction == Direction.SouthEast:
            self.rect.top += self.movement_speed
            self.rect.left += self.movement_speed
        if self.direction == Direction.South:
            self.rect.top += self.movement_speed
        if self.direction == Direction.SouthWest:
            self.rect.top += self.movement_speed
            self.rect.left -= self.movement_speed
        if self.direction == Direction.West:
            self.rect.left -= self.movement_speed
        if self.direction == Direction.NorthWest:
            self.rect.top -= self.movement_speed
            self.rect.left -= self.movement_speed

        self.pickImage()  # Movement_controller also calls upon move() method !

    def goOpposite(self):
        self.direction = Direction(self.direction.value * -1)

    def changeDirectionTo(self, dir):
        self.direction = dir

    def changeDirection(self):
        # temp = random.randint(-4, 4)
        # newValue = self.direction.value + temp
        #
        # if newValue > 4:
        #     newValue = newValue - temp - 4
        # elif newValue < -4:
        #     newValue = newValue - temp + 4
        #
        # if newValue < -4 or newValue > 4:
        #     raise RuntimeError(f'Value of direction can be in range of -4 and 4! '
        #                        f'Current value: {newValue} ')
        #
        # self.direction = Direction(newValue)

        temp = random.randint(-4, 4)
        while temp == 0 or temp == self.direction.value:
            temp = random.randint(-4, 4)

        self.direction = Direction(temp)

    def pickImage(self):
        if self.pace_tracker < 1:
            self.pace_tracker += self.pace_maker
            return
        else:
            self.pace_tracker = 0

        self.image_index += 1
        if self.image_index > len(self.image_array) - 1:
            self.image_index = 0

        if self.direction.value < 0:
            self.current_image = self.reverse_image_array[self.image_index]
        else:
            self.current_image = self.image_array[self.image_index]

    def load_images(self, reverse=''):
        temp = []
        i = 0
        try:
            while True:
                temp.append(pygame.image.load(self.image_path + self.image_name + reverse + str(i) + self.image_extension))
                i += 1
        except:
            return temp

    def speed_up(self):
        self.movement_speed *= gd.SPEED_COEF / 100 + 1  # speed * 1.1


# Danger Fishes
class BullShark(NpcSprite):
    def __init__(self, location, id):
        self.levels = [1, 2, 3, 4, 5]
        self.movement_speed = 35
        self.size = gd.DANGER_FISH_SIZE    # danger fish characteristic (important in main.py)
        self.image_path = './img/npcs/'
        self.image_name = 'bull-shark'
        self.image_extension = '.png'
        self.gone_out_of_the_screen = False
        NpcSprite.__init__(self, (-1, -1), id)

    # overrides
    def get_direction(self):
        randDir = random.randint(-1, 1) * 3  # Direciton values: -3, 3 (west or east)
        while randDir == 0:
            randDir = random.randint(-1, 1) * 3
        return Direction(randDir)

    def changeDirection(self):
        return

    def changeDirectionTo(self, dir):
        return

    def goOpposite(self):
        return

    def swim(self):
        if not self.alive:
            return

        if self.rect.left < 3 * -1 * self.current_image.get_rect().size[0] or \
            self.rect.left > 3 * self.current_image.get_rect().size[0]:
            self.gone_out_of_the_screen = True

        self.move()


# Types of fishes
class BlueFish(NpcSprite):
    def __init__(self, location, id):
        self.levels = [1]
        self.movement_speed = 3  # smaller fish -> higher speed -> more pixels change
        self.size = 100
        self.image_path = './img/npcs/'
        self.image_name = 'BlueFish'
        self.image_extension = '.png'
        NpcSprite.__init__(self, location, id)


class FlyingFish(NpcSprite):
    def __init__(self, location, id):
        self.levels = [1, 2]
        self.movement_speed = 2.6
        self.size = 100
        self.image_path = './img/npcs/'
        self.image_name = 'FlyingFish'
        self.image_extension = '.png'
        NpcSprite.__init__(self, location, id)


class GreyFish(NpcSprite):
    def __init__(self, location, id):
        self.levels = [1, 2, 3, 4]
        self.movement_speed = 2
        self.size = 300
        self.image_path = './img/npcs/'
        self.image_name = 'GreyFish'
        self.image_extension = '.png'
        NpcSprite.__init__(self, location, id)


class YellowFish(NpcSprite):
    def __init__(self, location, id):
        self.levels = [1, 2, 3, 4, 5]
        self.movement_speed = 1.5  # not recommended to go below 1 pixel
        self.size = 1500
        self.image_path = './img/npcs/'
        self.image_name = 'YellowFish'
        self.image_extension = '.png'
        NpcSprite.__init__(self, location, id)


class YellowStrapeFish(NpcSprite):
    def __init__(self, location, id):
        self.levels = [1, 2, 3]
        self.movement_speed = 2.2
        self.size = 300
        self.image_path = './img/npcs/downloads/'
        self.image_name = 'frame'
        self.image_extension = '.png'
        NpcSprite.__init__(self, location, id)


class Bird(NpcSprite):
    def __init__(self, location, id):
        self.levels = [1, 2, 3, 4]
        self.movement_speed = 2.4
        self.size = 300
        self.image_path = './img/npcs/downloads/'
        self.image_name = 'fish'
        self.image_extension = '.png'
        NpcSprite.__init__(self, location, id)
