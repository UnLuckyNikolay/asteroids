import pygame, random, pygame.gfxdraw
from constants import *
from asteroids.asteroid import Asteroid


class AsteroidGolden(Asteroid):
    def __init__(self, x, y):
        super().__init__(x, y, ASTEROID_MIN_RADIUS, (235, 205, 0), (175, 145, 0), 10)


    def split(self):
        pygame.sprite.Sprite.kill(self)
        self.has_been_hit = True