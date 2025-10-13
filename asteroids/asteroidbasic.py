import pygame, random

from constants import *
from asteroids.asteroid import Asteroid
from asteroids.ores import CopperOre, SilverOre, GoldenOre, Diamond


class AsteroidBasic(Asteroid):
    def __init__(self, position, velocity, max_speed, radius):
        color = random.randint(30, 80)
        super().__init__(position, velocity, max_speed, radius, (color, color, color), (color + 50, color + 50, color + 50), 1)


    def split(self):
        pygame.sprite.Sprite.kill(self)
        self.has_been_hit = True

        if self.radius <= ASTEROID_MIN_RADIUS:
            loot_quality = random.randint(1, 100)
            angle = random.randint(-15, 15)

            if loot_quality > 99:
                velocity = self.velocity.rotate(angle) * LOOT_SLOWDOWN
                loot = Diamond(self.position, velocity)
            elif loot_quality > 95:
                velocity = self.velocity.rotate(angle) * LOOT_SLOWDOWN
                loot = GoldenOre(self.position, velocity)
            elif loot_quality > 85:
                velocity = self.velocity.rotate(angle) * LOOT_SLOWDOWN
                loot = SilverOre(self.position, velocity)
            elif loot_quality > 60:
                velocity = self.velocity.rotate(angle) * LOOT_SLOWDOWN
                loot = CopperOre(self.position, velocity)

        else:
            split_angle = random.uniform(20, 50)
            new_radius = self.radius - ASTEROID_MIN_RADIUS

            velocity = self.velocity.rotate(split_angle) * 1.3
            asteroid_1 = AsteroidBasic(self.position, velocity, int(self.max_speed * 1.3), new_radius)
            
            velocity = self.velocity.rotate(-split_angle) * 1.3
            asteroid_2 = AsteroidBasic(self.position, velocity, int(self.max_speed * 1.3), new_radius)
