import pygame, pygame.gfxdraw
from enum import Enum
from typing import Any, Callable

from ui.elements.text import TextPlain, TextUpdated
from ui.elements.simple_sprite import SimpleSprite
from ui.helpers import get_points


class Allignment(Enum):
    """Use .CENTER or .LEFT_WALL to place text in the middle with minimum nudging."""
    
    UPPER_LEFT_CORNER = 0
    BOTTOM_LEFT_CORNER = 1
    UPPER_RIGHT_CORNER = 2

    LEFT_WALL = 10
    """Places text at the left wall without additional nudging."""
    RIGHT_WALL = 11
    """Places text at the right wall without additional nudging."""
    UPPER_WALL = 12
    """Places text at the upper wall without additional nudging."""

    CENTER = 20
    """Places text in the middle without additional nudging."""
    CENTER_ON_THE_LEFT = 21

class Container(pygame.sprite.Sprite):
    padding = 50

    def __init__(self, 
                 position : tuple[int, int],
                 size : tuple[int, int],
                 corners : tuple[int, int, int, int],
    ):
        if hasattr(self, "containers"):
            super().__init__(self.containers) # pyright: ignore[reportAttributeAccessIssue]
        else:
            super().__init__()
            
        self._position = position
        self._size = size
        self._corners = corners

        self._conditional_overrides : list[tuple[Callable, Callable]] = []

        self._color_outline = (200, 200, 200, 255)
        self._color_fill = (75, 75, 100, 75)
        
        self._elements : list[tuple[Any, Allignment, tuple[int, int]]] = []
        self._colored_sprites = (TextPlain, TextUpdated, SimpleSprite)

    def update(self, dt : float):
        for cd, ovr in self._conditional_overrides:
            if cd():
                ovr()

    def add_conditional_override(self, condition : Callable[[], bool], override : Callable):
        self._conditional_overrides.append((condition, override))

    def draw(self, screen : pygame.Surface):
        self._draw_box(screen, self._color_fill, self._color_outline)

    def _draw_box(self, screen : pygame.Surface, fill_color, outline_color):
        bg_points = get_points(self._position, self._size, self._corners)
        pygame.gfxdraw.filled_polygon(screen, bg_points, fill_color) 
        # Background is applied dirrectly to the screen bcs of how annoying working with alpha is
        # The rest is separate to be able to do effects like shine

        points = get_points((self.padding, self.padding), self._size, self._corners)
        sprite = pygame.Surface((self._size[0]+self.padding*2, self._size[1]+self.padding*2), pygame.SRCALPHA)
        # pygame.gfxdraw.filled_polygon(mask, points, fill_color) 
        # mask.set_colorkey((0, 0, 0))
        
        pygame.draw.polygon(sprite, outline_color, points, 3)
        self._draw_elements(sprite)

        screen.blit(sprite, (self._position[0]-self.padding, self._position[1]-self.padding))

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

    def set_color(self, color : tuple[int, int, int, int]):
        """Sets both outline and fill."""

        self.set_outline_color(color)
        self.set_fill_color(self._get_divided_color_tuple(color, 3, 75))

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
                return (self.padding + nudge[0], self.padding + nudge[1])
            case Allignment.BOTTOM_LEFT_CORNER:
                return (self.padding + nudge[0], self.padding + self._size[1] + nudge[1])
            case Allignment.UPPER_RIGHT_CORNER:
                return (self.padding + self._size[0] + nudge[0], self.padding + nudge[1])
            case Allignment.LEFT_WALL:
                return (self.padding + nudge[0], int(self.padding + self._size[1]/2 + nudge[1] - text_size[1]/2))
            case Allignment.RIGHT_WALL:
                return (self.padding + self._size[0] - text_size[0] + nudge[0], int(self.padding + self._size[1]/2 + nudge[1] - text_size[1]/2))
            case Allignment.UPPER_WALL:
                return (int(self.padding + self._size[0]/2 + nudge[0] - text_size[0]/2), self.padding + nudge[1])
            case Allignment.CENTER:
                return (int(self.padding + self._size[0]/2 + nudge[0] - text_size[0]/2), int(self.padding + self._size[1]/2 + nudge[1] - text_size[1]/2))
            case Allignment.CENTER_ON_THE_LEFT:
                return (int(self.padding + self._size[0] - self._size[1]/2 + nudge[0]), int(self.padding + self._size[1]/2 + nudge[1]))

    def _get_divided_color_tuple(self, color : tuple[int, int, int, int], divider : int | float, alpha_override : int | None = None) -> tuple[int, int, int, int]:
        """Returns a new tuple with all color values divided and rounded down. Alpha is not divided but can be overridden."""

        if alpha_override != None:
            return (int(color[0]/divider), int(color[1]/divider), int(color[2]/divider), alpha_override)
        return (int(color[0]/divider), int(color[1]/divider), int(color[2]/divider), color[3])
