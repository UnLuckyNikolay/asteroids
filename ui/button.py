import pygame, pygame.gfxdraw
from typing import Callable

class Button(pygame.sprite.Sprite):
    layer = 100 # pyright: ignore
    def __init__(self, 
                 x, y, 
                 width, height,
                 corner_topleft, corner_topright, corner_bottomright, corner_bottomleft, 
                 font, text, text_shift : int,
                 key_func : Callable, 
                 condition_func : Callable = lambda: True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.corner_topleft = corner_topleft
        self.corner_topright = corner_topright
        self.corner_bottomright = corner_bottomright
        self.corner_bottomleft = corner_bottomleft
        self.font = font
        self.text = text
        self.text_shift = text_shift
        self.key_func = key_func
        self.condition_func = condition_func

    def draw(self, screen):
        points = self._get_points(self.x, self.y, 
                                 self.height, self.width, 
                                 self.corner_topleft, self.corner_topright, self.corner_bottomright, self.corner_bottomleft)
        pygame.gfxdraw.filled_polygon(screen, points, (75, 75, 75, 100))
        pygame.draw.polygon(screen, (100, 200, 255, 100), points, 3)
        
        button_text = self.font.render(self.text, True, (80, 180, 220, 100))
        screen.blit(button_text, (self.x + self.text_shift, self.y + int(self.height / 5)))

    def _get_points(self, x, y, height, width, corner_topleft, corner_topright, corner_bottomright, corner_bottomleft):
        """Returns points for drawing the polygon."""
        points = [(x, y + corner_topleft),
                  (x + corner_topleft, y),
                  (x + width - corner_topright, y),
                  (x + width, y + corner_topright),
                  (x + width, y + height - corner_bottomright),
                  (x + width - corner_bottomright, y + height),
                  (x + corner_bottomleft, y + height),
                  (x, y + height - corner_bottomleft)]
        return points
    
    def check_click(self, position):
        if (position[0] > self.x and
            position[0] < self.x + self.width and
            position[1] > self.y and
            position[1] < self.y + self.height):
            return True
        else:
            return False

    def run_if_possible(self):
        if self.condition_func():
            self.key_func()
