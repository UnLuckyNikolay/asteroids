from constants import LEADERBOARD_LENGTH
from ui.container import Container, Allignment
from ui.textf import TextF

class Leaderboards():
    def __init__(self, x, y, font, scores):
        self.x = x
        self.y = y
        self.font = font
        self.scores = scores

    def draw(self, screen):
        containers = []
        
        for i in range(0, min(len(self.scores), LEADERBOARD_LENGTH)):
            containers.append(
                Container(self.x, self.y+65*i, 1080, 48, 15, 8, 15, 8,
                          (200, 200, 200, 100),
                          (TextF("{} - {}", 13, 8, self.font, (200, 200, 200, 100),
                               self.scores[i]['score'],
                               self.scores[i]['name']),
                               Allignment.NONE))
            )
        
        for container in containers:
            container.draw(screen)
