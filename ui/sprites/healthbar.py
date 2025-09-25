from ui.helpers import draw_polygon

class HealthBar():
    def __init__(self, local_x, local_y, handler_lives):
        self.x = local_x
        self.y = local_y
        self.handler = handler_lives

    def draw(self, screen, x, y):
        lives = self.handler()
        match lives:
            case 3:
                draw_polygon(screen, x+self.x, y+self.y, 26, 20, 2, 0, 0, 2, (0, 255, 0, 100))
                draw_polygon(screen, x+self.x+24, y+self.y, 26, 20, 0, 0, 0, 0, (0, 255, 0, 100))
                draw_polygon(screen, x+self.x+48, y+self.y, 26, 20, 0, 2, 6, 0, (0, 255, 0, 100))
            case 2:
                draw_polygon(screen, x+self.x, y+self.y, 26, 20, 2, 0, 0, 2, (255, 255, 0, 100))
                draw_polygon(screen, x+self.x+24, y+self.y, 26, 20, 0, 2, 2, 0, (255, 255, 0, 100))
            case 1:
                draw_polygon(screen, x+self.x, y+self.y, 26, 20, 2, 2, 2, 2, (255, 0, 0, 100))
            case _:
                return