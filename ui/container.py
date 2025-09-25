import pygame, pygame.gfxdraw

class Container(pygame.sprite.Sprite):
    layer = 100 # pyright: ignore
    def __init__(self, 
                 x, y, 
                 width, height,
                 corner_topleft, corner_topright, corner_bottomright, corner_bottomleft, 
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
        points = self._get_points(self.x, self.y, 
                                 self.height, self.width, 
                                 self.corner_topleft, self.corner_topright, self.corner_bottomright, self.corner_bottomleft)
        pygame.gfxdraw.filled_polygon(screen, points, (75, 75, 75, 100))
        pygame.draw.polygon(screen, self.color, points, 3)

        for element in self.elements:
            element.draw(screen, self.x, self.y)

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
