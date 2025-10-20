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
        self.__color_outline = (100, 200, 255, 255)
        self.__color_outline_active = (0, 255, 0, 255)
        self.__key_func = key_func
        self.__is_active = is_active

    def draw(self, screen):
        points = get_points(self.__position, self.__size, self.__corners)
        pygame.gfxdraw.filled_polygon(screen, points, self.__color_fill)
        if self.__is_active:
            pygame.draw.polygon(screen, self.__color_outline_active, points, 3)
        else:
            pygame.draw.polygon(screen, self.__color_outline, points, 3)

        for tuple in self.__elements:
            pos = self.__get_alligned_position(tuple[1])

            if callable(tuple[0]):
                element = tuple[0]()
                if element == None:
                    continue
            else:
                element = tuple[0]

            if (isinstance(element, Text) or isinstance(element, SimpleSprite)) and self.__is_active:
                element.draw(screen, *pos, self.__color_outline_active) # pyright: ignore[reportAttributeAccessIssue]
            else:
                element.draw(screen, *pos) # pyright: ignore[reportAttributeAccessIssue]
    
    def check_click(self, position):
        if (position[0] > self.__position[0] and
            position[0] < self.__position[0] + self.__size[0] and
            position[1] > self.__position[1] and
            position[1] < self.__position[1] + self.__size[1]):
            return True
        else:
            return False

    def run_if_possible(self) -> bool:
        self.__key_func()
        self.__is_active = False if self.__is_active else True            
        return True

    def set_active_outline_color(self, color : tuple[int, int, int, int]):
        self.__color_outline_active = color
