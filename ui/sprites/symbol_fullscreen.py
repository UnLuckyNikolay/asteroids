import pygame

from ui.simple_sprite import SimpleSprite


class SymbolFullscreen(SimpleSprite):
    def __init__(self, local_x, local_y, color):
        super().__init__(local_x, local_y, color)
    
    def draw(self, screen, position : tuple[int, int], color_override : tuple[int, int, int, int] | None = None):
        color = color_override if color_override != None else self.color
        x = position[0] + self.x
        y = position[1] + self.y

        pygame.draw.lines(screen, color, False, [(x-5, y-10), (x, y-15), (x+5, y-10)], width=3)
        pygame.draw.lines(screen, color, False, [(x-5, y+10), (x, y+15), (x+5, y+10)], width=3)
        pygame.draw.lines(screen, color, False, [(x-10, y-5), (x-15, y), (x-10, y+5)], width=3)
        pygame.draw.lines(screen, color, False, [(x+10, y-5), (x+15, y), (x+10, y+5)], width=3)
        pygame.draw.line(screen, color, (x, y+5), (x, y+15), width=3)
        pygame.draw.line(screen, color, (x+5, y), (x+15, y), width=3)
        pygame.draw.line(screen, color, (x, y-5), (x, y-15), width=3)
        pygame.draw.line(screen, color, (x-5, y), (x-15, y), width=3)
        