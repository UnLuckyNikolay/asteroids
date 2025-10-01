import pygame, pygame.gfxdraw
from typing import Callable, Any

from ui.container import Container, Allignment
from ui.text import Text
from ui.simple_sprite import SimpleSprite
from ui.helpers import get_points

class Switch(Container):
    layer = 100 # pyright: ignore
    def __init__(self,
                 x, y, 
                 width, height,
                 corner_topleft, corner_topright, corner_bottomright, corner_bottomleft, 
                 key_func : Callable, 
                 is_active,
                 color,
                 color_inactive,
                 *tuples_element_allignment : tuple[Any, Allignment]
    ):
        super().__init__(
            x, y, 
            width, height, 
            corner_topleft, corner_topright, corner_bottomright, corner_bottomleft, 
            color,
            *tuples_element_allignment
        )
        self.color_inactive = color_inactive
        self.key_func = key_func
        self.is_active = is_active

    def draw(self, screen):
        points = get_points(self.x, self.y, 
                            self.height, self.width, 
                            self.corner_topleft, self.corner_topright, 
                            self.corner_bottomright, self.corner_bottomleft)
        pygame.gfxdraw.filled_polygon(screen, points, (75, 75, 75, 100))
        if self.is_active:
            pygame.draw.polygon(screen, self.color, points, 3)
        else:
            pygame.draw.polygon(screen, self.color_inactive, points, 3)

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

            if (isinstance(element, Text) or isinstance(element, SimpleSprite)) and self.is_active:
                element.draw(screen, x, y, self.color) # pyright: ignore[reportAttributeAccessIssue]
            else:
                element.draw(screen, x, y) # pyright: ignore[reportAttributeAccessIssue]
    
    def check_click(self, position):
        if (position[0] > self.x and
            position[0] < self.x + self.width and
            position[1] > self.y and
            position[1] < self.y + self.height):
            return True
        else:
            return False

    def run_if_possible(self) -> bool:
        self.key_func()
        self.is_active = False if self.is_active else True            
        return True
