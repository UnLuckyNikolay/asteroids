import pygame, pygame.gfxdraw, random

from constants import *
from asteroids.asteroid import Asteroid
from asteroids.ores import CopperOre, SilverOre, GoldenOre, Diamond


class AsteroidHoming(Asteroid):
    def __init__(self, x, y, target):
        super().__init__(x, y, ASTEROID_MIN_RADIUS, (115, 0, 170), (75, 0, 130), 3)
        self.target = target

    
    def update(self, dt):
        angle = pygame.math.Vector2(self.velocity).angle_to(self.target.position - self.position)
        self.velocity = pygame.Vector2(self.velocity).rotate(angle)
        self.position += self.velocity * dt


    def split(self):
        loot_quality = random.randint(1, 100)
        angle = random.randint(-15, 15)

        if loot_quality > 90:
            loot = Diamond(self.position.x, self.position.y)
            loot.velocity = self.velocity.rotate(angle) * LOOT_SLOWDOWN
        elif loot_quality > 50:
            loot = GoldenOre(self.position.x, self.position.y)
            loot.velocity = self.velocity.rotate(angle) * LOOT_SLOWDOWN
        elif loot_quality > 25:
            loot = SilverOre(self.position.x, self.position.y)
            loot.velocity = self.velocity.rotate(angle) * LOOT_SLOWDOWN
        else:
            loot = CopperOre(self.position.x, self.position.y)
            loot.velocity = self.velocity.rotate(angle) * LOOT_SLOWDOWN

        pygame.sprite.Sprite.kill(self)
        self.has_been_hit = True