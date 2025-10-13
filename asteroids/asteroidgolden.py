import pygame, random

from constants import *
from asteroids.asteroid import Asteroid
from asteroids.ores import GoldenOre


class AsteroidGolden(Asteroid):
    def __init__(self, position, velocity, max_speed):
        super().__init__(position, velocity, max_speed, ASTEROID_MIN_RADIUS, (235, 205, 0), (175, 145, 0), 10)


    def split(self):
        loot_amount = random.randint(2,3)
        angle = random.randint(15, 30)

        velocity = self.velocity.rotate(angle) * (0.75 * LOOT_SLOWDOWN)
        loot1 = GoldenOre(self.position, velocity)
        velocity = self.velocity.rotate(-angle) * (0.75 * LOOT_SLOWDOWN)
        loot2 = GoldenOre(self.position, velocity)
        if loot_amount == 3:
            velocity = self.velocity * (0.75 * LOOT_SLOWDOWN)
            loot3 = GoldenOre(self.position, velocity)

        pygame.sprite.Sprite.kill(self)
        self.has_been_hit = True
