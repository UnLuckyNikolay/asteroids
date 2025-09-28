import pygame, random, pygame.gfxdraw

from constants import *
from asteroids.asteroid import Asteroid
from asteroids.ores import CopperOre, SilverOre, GoldenOre, Diamond


class AsteroidBasic(Asteroid):
    def __init__(self, x, y, radius):
        color = random.randint(30, 80)
        super().__init__(x, y, radius, (color, color, color), (color + 50, color + 50, color + 50), 1)


    def split(self):
        pygame.sprite.Sprite.kill(self)
        self.has_been_hit = True

        if self.radius <= ASTEROID_MIN_RADIUS:
            loot_quality = random.randint(1, 100)
            angle = random.randint(-15, 15)

            if loot_quality > 99:
                loot = Diamond(self.position.x, self.position.y)
                loot.velocity = self.velocity.rotate(angle) * LOOT_SLOWDOWN
            elif loot_quality > 95:
                loot = GoldenOre(self.position.x, self.position.y)
                loot.velocity = self.velocity.rotate(angle) * LOOT_SLOWDOWN
            elif loot_quality > 85:
                loot = SilverOre(self.position.x, self.position.y)
                loot.velocity = self.velocity.rotate(angle) * LOOT_SLOWDOWN
            elif loot_quality > 60:
                loot = CopperOre(self.position.x, self.position.y)
                loot.velocity = self.velocity.rotate(angle) * LOOT_SLOWDOWN

        else:
            split_angle = random.uniform(20, 50)
            new_radius = self.radius - ASTEROID_MIN_RADIUS

            asteroid_1 = AsteroidBasic(self.position.x, self.position.y, new_radius)
            asteroid_1.velocity = self.velocity.rotate(split_angle) * 1.3
            
            asteroid_2 = AsteroidBasic(self.position.x, self.position.y, new_radius)
            asteroid_2.velocity = self.velocity.rotate(-split_angle) * 1.3
