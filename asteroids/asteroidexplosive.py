import pygame

from constants import *
from asteroids.asteroid import Asteroid
from asteroids.asteroidbasic import AsteroidBasic


class AsteroidExplosive(Asteroid):
    def __init__(self, position, velocity, max_speed):
        super().__init__(position, velocity, max_speed, ASTEROID_MIN_RADIUS * 2, (215, 0, 0), (155, 0, 0), 2)


    def split(self):
        vectors = ((0, 1), (-0.71, 0.71), (-1, 0), (-0.71, -0.71), (0, -1), (0.71, -0.71), (1, 0), (0.71, 0.71))
        for vector in vectors:
            velocity = pygame.Vector2(vector[0], vector[1]) * 120
            AsteroidBasic(self.position, velocity, 120, ASTEROID_MIN_RADIUS)

        self.kill()
