import pygame, pygame.gfxdraw
from typing import Callable, Any

from ui.container import Container, Allignment
from ui.text import Text
from ui.simple_sprite import SimpleSprite
from ui.helpers import get_points

class Switch(Container):
    def __init__(self,
                 position, 
                 size, 
                 corners : tuple[int, int, int, int],
                 key_func : Callable, 
                 is_active : bool,
    ):
        super().__init__(
            position, 
            size,
            corners,
        )
        self._color_outline = (100, 200, 255, 255)
        self._color_outline_active = (0, 255, 0, 255)
        self._color_fill_hover_inactive = self._get_divided_color_tuple(self._color_outline, 2, 150)
        self._color_fill_hover_active = self._get_divided_color_tuple(self._color_outline_active, 2, 150)
        self._is_hovered = False
        
        self._key_func = key_func
        self._is_active = is_active

    def draw(self, screen):
        points = get_points(self._position, self._size, self._corners)
        if self._is_hovered and self._is_active:
            pygame.gfxdraw.filled_polygon(screen, points, self._color_fill_hover_active)
        if self._is_hovered and not self._is_active:
            pygame.gfxdraw.filled_polygon(screen, points, self._color_fill_hover_inactive)
        else:
            pygame.gfxdraw.filled_polygon(screen, points, self._color_fill)
        if self._is_active:
            pygame.draw.polygon(screen, self._color_outline_active, points, 3)
        else:
            pygame.draw.polygon(screen, self._color_outline, points, 3)

        for tuple in self._elements:
            pos = self._get_alligned_position(tuple[1])

            if callable(tuple[0]):
                element = tuple[0]()
                if element == None:
                    continue
            else:
                element = tuple[0]

            if (isinstance(element, Text) or isinstance(element, SimpleSprite)) and self._is_active:
                element.draw(screen, *pos, self._color_outline_active) # pyright: ignore[reportAttributeAccessIssue]
            else:
                element.draw(screen, *pos) # pyright: ignore[reportAttributeAccessIssue]
    
    def set_outline_color(self, color : tuple[int, int, int, int]):
        """Default value - blue (100, 200, 255, 255)."""
        
        self._color_outline = color
        self._color_fill_hover_inactive = self._get_divided_color_tuple(self._color_outline, 2, 150)

    def set_active_outline_color(self, color : tuple[int, int, int, int]):
        """Default value - green (0, 255, 0, 255)."""

        self._color_outline_active = color
        self._color_fill_hover_active = self._get_divided_color_tuple(self._color_outline_active, 2, 150)

    def switch_hovered_state(self):
        self._is_hovered = False if self._is_hovered else True

    def check_cursor_hover(self, position):
        if (position[0] > self._position[0] and
            position[0] < self._position[0] + self._size[0] and
            position[1] > self._position[1] and
            position[1] < self._position[1] + self._size[1]):
            return True
        else:
            return False

    def run_if_possible(self) -> bool:
        self._key_func()
        self._is_active = False if self._is_active else True            
        return True

