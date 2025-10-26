from constants import LEADERBOARD_LENGTH
from ui_elements.container import Container, Allignment
from ui_elements.text import TextPlain

class Leaderboard():
    def __init__(self, x, y, font, scores):
        self.x = x
        self.y = y
        self.font = font
        self.scores = scores

    def draw(self, screen):
        containers = []
        
        for i in range(0, min(len(self.scores), LEADERBOARD_LENGTH)):
            match i:
                case 0:
                    color = (185, 242, 255, 255) # Diamond
                case 1:
                    color = (255, 233, 0, 255) # Gold
                case 2:
                    color = (192, 192, 192, 255) # Silver
                case 3:
                    color = (206, 137, 70, 255) # Bronze
                case _:
                    color = (240, 240, 240, 255)

            c_next_board = Container((self.x, self.y+65*i), (1080, 48), (15, 8, 15, 8))
            c_next_board.set_outline_color(color)
            c_next_board.set_fill_color((int(color[0]/3), int(color[1]/3), int(color[2]/3), 100))
            c_next_board.add_element(
                TextPlain(
                    "{} - {}", self.font, color,
                    self.scores[i]['score'],
                    self.scores[i]['name']
                ),
                Allignment.LEFT_WALL,
                (13, 0)
            )
            containers.append(c_next_board)
        
        for container in containers:
            container.draw(screen)
