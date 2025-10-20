import pygame

class Text(pygame.sprite.Sprite):
    """
    Used to place text inside of buttons/containers without additional formatting.
    """
    def __init__(
        self, 
        text : str, 
        local_pos : tuple[int, int], 
        font : pygame.font.Font, 
        color : tuple[int, int, int, int]
    ):
        self._test = text
        self._position = local_pos
        self._font = font
        self._color = color

        self._surface = self._font.render(self._test, True, self._color)

    def draw(self, screen, position : tuple[int, int], color_override : tuple[int, int, int, int] | None = None):
        if color_override != None:
            surface = self._font.render(self._test, True, color_override)
            screen.blit(surface, (position[0] + self._position[0], position[1] + self._position[1]))
        else:
            screen.blit(self._surface, (position[0] + self._position[0], position[1] + self._position[1]))

    def get_width(self):
        return self._surface.get_width()

class TextF(pygame.sprite.Sprite):
    """
    Used to place text inside of buttons/containers. 
    
    Takes any number of strings and replaces {} with them using .format().
    """
    def __init__(
        self, 
        text : str, 
        local_pos : tuple[int, int], 
        font : pygame.font.Font, 
        color : tuple[int, int, int, int], 
        *formatting_strings
    ):
        self._test = text
        self._position = local_pos
        self._font = font
        self._color = color
        self.strings = formatting_strings

    def draw(self, screen, position : tuple[int, int], color_override : tuple[int, int, int, int] | None = None):
        text = self._test
        text = text.format(*self.strings)
        if color_override == None:
            button_text = self._font.render(text, True, self._color)
        else:
            button_text = self._font.render(text, True, color_override)
        screen.blit(button_text, (position[0] + self._position[0], position[1] + self._position[1]))

class TextH(pygame.sprite.Sprite):
    """
    Used to place text inside of buttons/containers. 

    Takes any number of getter functions and replaces {} with their return values.
    """
    def __init__(
        self, 
        text : str, 
        local_pos : tuple[int, int], 
        font : pygame.font.Font, 
        color : tuple[int, int, int, int], 
        *formatting_getters
    ):
        self._test = text
        self._position = local_pos
        self._font = font
        self._color = color
        self.getters = formatting_getters

    def draw(self, screen, position : tuple[int, int], color_override : tuple[int, int, int, int] | None = None):
        text = self._test
        for getter in self.getters:
            text = text.replace("{}", str(getter()), 1)
        if color_override == None:
            button_text = self._font.render(text, True, self._color)
        else:
            button_text = self._font.render(text, True, color_override)
        screen.blit(button_text, (position[0] + self._position[0], position[1] + self._position[1]))
