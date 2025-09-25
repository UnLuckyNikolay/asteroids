import pygame, pygame.gfxdraw
from typing import Callable
from ui.container import Container

class Button(Container):
    layer = 100 # pyright: ignore
    def __init__(self,
                 x, y, 
                 width, height,
                 corner_topleft, corner_topright, corner_bottomright, corner_bottomleft, 
                 key_func : Callable, 
                 condition_func : Callable,
                 color,
                 *elements
    ):
        super().__init__(
            x, y, 
            width, height, 
            corner_topleft, corner_topright, corner_bottomright, corner_bottomleft, 
            color,
            *elements
        )
        self.key_func = key_func
        self.condition_func = condition_func

    def run_if_possible(self):
        if self.condition_func():
            self.key_func()
