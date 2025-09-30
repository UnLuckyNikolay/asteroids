import pygame, random

from constants import *
from asteroids.asteroidbasic import AsteroidBasic
from asteroids.asteroidgolden import AsteroidGolden
from asteroids.asteroidexplosive import AsteroidExplosive
from asteroids.asteroidhoming import AsteroidHoming


class AsteroidField(pygame.sprite.Sprite):
    def __init__(self, game, player, screen_resolution):
        pygame.sprite.Sprite.__init__(self, self.containers) # pyright: ignore[reportAttributeAccessIssue]
        self.spawn_timer = 0.0
        self.spawn_increase_timer = 0.0
        self.game = game
        self.player = player

        self.edges, self.spawn_rate = self.update_spawns(screen_resolution)


    def update_spawns(self, screen_resolution):
        edges = [
            [
                pygame.Vector2(1, 0),
                lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * screen_resolution[1]),
            ],
            [
                pygame.Vector2(-1, 0),
                lambda y: pygame.Vector2(screen_resolution[0] + ASTEROID_MAX_RADIUS, y * screen_resolution[1]),
            ],
            [
                pygame.Vector2(0, 1),
                lambda x: pygame.Vector2(x * screen_resolution[0], -ASTEROID_MAX_RADIUS),
            ],
            [
                pygame.Vector2(0, -1),
                lambda x: pygame.Vector2(x * screen_resolution[0], screen_resolution[1] + ASTEROID_MAX_RADIUS),
            ],
        ]
        spawn_rate = (ASTEROID_SPAWN_RATE * (1280*720) / (screen_resolution[0]*screen_resolution[1]))
        return edges, spawn_rate

    def spawn(self, radius, position, velocity):
        roll = random.randint(1, 100)
        if roll <= 5:
            asteroid = AsteroidGolden(position.x, position.y)
            asteroid.velocity = velocity * 3
        elif roll <= 12:
            asteroid = AsteroidHoming(position.x, position.y, self.player)
            asteroid.velocity = velocity * 2
        elif roll <= 22:
            asteroid = AsteroidExplosive(position.x, position.y)
            asteroid.velocity = velocity
        else:
            asteroid = AsteroidBasic(position.x, position.y, radius)
            asteroid.velocity = velocity
    
    def update(self, dt):
        self.spawn_timer += dt
        self.spawn_increase_timer += dt

        if self.spawn_timer > self.spawn_rate:
            self.spawn_timer -= self.spawn_rate

            edge = random.choice(self.edges)
            speed = random.randint(40, 120)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)
            
        if self.spawn_increase_timer >= 15:
            self.spawn_increase_timer -= 15
            self.spawn_rate *= 0.9
