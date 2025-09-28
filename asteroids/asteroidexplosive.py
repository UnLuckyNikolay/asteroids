import pygame

from constants import *
from asteroids.asteroid import Asteroid
from asteroids.asteroidbasic import AsteroidBasic


class AsteroidExplosive(Asteroid):
    def __init__(self, x, y):
        super().__init__(x, y, ASTEROID_MIN_RADIUS * 2, (215, 0, 0), (155, 0, 0), 2)


    def split(self):
        pygame.sprite.Sprite.kill(self)
        self.has_been_hit = True
        vectors = ((0, 1), (-0.71, 0.71), (-1, 0), (-0.71, -0.71), (0, -1), (0.71, -0.71), (1, 0), (0.71, 0.71))
        for vector in vectors:
            asteroid_1 = AsteroidBasic(self.position.x, self.position.y, ASTEROID_MIN_RADIUS)
            asteroid_1.velocity = pygame.Vector2(vector[0], vector[1]) * 120