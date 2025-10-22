import pygame

from ui_elements.simple_sprite import SimpleSprite


class SymbolCross(SimpleSprite):
    def __init__(self, local_x, local_y, color):
        super().__init__(local_x, local_y, color)
    
    def draw(self, screen, position : tuple[int, int], color_override : tuple[int, int, int, int] | None = None):
        color = color_override if color_override != None else self.color
        x = position[0] + self.x
        y = position[1] + self.y
        size = 10

        pygame.draw.line(screen, color, (x-size, y-size), (x+size, y+size), width=4)
        pygame.draw.line(screen, color, (x-size, y+size), (x+size, y-size), width=4)
        