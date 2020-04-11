import pygame


class Player:
    def __init__(self, image, coordX, coordY, size):
        self.image = image
        self.current_image = pygame.image.load(self.image)
        self.rect = self.current_image.get_rect()
        self.rect.left, self.rect.top = [coordX, coordY]
        self.size = size
        self.active = True

    def stop(self):
        self.active = False

    def move(self, mouse_position):
        self.rect.centerx, self.rect.centery = mouse_position

    def start(self):
        pygame.mouse.set_visible(False)
        while self.active:
            self.move(pygame.mouse.get_pos())
