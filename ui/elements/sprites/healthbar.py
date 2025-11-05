import pygame.gfxdraw
from typing import Callable

from ui.helpers import draw_polygon

class HealthBar():
    def __init__(
            self, 
            local_position : tuple[int, int], 
            corner_topright : int, 
            corner_bottomright : int, 
            handler_lives : Callable,
            is_godmode : bool
    ):
        self.pos = local_position
        self.corner_topright = corner_topright
        self.corner_bottomright = corner_bottomright
        self.handler = handler_lives
        self.is_godmode = is_godmode

        self.color_golden = (240, 200, 50, 255)#(240, 180, 60, 255)
        self.color_golden_light = (255, 240, 120, 255)#(255, 220, 70, 255)
        self.color_green = (0, 150, 0, 255)
        self.color_yellow = (150, 150, 0, 255)
        self.color_red = (150, 0, 0, 255)

    def draw(self, screen, position : tuple[int, int]):
        lives = self.handler()
        x = position[0]+self.pos[0]
        y = position[1]+self.pos[1]
        if self.is_godmode:
            draw_polygon(screen, (x, y), (20, 26), 
                            (2, 0, 0, 2), self.color_golden)
            pygame.gfxdraw.filled_polygon(
                screen, 
                [(x, y+15), (x, y+22), (x+20, y+11), (x+20, y+4)], 
                self.color_golden_light
            )
            draw_polygon(screen, (x+24, y), (20, 26), 
                            (0, 0, 0, 0), self.color_golden)
            pygame.gfxdraw.filled_polygon(
                screen, 
                [(x+24, y+15), (x+24, y+22), (x+44, y+11), (x+44, y+4)], 
                self.color_golden_light
            )
            draw_polygon(screen, (x+48, y), (20, 26), 
                            (0, self.corner_topright, self.corner_bottomright, 0), self.color_golden)
            pygame.gfxdraw.filled_polygon(
                screen, 
                [(x+48, y+15), (x+48, y+22), (x+68, y+11), (x+68, y+4)], 
                self.color_golden_light
            )
        elif lives == 3:
            draw_polygon(screen, (x, y), (20, 26), 
                            (2, 0, 0, 2), self.color_green)
            draw_polygon(screen, (x+24, y), (20, 26), 
                            (0, 0, 0, 0), self.color_green)
            draw_polygon(screen, (x+48, y), (20, 26), 
                            (0, self.corner_topright, self.corner_bottomright, 0), self.color_green)
        elif lives == 2:
            draw_polygon(screen, (x, y), (20, 26), 
                            (2, 0, 0, 2), self.color_yellow)
            draw_polygon(screen, (x+24, y), (20, 26), 
                            (0, 2, 2, 0), self.color_yellow)
        elif lives == 1:
            draw_polygon(screen, (x, y), (20, 26), 
                            (2, 2, 2, 2), self.color_red)
                