import pygame

class Text(pygame.sprite.Sprite):
    def __init__(self, text, local_x, local_y, font, color, *formatting_handlers):
        self.text = text
        self.x = local_x
        self.y = local_y
        self.font = font
        self.color = color
        self.handlers = formatting_handlers

    def draw(self, screen, x, y):
        text = self.text
        for handler in self.handlers:
            text = text.format(handler())
        button_text = self.font.render(text, True, self.color)
        screen.blit(button_text, (x + self.x, y + self.y))
