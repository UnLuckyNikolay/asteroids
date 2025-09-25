import pygame, pygame.gfxdraw

from ui.helpers import get_points

class Container(pygame.sprite.Sprite):
    layer = 100 # pyright: ignore
    def __init__(self, 
                 x, y, 
                 width, height,
                 corner_topleft, corner_topright, 
                 corner_bottomright, corner_bottomleft, 
                 color,
                 *elements
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
        self.elements = elements

    def draw(self, screen):
        points = get_points(self.x, self.y, 
                            self.height, self.width, 
                            self.corner_topleft, self.corner_topright, 
                            self.corner_bottomright, self.corner_bottomleft)
        pygame.gfxdraw.filled_polygon(screen, points, (75, 75, 75, 100))
        pygame.draw.polygon(screen, self.color, points, 3)

        for element in self.elements:
            element.draw(screen, self.x, self.y)
