import pygame


class Player:
    def __init__(self, img_path, img_name, img_extension, location, size, id):
        self.image_array = self.load_images(img_path, img_name, img_extension)
        self.reverse_image_array = self.load_images(img_path, img_name, img_extension, 'Reverse')
        self.image_index = 0  # tracking index of image in image array (for gifs)
        self.pace_tracker = 0  # for smoother transition of frames
        self.pace_maker = 1 / len(self.image_array)  # addition to tracker at the end of each iteration
        self.current_image = self.image_array[0]
        self.rect = self.current_image.get_rect()
        self.rect.left, self.rect.top = location
        self.size = size
        self.id = id

    def swim(self):
        self.move()

    def move(self):
        self.rect.centerx, self.rect.centery = pygame.mouse.get_pos()
        self.pickImage()

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

        # if self.direction.value < 0:
        #     self.current_image = self.image_array[self.image_index]
        # else:
        #     self.current_image = self.reverse_image_array[self.image_index]

    def load_images(self, img_path, img_name, img_extension, reverse=''):
        temp = []
        i = 0
        try:
            while True:
                temp.append(pygame.image.load(img_path + img_name + reverse + str(i) + img_extension))
                i += 1
        except:
            return temp
