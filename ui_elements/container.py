import pygame, pygame.gfxdraw
from enum import Enum
from typing import Any

from ui_elements.text import TextPlain, TextUpdated
from ui_elements.simple_sprite import SimpleSprite
from ui_elements.helpers import get_points


class Allignment(Enum):
    """Use .CENTER or .LEFT_WALL to place text in the middle with minimum nudging."""
    
    UPPER_LEFT_CORNER = 0
    BOTTOM_LEFT_CORNER = 1
    UPPER_RIGHT_CORNER = 2

    LEFT_WALL = 10
    """Places text at the left wall without additional nudging."""

    CENTER = 20
    """Places text in the middle without additional nudging."""
    CENTER_ON_THE_LEFT = 21

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
        self._color_fill = (75, 75, 100, 75)
        
        self._elements : list[tuple[Any, Allignment, tuple[int, int]]] = []
        self._colored_sprites = (TextPlain, TextUpdated, SimpleSprite)

    def draw(self, screen):
        points = get_points(self._position, self._size, self._corners)
        pygame.gfxdraw.filled_polygon(screen, points, self._color_fill)
        pygame.draw.polygon(screen, self._color_outline, points, 3)
        self._draw_elements(screen)

    def _draw_elements(self, screen):
        for tuple in self._elements:

            if callable(tuple[0]):
                element = tuple[0]()
                if element == None:
                    continue    
                pos = self._get_alligned_position(tuple[1], tuple[2])
            elif isinstance(tuple[0], (TextPlain, TextUpdated)):
                size = tuple[0].prepare_and_return_size()
                element = tuple[0]
                pos = self._get_alligned_position(tuple[1], (tuple[2][0]+2, tuple[2][1]+1), text_size=size) # Nudges all text a bit
            else:
                element = tuple[0]
                pos = self._get_alligned_position(tuple[1], tuple[2])

            element.draw(screen, pos) # pyright: ignore[reportAttributeAccessIssue]

    def set_fill_color(self, color : tuple[int, int, int, int]):
        """Default value - blue-ish grey (75, 75, 100, 75)"""
        self._color_fill = color

    def set_outline_color(self, color : tuple[int, int, int, int]):
        """Default value - white (200, 200, 200, 255)."""

        self._color_outline = color
        self._set_element_color(color)

    def _set_element_color(self, color : tuple[int, int, int, int]):
        for tuple in self._elements:
            if isinstance(tuple[0], self._colored_sprites):
                tuple[0].set_color(color)

    def set_corners(self, topleft : int, topright : int, bottomright : int, bottomleft : int):
        self._corners = (topleft, topright, bottomright, bottomleft)

    def add_element(
            self, 
            element, 
            allignment : Allignment = Allignment.UPPER_LEFT_CORNER,
            nudge : tuple[int, int] = (0, 0),
            color_override_and_lock : tuple[int, int, int, int] | None = None
        ):
        if color_override_and_lock != None and isinstance(element, self._colored_sprites):
            element.set_color(color_override_and_lock)
            element.lock_color = True
        self._elements.append((element, allignment, nudge))

    def _get_alligned_position(self, allignment : Allignment, nudge : tuple[int, int] = (0, 0), text_size : tuple[int, int] = (0, 0)) -> tuple[int, int]:
        match allignment:
            case Allignment.UPPER_LEFT_CORNER:
                return (self._position[0] + nudge[0], self._position[1] + nudge[1])
            case Allignment.BOTTOM_LEFT_CORNER:
                return (self._position[0] + nudge[0], self._position[1] + self._size[1] + nudge[1])
            case Allignment.UPPER_RIGHT_CORNER:
                return (self._position[0] + self._size[0] + nudge[0], self._position[1] + nudge[1])
            case Allignment.LEFT_WALL:
                return (self._position[0] + nudge[0], int(self._position[1] + self._size[1]/2 + nudge[1] - text_size[1]/2))
            case Allignment.CENTER:
                return (int(self._position[0] + self._size[0]/2 + nudge[0] - text_size[0]/2), int(self._position[1] + self._size[1]/2 + nudge[1] - text_size[1]/2))
            case Allignment.CENTER_ON_THE_LEFT:
                return (int(self._position[0] + self._size[0] - self._size[1]/2 + nudge[0]), int(self._position[1] + self._size[1]/2 + nudge[1]))

    def _get_divided_color_tuple(self, color : tuple[int, int, int, int], divider : int | float, alpha_override : int | None = None) -> tuple[int, int, int, int]:
        """Returns a new tuple with all color values divided and rounded down. Alpha is not divided but can be overridden."""

        if alpha_override != None:
            return (int(color[0]/divider), int(color[1]/divider), int(color[2]/divider), alpha_override)
        return (int(color[0]/divider), int(color[1]/divider), int(color[2]/divider), color[3])
