import pygame, pygame.gfxdraw
from typing import Callable, Any

from ui.container import Container, Allignment
from ui.text import Text
from ui.simple_sprite import SimpleSprite
from ui.helpers import get_points

class Button(Container):
    def __init__(self,
                 position, 
                 size, 
                 corners : tuple[int, int, int, int],
                 key_func : Callable, 
                 condition_func : Callable = lambda: True,
    ):
        super().__init__(
            position, 
            size,
            corners,
        )
        self._color_outline = (100, 200, 255, 255)
        self._color_outline_inactive = (100, 100, 100, 255)
        self._key_func = key_func
        self._condition_func = condition_func

    def draw(self, screen):
        points = get_points(self._position, self._size, self._corners)
        pygame.gfxdraw.filled_polygon(screen, points, self._color_fill)
        if self._condition_func():
            pygame.draw.polygon(screen, self._color_outline, points, 3)
        else:
            pygame.draw.polygon(screen, self._color_outline_inactive, points, 3)

        for tuple in self._elements:
            pos = self._get_alligned_position(tuple[1])

            if callable(tuple[0]):
                element = tuple[0]()
                if element == None:
                    continue
            else:
                element = tuple[0]

            if (isinstance(element, Text) or isinstance(element, SimpleSprite)) and not self._condition_func():
                element.draw(screen, *pos, self._color_outline_inactive) # pyright: ignore[reportAttributeAccessIssue]
            else:
                element.draw(screen, *pos) # pyright: ignore[reportAttributeAccessIssue]
    
    def check_click(self, position):
        if (position[0] > self._position[0] and
            position[0] < self._position[0] + self._size[0] and
            position[1] > self._position[1] and
            position[1] < self._position[1] + self._size[1]):
            return True
        else:
            return False

    def run_if_possible(self) -> bool:
        if self._condition_func():
            self._key_func()
            return True
        return False

    def set_inactive_outline_color(self, color : tuple[int, int, int, int]):
        """Default value - dark grey (100, 100, 100, 255)"""
        self._color_outline_inactive = color
