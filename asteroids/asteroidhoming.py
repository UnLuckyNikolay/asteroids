import pygame, pygame.gfxdraw
from constants import *
from asteroids.asteroid import Asteroid


class AsteroidHoming(Asteroid):
    def __init__(self, x, y, target):
        super().__init__(x, y, ASTEROID_MIN_RADIUS, (115, 0, 170), (75, 0, 130), 3)
        self.target = target

    
    def update(self, dt):
        angle = pygame.math.Vector2(self.velocity).angle_to(self.target.position - self.position)
        self.velocity = pygame.Vector2(self.velocity).rotate(angle)
        self.position += self.velocity * dt


    def split(self):
        pygame.sprite.Sprite.kill(self)
        self.has_been_hit = True