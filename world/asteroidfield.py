import pygame, random
from constants import *
from asteroids.asteroidbasic import AsteroidBasic
from asteroids.asteroidgolden import AsteroidGolden
from asteroids.asteroidexplosive import AsteroidExplosive
from asteroids.asteroidhoming import AsteroidHoming


class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS),
        ],
    ]


    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0
        self.player = player


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
        if self.spawn_timer > ASTEROID_SPAWN_RATE:
            self.spawn_timer -= ASTEROID_SPAWN_RATE

            edge = random.choice(self.edges)
            speed = random.randint(40, 120)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)
