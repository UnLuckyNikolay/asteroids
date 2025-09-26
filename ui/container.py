import pygame, pygame.gfxdraw
from enum import Enum
from typing import Any

from ui.helpers import get_points


class Allignment(Enum):
    NONE = 0
    CENTER = 1

class Container(pygame.sprite.Sprite):
    layer = 100 # pyright: ignore
    def __init__(self, 
                 x, y, 
                 width, height,
                 corner_topleft, corner_topright, 
                 corner_bottomright, corner_bottomleft, 
                 color,
                 *tuples_element_allignment : tuple[Any, Allignment]
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.corner_topleft = corner_topleft
        self.corner_topright = corner_topright
        self.corner_bottomright = corner_bottomright
        self.corner_bottomleft = corner_bottomleft
        self.color = color
        self.tuples = tuples_element_allignment

    def draw(self, screen):
        points = get_points(self.x, self.y, 
                            self.height, self.width, 
                            self.corner_topleft, self.corner_topright, 
                            self.corner_bottomright, self.corner_bottomleft)
        pygame.gfxdraw.filled_polygon(screen, points, (75, 75, 75, 100))
        pygame.draw.polygon(screen, self.color, points, 3)

        for tuple in self.tuples:
            match tuple[1]:
                case Allignment.NONE:
                    x = self.x
                    y = self.y
                case Allignment.CENTER:
                    x = self.x + self.width / 2
                    y = self.y + self.height / 2

            if callable(tuple[0]):
                element = tuple[0]()
                if element == None:
                    continue
            else:
                element = tuple[0]

            element.draw(screen, x, y) # pyright: ignore[reportAttributeAccessIssue]
