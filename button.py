import pygame

screen_center = 400


class Button:
    def __init__(self, position_x, position_y, font, text_color, text):
        self.width, self.height = pygame.font.Font.size(font, text)
        self.position_x = (screen_center - (self.width / 2))
        self.position_y = position_y
        self.font = font
        self.text_color = text_color
        self.text = text

    def get_button(self):
        button_surface = self.font.render(self.text, False, self.text_color)
        return button_surface

    def get_position(self):
        return self.position_x, self.position_y

    def collision(self, mouse_position):
        x, y = mouse_position

        if self.position_x <= x <= self.position_x + self.width:
            if self.position_y <= y <= self.position_y + self.height:
                return True

        return False