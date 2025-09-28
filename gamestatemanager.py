import pygame
from constants import *


class GameStateManager():
    def __init__(self, player):
        self._score = 0
        #self.lives = 3
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
        #for weapon in self.player.weapons:
        #    if self._score >= weapon.get_upgrade_cost():
        #        weapon.upgrade()

    def get_score(self):
        return self._score
    
    #def get_lives(self):
    #    return self.lives