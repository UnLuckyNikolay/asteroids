import pygame, pygame.gfxdraw

from ui.elements.simple_sprite import SimpleSprite


class AmogusBlue(SimpleSprite):
    def __init__(self, local_x, local_y):
        super().__init__(local_x, local_y, None)
    
    def draw(self, screen, position : tuple[int, int], color_override : tuple[int, int, int, int] | None = None):
        #color = color_override if color_override != None else self.color
        x = position[0] + self.x
        y = position[1] + self.y

        blue = (0, 75, 180, 255)
        blue_fill = (0, 100, 250, 255)
        gray = (150, 150, 150, 255)
        gray_fill = (200, 200, 200, 255)

        # Knife
        pygame.gfxdraw.filled_polygon(
           screen,
           [(x-47, y+4), (x-37, y+15), (x-32, y+17), (x-31, y+9)], 
           gray_fill
        )
        pygame.draw.lines(
            screen, gray, False, 
            [(x-26, y+12), (x-47, y+4), (x-37, y+15), (x-32, y+17), (x-31, y+9)], 
            width=3
        )
        # Hand
        pygame.gfxdraw.filled_circle(screen, int(x-22), int(y+13), 5, blue_fill)
        pygame.draw.circle(screen, blue, (x-22, y+13), 7, width=3)
        # Backpack
        points_backpack = [
            (x-13, y+12), (x-19, y+12), (x-22, y+10), (x-23, y-9), (x-20, y-11), 
            (x-16, y-12)
        ]
        pygame.gfxdraw.filled_polygon(screen, points_backpack, blue_fill)
        pygame.draw.polygon(screen, blue, points_backpack, width=3)
        # Body
        points_body = [
            (x-13, y+13), (x-16, y-12), (x-15, y-18), (x-11, y-22), (x-6, y-23), 
            (x, y-23), (x+6, y-21), (x+20, y+4), (x+21, y+10), (x+19, y+15), (x+14, y+15),
            (x+10, y+10), (x+2, y+11), (x+2, y+18), (x-2, y+21), (x-8, y+20), (x-13, y+13)
        ]
        pygame.gfxdraw.filled_polygon(screen, points_body, blue_fill)
        pygame.draw.polygon(screen, blue, points_body, width=3)
        # Head
        points_head = [
            (x+1, y-7), (x+6, y-9), (x+7, y-14), (x+4, y-17), (x-4, y-16), 
            (x-10, y-13), (x-11, y-10), (x-8, y-6), (x+1, y-7)
        ]
        pygame.gfxdraw.filled_polygon(screen, points_head, gray_fill)
        pygame.draw.polygon(screen, gray, points_head, width=3)
        # Hand raised
        pygame.gfxdraw.filled_circle(screen, int(x+20), int(y-20), 5, blue_fill)
        pygame.draw.circle(screen, blue, (x+20, y-20), 7, width=3)
        
class AmogusPink(SimpleSprite):
    def __init__(self, local_x, local_y):
        super().__init__(local_x, local_y, None)
    
    def draw(self, screen, position : tuple[int, int], color_override : tuple[int, int, int, int] | None = None):
        #color = color_override if color_override != None else self.color
        x = position[0] + self.x
        y = position[1] + self.y

        pink = (90, 20, 100, 255)
        pink_fill = (150, 30, 175, 255)
        gray = (150, 150, 150, 255)
        gray_fill = (200, 200, 200, 255)

        # Hand
        pygame.gfxdraw.filled_circle(screen, int(x+30), int(y+10), 5, pink_fill)
        pygame.draw.circle(screen, pink, (x+30, y+10), 7, width=3)
        # Backpack
        points_backpack = [
            (x+13, y+12), (x+19, y+12), (x+22, y+10), (x+23, y-9), (x+20, y-11), 
            (x+16, y-12)
        ]
        pygame.gfxdraw.filled_polygon(screen, points_backpack, pink_fill)
        pygame.draw.polygon(screen, pink, points_backpack, width=3)
        # Body
        points_body = [
            (x+13, y+13), (x+16, y-12), (x+15, y-18), (x+11, y-22), (x+6, y-23), 
            (x, y-23), (x-6, y-21), (x-20, y+4), (x-21, y+10), (x-19, y+15), (x-14, y+15),
            (x-10, y+10), (x-2, y+11), (x-2, y+18), (x+2, y+21), (x+8, y+20), (x+13, y+13)
        ]
        pygame.gfxdraw.filled_polygon(screen, points_body, pink_fill)
        pygame.draw.polygon(screen, pink, points_body, width=3)
        # Head
        points_head = [
            (x-1, y-7), (x-6, y-9), (x-7, y-14), (x-4, y-17), (x+4, y-16), 
            (x+10, y-13), (x+11, y-10), (x+8, y-6), (x-1, y-7)
        ]
        pygame.gfxdraw.filled_polygon(screen, points_head, gray_fill)
        pygame.draw.polygon(screen, gray, points_head, width=3)
        # Hand raised
        pygame.gfxdraw.filled_circle(screen, int(x-20), int(y-20), 5, pink_fill)
        pygame.draw.circle(screen, pink, (x-20, y-20), 7, width=3)