import pygame, pygame.gfxdraw

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

class SymbolArrowDown(SimpleSprite):
    def __init__(self, local_x, local_y, color):
        super().__init__(local_x, local_y, color)
    
    def draw(self, screen, position : tuple[int, int], color_override : tuple[int, int, int, int] | None = None):
        color = color_override if color_override != None else self.color
        x = position[0] + self.x
        y = position[1] + self.y

        pygame.gfxdraw.filled_polygon(screen, [(x, y+5), (x-10, y-5), (x+10, y-5)], color)

class SymbolArrowUp(SimpleSprite):
    def __init__(self, local_x, local_y, color):
        super().__init__(local_x, local_y, color)
    
    def draw(self, screen, position : tuple[int, int], color_override : tuple[int, int, int, int] | None = None):
        color = color_override if color_override != None else self.color
        x = position[0] + self.x
        y = position[1] + self.y

        pygame.gfxdraw.filled_polygon(screen, [(x, y-5), (x-10, y+5), (x+10, y+5)], color)
        
class SymbolPencil(SimpleSprite):
    def __init__(self, local_x, local_y, color):
        super().__init__(local_x, local_y, color)
    
    def draw(self, screen, position : tuple[int, int], color_override : tuple[int, int, int, int] | None = None):
        color = color_override if color_override != None else self.color
        x = position[0] + self.x
        y = position[1] + self.y

        pygame.gfxdraw.filled_polygon(screen, [(x-12, y+12), (x-7, y+12), (x-12, y+7)], color)
        pygame.gfxdraw.filled_polygon(screen, [(x-4, y+9), (x-9, y+4), (x+7, y-12), (x+8, y-12), (x+12, y-8), (x+12, y-7)], color)
        