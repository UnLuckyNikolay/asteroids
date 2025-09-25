import pygame

class TextF(pygame.sprite.Sprite):
    """
    Used to place text inside of buttons/containers. 
    
    Takes any number of strings and replaces {} with them using .format().
    """
    def __init__(self, text, local_x, local_y, font, color, *formatting_strings):
        self.text = text
        self.x = local_x
        self.y = local_y
        self.font = font
        self.color = color
        self.strings = formatting_strings

    def draw(self, screen, x, y):
        text = self.text
        text = text.format(*self.strings)
        button_text = self.font.render(text, True, self.color)
        screen.blit(button_text, (x + self.x, y + self.y))
