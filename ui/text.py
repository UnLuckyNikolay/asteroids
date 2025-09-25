import pygame

class Text(pygame.sprite.Sprite):
    def __init__(self, text, local_x, local_y, font, color, for_formatting = None):
        self.text = text
        self.x = local_x
        self.y = local_y
        self.font = font
        self.color = color
        self.formatting = for_formatting

    def draw(self, screen, x, y):
        text = self.text.format(self.formatting) if self.formatting != None else self.text
        button_text = self.font.render(text, True, self.color)
        screen.blit(button_text, (x + self.x, y + self.y))
