import pygame

from constants import *


class RoundStateManager(pygame.sprite.Sprite):
    def __init__(self, player):
        if hasattr(self, "containers"):
            super().__init__(self.containers) # pyright: ignore[reportAttributeAccessIssue]
        else:
            super().__init__()

        self._score = 0
        self.player = player
        self.round_time : float = 0 # In seconds

        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.position = (30, 30)
        self.color = (150, 150, 150)


    @property
    def score(self):
        return self._score
    
    @score.setter
    def score(self, value):
        self._score = value

    def get_score(self):
        return self._score
    
    def update(self, delta : float):
        self.round_time += delta

    def get_current_time_as_text(self) -> str:
        seconds = int(self.round_time%60)
        seconds = str(seconds) if seconds >= 10 else f"0{str(seconds)}"
        minutes = int(self.round_time//60)

        return f"{minutes}:{seconds}"
    