import pygame
from typing import Callable

class TextPlain(pygame.sprite.Sprite):
    """
    Used to place text inside of buttons/containers.
    
    Takes any number of strings and replaces {} with them using .format(). Gets all text during initialization.
    """
    def __init__(
        self, 
        text : str, 
        font : pygame.font.Font, 
        color : tuple[int, int, int, int], 
        *formatting_strings,
        local_pos : tuple[int, int] = (0, 0), 
    ):
        if len(formatting_strings) > 0:
            self._text = text.format(*formatting_strings)
        else:
            self._text = text
        self._position = local_pos
        self._font = font
        self._color = color
        self.lock_color : bool = False

        self._surface = self._font.render(self._text, True, self._color)

    def set_color(self, color : tuple[int, int, int, int]):
        if not self.lock_color:
            self._color = color
            self._surface = self._font.render(self._text, True, self._color)

    def prepare_and_return_size(self):
        return self._surface.get_size()
    
    def get_width(self):
        # Used for button descriptions
        return self._surface.get_width()

    def draw(self, screen, position : tuple[int, int]):
        screen.blit(self._surface, (position[0] + self._position[0], position[1] + self._position[1]))

class TextUpdated(pygame.sprite.Sprite):
    """
    Used to place text inside of buttons/containers.

    Takes any number of getter functions and replaces {} with their return values. Updated before each .draw.
    """
    def __init__(
        self, 
        text : str, 
        font : pygame.font.Font, 
        color : tuple[int, int, int, int], 
        *formatting_getters : Callable,
        local_pos : tuple[int, int] = (0, 0),
    ):
        self._text = text
        self._position = local_pos
        self._font = font
        self._color = color
        self.lock_color : bool = False
        self._getters = formatting_getters

    def set_color(self, color : tuple[int, int, int, int]):
        if not self.lock_color:
            self._color = color

    def prepare_and_return_size(self):
        text = self._text
        for getter in self._getters:
            text = text.replace("{}", str(getter()), 1)
        self._surface = self._font.render(text, True, self._color)
        return self._surface.get_size()

    def draw(self, screen, position : tuple[int, int]):
        screen.blit(self._surface, (position[0] + self._position[0], position[1] + self._position[1]))
