import pygame
from direction import Direction
import game_data as gd


class Player:
    def __init__(self, img_path, img_name, img_extension, location, id):
        self.img_path = img_path
        self.img_name = img_name
        self.img_extension = img_extension
        self.image_array = self.load_images(img_path, img_name, img_extension)
        self.reverse_image_array = self.load_images(img_path, img_name, img_extension, 'reverse')
        self.image_index = 0  # tracking index of image in image array (for gifs)
        self.pace_tracker = 0  # for smoother transition of frames
        self.pace_maker = 1 / len(self.image_array)  # addition to tracker at the end of each iteration
        self.current_image = self.image_array[0]
        self.rect = self.current_image.get_rect()
        self.rect.left, self.rect.top = location
        self.size = gd.PLAYER_BASE_SIZE
        self.id = id
        self.direction = Direction.East
        self.earlier_position_x = self.rect.centerx

    # override
    def speed_up(self):
        return

    def swim(self):
        self.move()

    def move(self):
        self.rect.centerx, self.rect.centery = pygame.mouse.get_pos()
        self.check_direction()
        self.pickImage()

    def check_direction(self):
        if self.earlier_position_x - self.rect.centerx < 0:
            self.direction = Direction.East
        elif self.earlier_position_x - self.rect.centerx > 0:
            self.direction = Direction.West
        self.earlier_position_x = self.rect.centerx

    def pickImage(self):
        if self.pace_tracker < 1:
            self.pace_tracker += self.pace_maker
            return
        else:
            self.pace_tracker = 0

        self.image_index += 1
        if self.image_index > len(self.image_array) - 1:
            self.image_index = 0

        if self.direction == Direction.East:
            self.current_image = self.image_array[self.image_index]
        else:
            self.current_image = self.reverse_image_array[self.image_index]

    def load_images(self, img_path, img_name, img_extension, reverse=''):
        temp = []
        i = 0
        try:
            while True:
                temp.append(pygame.image.load(img_path + img_name + reverse + str(i) + img_extension))
                i += 1
        except:
            return temp

    def change_level_image(self, level):
        self.image_index = 0
        self.size = level * gd.PLAYER_BASE_SIZE
        temp = self.img_path[0: len(self.img_path) - 2]
        self.img_path = temp + str(level) + '/'
        self.image_array = self.load_images(self.img_path, self.img_name, self.img_extension)
        self.reverse_image_array = self.load_images(self.img_path, self.img_name, self.img_extension, 'reverse')
        self.current_image = self.image_array[0]
        self.rect = self.current_image.get_rect()