import pygame, random

from constants import *
from asteroids.asteroid import Asteroid
from asteroids.ores import CopperOre, SilverOre, GoldenOre, Diamond


class AsteroidHoming(Asteroid):
    def __init__(self, position, velocity, max_speed, target):
        super().__init__(position, velocity, max_speed, ASTEROID_MIN_RADIUS, (115, 0, 170), (75, 0, 130), 3)
        self.target = target

    
    def update(self, dt):
        if self.target.is_alive:
            direction_vector = (self.target.position - self.position).normalize() * self.max_speed
            self.velocity = self.velocity.move_towards(direction_vector, HOMING_SPEED*dt)
        self.position += self.velocity * dt


    def split(self):
        loot_quality = random.randint(1, 100)
        angle = random.randint(-15, 15)

        if loot_quality > 90:
            velocity = self.velocity.rotate(angle) * LOOT_SLOWDOWN
            loot = Diamond(self.position, velocity)
        elif loot_quality > 50:
            velocity = self.velocity.rotate(angle) * LOOT_SLOWDOWN
            loot = GoldenOre(self.position, velocity)
        elif loot_quality > 25:
            velocity = self.velocity.rotate(angle) * LOOT_SLOWDOWN
            loot = SilverOre(self.position, velocity)
        else:
            velocity = self.velocity.rotate(angle) * LOOT_SLOWDOWN
            loot = CopperOre(self.position, velocity)

        self.kill()
