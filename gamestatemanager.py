import pygame
from constants import *


class GameStateManager():
    def __init__(self, player):
        self._score = 0
        self.lives = PLAYER_LIVES
        self.player = player

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
        if self._score >= self.player.weapon.get_upgrade_cost():
            self.player.weapon.upgrade()


    def draw(self, screen):
        score_text = self.font.render(f"Score: {self.score}", True, self.color)
        screen.blit(score_text, self.position)
        
        lives_text = self.font.render(f"Lives: {self.lives}", True, self.color)
        screen.blit(lives_text, (self.position[0], self.position[1] + 30))