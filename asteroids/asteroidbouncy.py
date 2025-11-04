import random

from constants import *
from asteroids.asteroid import Asteroid
from asteroids.ores import CopperOre, SilverOre, GoldenOre, Diamond


class AsteroidBouncy(Asteroid):
    def __init__(self, position, velocity, max_speed, radius, game):
        # Color of the Repulsion Gel from Portal 2
        super().__init__(position, velocity, max_speed, radius, (0, 95, 130), (0, 75, 100), 2)
        self.game = game
        self.is_new = True

    
    def update(self, dt): # Rewrites parent method to bounce around the screen
        res = self.game.screen_resolution

        self.position += self.velocity * dt

        if self.position.x - self.radius < 0:
            self.velocity.x = abs(self.velocity.x)
        elif self.position.x + self.radius > res[0]:
            self.velocity.x = -abs(self.velocity.x)
        if self.position.y - self.radius < 0:
            self.velocity.y = abs(self.velocity.y)
        elif self.position.y + self.radius > res[1]:
            self.velocity.y = -abs(self.velocity.y)

    def split(self):
        if self.radius <= ASTEROID_MIN_RADIUS:
            loot_quality = random.randint(1, 100)
            angle = random.randint(-15, 15)

            if loot_quality > 99:
                velocity = self.velocity.rotate(angle) * LOOT_SLOWDOWN
                Diamond(self.position, velocity)
            elif loot_quality > 95:
                velocity = self.velocity.rotate(angle) * LOOT_SLOWDOWN
                GoldenOre(self.position, velocity)
            elif loot_quality > 85:
                velocity = self.velocity.rotate(angle) * LOOT_SLOWDOWN
                SilverOre(self.position, velocity)
            elif loot_quality > 60:
                velocity = self.velocity.rotate(angle) * LOOT_SLOWDOWN
                CopperOre(self.position, velocity)

        else:
            split_angle = random.uniform(20, 50)
            new_radius = self.radius - ASTEROID_MIN_RADIUS

            velocity = self.velocity.rotate(split_angle) * 1.3
            AsteroidBouncy(self.position, velocity, int(self.max_speed * 1.3), new_radius, self.game)
            
            velocity = self.velocity.rotate(-split_angle) * 1.3
            AsteroidBouncy(self.position, velocity, int(self.max_speed * 1.3), new_radius, self.game)

        self.kill()
