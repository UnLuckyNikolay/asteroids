import pygame

class Text(pygame.sprite.Sprite):
    """
    Used to place text inside of buttons/containers without additional formatting.
    """
    def __init__(self, text, local_x, local_y, font, color):
        self.text = text
        self.x = local_x
        self.y = local_y
        self.font = font
        self.color = color

    def draw(self, screen, x, y, color_override=None):
        if color_override == None:
            button_text = self.font.render(self.text, True, self.color)
        else:
            button_text = self.font.render(self.text, True, color_override)
        screen.blit(button_text, (x + self.x, y + self.y))

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

    def draw(self, screen, x, y, color_override=None):
        text = self.text
        text = text.format(*self.strings)
        if color_override == None:
            button_text = self.font.render(text, True, self.color)
        else:
            button_text = self.font.render(text, True, color_override)
        screen.blit(button_text, (x + self.x, y + self.y))

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

    def draw(self, screen, x, y, color_override=None):
        text = self.text
        for getter in self.getters:
            text = text.replace("{}", str(getter()), 1)
        if color_override == None:
            button_text = self.font.render(text, True, self.color)
        else:
            button_text = self.font.render(text, True, color_override)
        screen.blit(button_text, (x + self.x, y + self.y))
