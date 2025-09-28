from ui.helpers import draw_polygon

class HealthBar():
    def __init__(self, local_x, local_y, corner_topright, corner_bottomright, handler_lives):
        self.x = local_x
        self.y = local_y
        self.corner_topright = corner_topright
        self.corner_bottomright = corner_bottomright
        self.handler = handler_lives

        self.color_green = (0, 150, 0)
        self.color_yellow = (150, 150, 0)
        self.color_red = (150, 0, 0)

    def draw(self, screen, x, y):
        lives = self.handler()
        match lives:
            case 3:
                draw_polygon(screen, x+self.x, y+self.y, 26, 20, 2, 
                             0, 0, 2, self.color_green)
                draw_polygon(screen, x+self.x+24, y+self.y, 26, 20, 
                             0, 0, 0, 0, self.color_green)
                draw_polygon(screen, x+self.x+48, y+self.y, 26, 20, 
                             0, self.corner_topright, self.corner_bottomright, 0, self.color_green)
            case 2:
                draw_polygon(screen, x+self.x, y+self.y, 26, 20, 
                             2, 0, 0, 2, self.color_yellow)
                draw_polygon(screen, x+self.x+24, y+self.y, 26, 20, 
                             0, 2, 2, 0, self.color_yellow)
            case 1:
                draw_polygon(screen, x+self.x, y+self.y, 26, 20, 
                             2, 2, 2, 2, self.color_red)
            case _:
                return