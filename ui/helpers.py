import pygame, pygame.gfxdraw

def get_points(x, y, 
               height, width, 
               corner_topleft, corner_topright, 
               corner_bottomright, corner_bottomleft
               ) -> list:
    """Returns list of 8 points for drawing a quadrangular polygon with cut corners."""
    points = [(x, y + corner_topleft),
                (x + corner_topleft, y),
                (x + width - corner_topright, y),
                (x + width, y + corner_topright),
                (x + width, y + height - corner_bottomright),
                (x + width - corner_bottomright, y + height),
                (x + corner_bottomleft, y + height),
                (x, y + height - corner_bottomleft)]
    return points

def draw_polygon(screen, 
                 x, y, 
                 height, width, 
                 corner_topleft, corner_topright, 
                 corner_bottomright, corner_bottomleft, 
                 color):
    """Draws a filled quadrangular polygon with cut corners."""
    points = get_points(x, y, 
                        height, width, 
                        corner_topleft, corner_topright, 
                        corner_bottomright, corner_bottomleft)
    pygame.gfxdraw.filled_polygon(screen, points, color)
