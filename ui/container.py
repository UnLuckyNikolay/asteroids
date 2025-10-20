import pygame, pygame.gfxdraw
from enum import Enum
from typing import Any

from ui.helpers import get_points


class Allignment(Enum):
    NONE = 0
    CENTER = 1

class Container(pygame.sprite.Sprite):
    def __init__(self, 
                 position : tuple[int, int],
                 size : tuple[int, int],
                 corners : tuple[int, int, int, int],
    ):
        self._position = position
        self._size = size
        self._corners = corners
        self._color_outline = (200, 200, 200, 255)
        self._color_fill = (75, 75, 75, 100)
        self._elements : list[tuple[Any, Allignment]] = []

    def draw(self, screen):
        points = get_points(self._position, self._size, self._corners)
        pygame.gfxdraw.filled_polygon(screen, points, self._color_fill)
        pygame.draw.polygon(screen, self._color_outline, points, 3)

        for tuple in self._elements:
            pos = self._get_alligned_position(tuple[1])

            if callable(tuple[0]):
                element = tuple[0]()
                if element == None:
                    continue
            else:
                element = tuple[0]

            element.draw(screen, *pos) # pyright: ignore[reportAttributeAccessIssue]

    def set_fill_color(self, color : tuple[int, int, int, int]):
        self._color_fill = color

    def set_outline_color(self, color : tuple[int, int, int, int]):
        self._color_outline = color

    def set_corners(self, topleft : int, topright : int, bottomright : int, bottomleft : int):
        self._corners = (topleft, topright, bottomright, bottomleft)

    def add_element(self, element, allignment : Allignment = Allignment.NONE):
        self._elements.append((element, allignment))

    def _get_alligned_position(self, allignment : Allignment) -> tuple[int, int]:
        match allignment:
            case Allignment.NONE:
                return self._position
            case Allignment.CENTER:
                return (int(self._position[0] + self._size[0] / 2), int(self._position[1] + self._size[1] / 2))
