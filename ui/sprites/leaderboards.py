import json

from constants import LEADERBOARD_LENGTH
from ui.container import Container
from ui.textf import TextF

class Leaderboards():
    def __init__(self, x, y, font):
        self.x = x
        self.y = y
        self.font = font

    def draw(self, screen):
        containers = []            
        try:
            with open("leaderboard.json", "r") as file:
                scores = json.load(file)
        except FileNotFoundError:
            scores = []
        
        for i in range(0, min(len(scores), LEADERBOARD_LENGTH)):
            containers.append(
                Container(self.x, self.y+65*i, 1080, 48, 15, 8, 15, 8,
                          (200, 200, 200, 100),
                          TextF("{} - {}", 12, 9, self.font, (200, 200, 200, 100),
                               scores[i]['score'],
                               scores[i]['name']))
            )
        
        for container in containers:
            container.draw(screen)
