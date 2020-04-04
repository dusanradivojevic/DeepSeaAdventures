import pygame
import random, time
from threading import Thread
from direction import Direction, DirectionChanger
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# Non Player Character
class NpcSprite(pygame.sprite.Sprite):
    def __init__(self, image, reverse_image, speed, id):
        self.id = id
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.reverse_image = reverse_image
        self.current_image = pygame.image.load(self.image)
        self.rect = self.current_image.get_rect()
        self.rect.left, self.rect.top = [random.randint(100, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT - 100)]
        self.speed = speed
        self.alive = True

        randDir = random.randint(-4, 4)  # Direciton values: [-4 , 4]
        while randDir == 0:
            randDir = random.randint(-4, 4)

        self.direction = Direction(randDir)

    def swimming(self):
        dirChangeTimer = DirectionChanger(SCREEN_HEIGHT / 10, SCREEN_HEIGHT / 2)
        while self.alive:
            self.move()

            if dirChangeTimer.value >= dirChangeTimer.max_value:
                dirChangeTimer.resetChanger()
                self.changeDirection()
            else:
                dirChangeTimer.value += 1

            time.sleep(1 / self.speed)

    def move(self):
        if self.direction == Direction.Default:
            self.changeDirection()
            return
        if self.direction == Direction.North:
            self.rect.top -= 1
        if self.direction == Direction.NorthEast:
            self.rect.top -= 1
            self.rect.left += 1
        if self.direction == Direction.East:
            self.rect.left += 1
        if self.direction == Direction.SouthEast:
            self.rect.top += 1
            self.rect.left += 1
        if self.direction == Direction.South:
            self.rect.top += 1
        if self.direction == Direction.SouthWest:
            self.rect.top += 1
            self.rect.left -= 1
        if self.direction == Direction.West:
            self.rect.left -= 1
        if self.direction == Direction.NorthWest:
            self.rect.top -= 1
            self.rect.left -= 1

    def goOpposite(self):
        self.direction = Direction(self.direction.value * -1)

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


# Types of fishes
class BlueFish(NpcSprite):
    def __init__(self, id):
        self.speed = 120  # smaller fish -> higher speed -> more frequent in generator
        self.size_index = 5  # larger fish -> smaller index
        self.image = './img/npcs/BlueFish.png'
        self.image_reverse = './img/npcs/BlueFishReverse.png'
        NpcSprite.__init__(self, self.image, self.image_reverse, self.speed, id)


class FlyingFish(NpcSprite):
    def __init__(self, id):
        self.speed = 160
        self.size_index = 5
        self.image = './img/npcs/FlyingFish.png'
        self.image_reverse = './img/npcs/FlyingFishReverse.png'
        NpcSprite.__init__(self, self.image, self.image_reverse, self.speed, id)


class GreyFish(NpcSprite):
    def __init__(self, id):
        self.speed = 60
        self.size_index = 3
        self.image = './img/npcs/GreyFish.png'
        self.image_reverse = './img/npcs/GreyFishReverse.png'
        NpcSprite.__init__(self, self.image, self.image_reverse, self.speed, id)


class YellowFish(NpcSprite):
    def __init__(self, id):
        self.speed = 20
        self.size_index = 1
        self.image = './img/npcs/YellowFish.png'
        self.image_reverse = './img/npcs/YellowFishReverse.png'
        NpcSprite.__init__(self, self.image, self.image_reverse, self.speed, id)


class YellowStrapeFish(NpcSprite):
    def __init__(self, id):
        self.speed = 50
        self.size_index = 3
        self.image = './img/npcs/YellowStrapeFish.png'
        self.image_reverse = './img/npcs/YellowStrapeFishReverse.png'
        NpcSprite.__init__(self, self.image, self.image_reverse, self.speed, id)


# Fish generator class
class FishGenerator:
    def __init__(self, fish_tank_capacity, frequency, list):
        self.id_generator = 0
        self.capacity = fish_tank_capacity
        self.frequency = frequency
        self.work = True
        self.fishes = list  # list of fishes in the tank

    def start(self):
        while self.work:
            if self.capacity == len(self.fishes):
                # time.sleep(10)
                # self.fishes[0].alive = False
                # self.fishes.pop(0)
                continue

            rand = random.randint(1, 10)  # top limit depends on number of species

            if rand == 1:
                newFish = YellowFish(self.id_generator)
            if rand > 1 and rand <= 2:
                newFish = YellowStrapeFish(self.id_generator)
            if rand > 2 and rand <= 4:
                newFish = GreyFish(self.id_generator)
            if rand > 4 and rand <= 7:
                newFish = BlueFish(self.id_generator)
            if rand > 7 and rand <= 10:
                newFish = FlyingFish(self.id_generator)

            self.fishes.append(newFish)
            self.id_generator += 1

            thread = Thread(target=newFish.swimming)
            thread.start()

            time.sleep(self.frequency)


# Prevents fishes to go out of the screen and keeps smaller away from larger fish
class MovementController:
    def __init__(self, list):
        self.min_distance = 50  # pixels
        self.work = True
        self.fishes = list  # list of fishes in the tank

    def start_control(self):
        while self.work:
            for fish in self.fishes:
                if fish.rect.left < 0:
                    fish.goOpposite()
                elif fish.rect.left > SCREEN_WIDTH - 50:  # we dont want them to go off the screen
                    fish.goOpposite()
                elif fish.rect.top < 0:
                    fish.goOpposite()
                elif fish.rect.top > SCREEN_HEIGHT - 50:
                    fish.goOpposite()

                while self.endangered(fish):
                    fish.changeDirection()
                    fish.move()

            time.sleep(0.5)  # fishes need to have time to move

    def endangered(self, fish):
        x = fish.rect.centerx
        y = fish.rect.centery
        for other in self.fishes:
            if fish.id == other.id:
                continue

            if fish.size_index < other.size_index:
                continue

            x2 = other.rect.centerx
            y2 = other.rect.centery
            if math.sqrt(pow((x2 - x), 2) + pow((y2 - y), 2)) < self.min_distance:
                return True

        return False