from typing import Callable

from ui.helpers import draw_polygon

class HealthBar():
    def __init__(
            self, 
            local_position : tuple[int, int], 
            corner_topright : int, 
            corner_bottomright : int, 
            handler_lives : Callable
    ):
        self.pos = local_position
        self.corner_topright = corner_topright
        self.corner_bottomright = corner_bottomright
        self.handler = handler_lives

        self.color_green = (0, 150, 0, 255)
        self.color_yellow = (150, 150, 0, 255)
        self.color_red = (150, 0, 0, 255)

    def draw(self, screen, position : tuple[int, int]):
        lives = self.handler()
        x = position[0]+self.pos[0]
        y = position[1]+self.pos[1]
        match lives:
            case 3:
                draw_polygon(screen, (x, y), (20, 26), 
                             (2, 0, 0, 2), self.color_green)
                draw_polygon(screen, (x+24, y), (20, 26), 
                             (0, 0, 0, 0), self.color_green)
                draw_polygon(screen, (x+48, y), (20, 26), 
                             (0, self.corner_topright, self.corner_bottomright, 0), self.color_green)
            case 2:
                draw_polygon(screen, (x, y), (20, 26), 
                             (2, 0, 0, 2), self.color_yellow)
                draw_polygon(screen, (x+24, y), (20, 26), 
                             (0, 2, 2, 0), self.color_yellow)
            case 1:
                draw_polygon(screen, (x, y), (20, 26), 
                             (2, 2, 2, 2), self.color_red)
            case _:
                return