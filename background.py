import pygame
import game_data as gd


class Background:
    def __init__(self, image_file, location):
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        # self.rect.left, self.rect.top = location
        self.rect.left, self.rect.top = [0.5 * gd.SCREEN_WIDTH - 0.5 * self.image.get_width(),
                                       0.5 * gd.SCREEN_HEIGHT - 0.5 * self.image.get_height()]  # centering background


class GifBackground:
    def __init__(self, img_path, img_name, img_extension, location):
        self.image_array = self.load_images(img_path, img_name, img_extension)
        self.current_image = self.image_array[0]
        self.image_index = 0  # tracking index of image in image array
        self.pace_tracker = 0  # for smoother transition of frames
        self.pace_maker = 1 / len(self.image_array)  # addition to tracker at the end of each iteration
        self.rect = self.current_image.get_rect()
        self.rect.left, self.rect.top = location

    def pickImage(self):
        if self.pace_tracker < 1:
            self.pace_tracker += self.pace_maker
            return
        else:
            self.pace_tracker = 0

        self.image_index += 1
        if self.image_index > len(self.image_array) - 1:
            self.image_index = 0

        self.current_image = self.image_array[self.image_index]

    def load_images(self, img_path, img_name, img_extension):
        temp = []
        i = 0
        try:
            while True:
                temp.append(pygame.image.load(img_path + img_name + str(i) + img_extension))
                i += 1
        except:
            return temp