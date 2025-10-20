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
        self.__position = position
        self.__size = size
        self.__corners : tuple[int, int, int, int] = (0, 0, 0, 0)
        self.__color_outline = (200, 200, 200, 255)
        self.__color_fill = (75, 75, 75, 100)
        self.__elements : list[tuple[Any, Allignment]] = []

    def draw(self, screen):
        points = get_points(self.__position, self.__size, self.__corners)
        pygame.gfxdraw.filled_polygon(screen, points, self.__color_fill)
        pygame.draw.polygon(screen, self.__color_outline, points, 3)

        for tuple in self.__elements:
            pos = self.__get_alligned_position(tuple[1])

            if callable(tuple[0]):
                element = tuple[0]()
                if element == None:
                    continue
            else:
                element = tuple[0]

            element.draw(screen, *pos) # pyright: ignore[reportAttributeAccessIssue]

    def set_fill_color(self, color : tuple[int, int, int, int]):
        self.__color_fill = color

    def set_outline_color(self, color : tuple[int, int, int, int]):
        self.__color_outline = color

    def set_corners(self, topleft : int, topright : int, bottomright : int, bottomleft : int):
        self.__corners = (topleft, topright, bottomright, bottomleft)

    def add_element(self, element, allignment : Allignment = Allignment.NONE):
        self.__elements.append((element, allignment))

    def __get_alligned_position(self, allignment : Allignment) -> tuple[int, int]:
        match allignment:
            case Allignment.NONE:
                return self.__position
            case Allignment.CENTER:
                return (int(self.__position[0] + self.__size[0] / 2), int(self.__position[1] + self.__size[1] / 2))
