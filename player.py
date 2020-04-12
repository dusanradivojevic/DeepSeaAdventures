import pygame


class Player:
    def __init__(self, image, coordX, coordY, size):
        self.image = image
        self.current_image = pygame.image.load(self.image)
        self.rect = self.current_image.get_rect()
        self.rect.left, self.rect.top = [coordX, coordY]
        self.size = size

    def move(self):
        self.rect.centerx, self.rect.centery = pygame.mouse.get_pos()
