import pygame
import random, time
from threading import Thread
from direction import Direction, DirectionChanger
import math
from game_controller import find_index_of_fish
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
        self.pace_maker = 1 / len(self.image_array)  # addition to tracker at the end of each iteration
        self.current_image = self.image_array[0]
        self.rect = self.current_image.get_rect()
        self.rect.left, self.rect.top = location[0], location[1]
        self.alive = True

        randDir = random.randint(-4, 4)  # Direciton values: [-4 , 4]
        while randDir == 0:
            randDir = random.randint(-4, 4)

        self.direction = Direction(randDir)

    def stop(self):
        self.alive = False

    def swim(self):
        if not self.alive:
            return

        # How many times will this function be executed before changing direction
        dirChangeTimer = DirectionChanger(gd.SCREEN_HEIGHT / 10, gd.SCREEN_HEIGHT / 2)
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
        temp = random.randint(-4, 4)
        newValue = self.direction.value + temp

        if newValue > 4:
            newValue = newValue - temp - 4
        elif newValue < -4:
            newValue = newValue - temp + 4

        if newValue < -4 or newValue > 4:
            raise RuntimeError(f'Value of direction can be in range of -4 and 4! '
                               f'Current value: {newValue} ')

        self.direction = Direction(newValue)

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
            self.current_image = self.image_array[self.image_index]
        else:
            self.current_image = self.reverse_image_array[self.image_index]

    def load_images(self, reverse=''):
        temp = []
        i = 0
        try:
            while True:
                temp.append(pygame.image.load(self.image_path + self.image_name + reverse + str(i) + self.image_extension))
                i += 1
        except:
            return temp


# Types of fishes
class BlueFish(NpcSprite):
    def __init__(self, location, id):
        self.movement_speed = 2  # smaller fish -> higher speed -> more pixels change
        self.size = 100
        self.image_path = './img/npcs/'
        self.image_name = 'BlueFish'
        self.image_extension = '.png'
        NpcSprite.__init__(self, location, id)


class FlyingFish(NpcSprite):
    def __init__(self, location, id):
        self.movement_speed = 1.6
        self.size = 100
        self.image_path = './img/npcs/'
        self.image_name = 'FlyingFish'
        self.image_extension = '.png'
        NpcSprite.__init__(self, location, id)


class GreyFish(NpcSprite):
    def __init__(self, location, id):
        self.movement_speed = 1.3
        self.size = 300
        self.image_path = './img/npcs/'
        self.image_name = 'GreyFish'
        self.image_extension = '.png'
        NpcSprite.__init__(self, location, id)


class YellowFish(NpcSprite):
    def __init__(self, location, id):
        self.movement_speed = 1  # not recommended to go below 1 pixel
        self.size = 1500
        self.image_path = './img/npcs/'
        self.image_name = 'YellowFish'
        self.image_extension = '.png'
        NpcSprite.__init__(self, location, id)


class YellowStrapeFish(NpcSprite):
    def __init__(self, location, id):
        self.movement_speed = 1.2
        self.size = 300
        self.image_path = './img/npcs/downloads/'
        self.image_name = 'frame'
        self.image_extension = '.png'
        NpcSprite.__init__(self, location, id)


class Bird(NpcSprite):
    def __init__(self, location, id):
        self.movement_speed = 1.4
        self.size = 300
        self.image_path = './img/npcs/downloads/'
        self.image_name = 'fish'
        self.image_extension = '.png'
        NpcSprite.__init__(self, location, id)


# Fish generator class, spawn fishes in the tank
class FishGenerator:
    def __init__(self, fish_tank_capacity, frequency, list):
        self.id_generator = 0  # Should not be reduced
        self.capacity = fish_tank_capacity
        self.frequency = frequency
        self.work = True
        self.fishes = list  # list of fishes in the tank

    def stop(self):
        self.work = False

    def start(self):
        while self.work:
            if self.capacity == len(self.fishes):
                time.sleep(5)
                # self.fishes[0].alive = False
                # self.fishes.pop(0)
                continue

            rand = random.randint(1, 15)  # top limit depends on number of species

            if rand == 1:
                new_fish = YellowFish(self.get_location(), self.id_generator)
            if 1 < rand <= 3:
                new_fish = YellowStrapeFish(self.get_location(), self.id_generator)
            if 3 < rand <= 5:
                new_fish = GreyFish(self.get_location(), self.id_generator)
            if 5 < rand <= 8:
                new_fish = BlueFish(self.get_location(), self.id_generator)
            if 8 < rand <= 11:
                new_fish = FlyingFish(self.get_location(), self.id_generator)
            if 11 < rand <= 15:
                new_fish = Bird(self.get_location(), self.id_generator)

            self.fishes.append(new_fish)
            self.id_generator += 1

            time.sleep(self.frequency)

    def get_location(self):
        max_iteration = 20
        for i in range(max_iteration):
            a, b = [random.randint(100, gd.SCREEN_WIDTH - 100), random.randint(100, gd.SCREEN_HEIGHT - 100)]
            found = True
            for other in self.fishes:
                x2 = other.rect.centerx
                y2 = other.rect.centery
                if math.sqrt(pow((x2 - a), 2) + pow((y2 - b), 2)) < gd.MIN_DISTANCE / 2:
                    found = False
                    break
            if found:
                return [a, b]


# Prevents fishes to go out of the screen and keeps smaller away from larger fish
class MovementController:
    def __init__(self, list):
        self.fishes = list  # list of fishes in the tank

    def control(self):
        for fish in self.fishes:
            if fish.rect.left < 0:
                # fish.goOpposite()
                fish.changeDirectionTo(Direction.East)
            elif fish.rect.left > gd.SCREEN_WIDTH - 50:  # we dont want them to go off the screen
                fish.changeDirectionTo(Direction.West)
            elif fish.rect.top < 0:
                fish.changeDirectionTo(Direction.South)
            elif fish.rect.top > gd.SCREEN_HEIGHT - 50:
                fish.changeDirectionTo(Direction.North)

            if self.endangered(fish):
                # fish.changeDirection()
                fish.goOpposite()
                fish.move()

    def endangered(self, fish):
        x = fish.rect.centerx
        y = fish.rect.centery
        for other in self.fishes:
            if fish.id == other.id:
                continue

            if fish.size > other.size:
                continue

            x2 = other.rect.centerx
            y2 = other.rect.centery
            if math.sqrt(pow((x2 - x), 2) + pow((y2 - y), 2)) < gd.MIN_DISTANCE:
                if math.sqrt(pow((x2 - x), 2) + pow((y2 - y), 2)) < gd.MIN_DISTANCE / 2:
                    self.fishes.pop(find_index_of_fish(self.fishes, fish))

                return True

        return False