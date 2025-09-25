import pygame

class TextH(pygame.sprite.Sprite):
    """
    Used to place text inside of buttons/containers. 

    Takes any number of getter functions and replaces {} with their return values.
    """
    def __init__(self, text, local_x, local_y, font, color, *formatting_getters):
        self.text = text
        self.x = local_x
        self.y = local_y
        self.font = font
        self.color = color
        self.getters = formatting_getters

    def draw(self, screen, x, y):
        text = self.text
        for getter in self.getters:
            text = text.replace("{}", str(getter()), 1)
        button_text = self.font.render(text, True, self.color)
        screen.blit(button_text, (x + self.x, y + self.y))
