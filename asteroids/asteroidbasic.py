import pygame, random, pygame.gfxdraw
from constants import *
from asteroids.asteroid import Asteroid


class AsteroidBasic(Asteroid):
    def __init__(self, x, y, radius):
        color = random.randint(30, 80)
        super().__init__(x, y, radius, (color, color, color), (color + 50, color + 50, color + 50), 1)


    def split(self):
        pygame.sprite.Sprite.kill(self)
        self.has_been_hit = True
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            split_angle = random.uniform(20, 50)
            new_radius = self.radius - ASTEROID_MIN_RADIUS

            asteroid_1 = AsteroidBasic(self.position.x, self.position.y, new_radius)
            asteroid_1.velocity = self.velocity.rotate(split_angle) * 1.3
            
            asteroid_2 = AsteroidBasic(self.position.x, self.position.y, new_radius)
            asteroid_2.velocity = self.velocity.rotate(-split_angle) * 1.3