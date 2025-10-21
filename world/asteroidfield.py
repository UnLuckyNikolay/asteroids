import pygame, random

from constants import *
from asteroids.asteroidbasic import AsteroidBasic
from asteroids.asteroidgolden import AsteroidGolden
from asteroids.asteroidexplosive import AsteroidExplosive
from asteroids.asteroidhoming import AsteroidHoming


class AsteroidField(pygame.sprite.Sprite):
    def __init__(self, game, player, screen_resolution):
        pygame.sprite.Sprite.__init__(self, self.containers) # pyright: ignore[reportAttributeAccessIssue]
        self.game = game
        self.player = player

        self.time_passed_for_spawns = 0.0
        self.time_passed_for_difficulty = 0.0
        self.spawn_time_mp = 1.0

        self.update_spawns(screen_resolution)


    def update_spawns(self, screen_resolution):
        self.edges = [
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
        self.spawn_time = (ASTEROID_SPAWN_RATE * (1280*720) / (screen_resolution[0]*screen_resolution[1]))
    
    def update(self, dt):
        self.time_passed_for_spawns += dt
        self.time_passed_for_difficulty += dt

        spawn_time = self.spawn_time*self.spawn_time_mp

        while self.time_passed_for_spawns > spawn_time:
            self.time_passed_for_spawns -= spawn_time

            edge = random.choice(self.edges)
            speed = random.randint(40, 120)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            self.__spawn(ASTEROID_MIN_RADIUS * kind, position, velocity, speed)
            
        while self.time_passed_for_difficulty >= DIFFICULTY_INCREASE_TIMER:
            self.time_passed_for_difficulty -= DIFFICULTY_INCREASE_TIMER
            self.spawn_time_mp *= DIFFICULTY_INCREASE_MP


    def __spawn(self, radius, position, velocity, speed):
        roll = random.randint(1, 100)
        if roll <= CHANCE_GOLDEN:
            velocity = velocity * 3
            asteroid = AsteroidGolden(position, velocity, speed*3)
        elif roll <= CHANCE_HOMING:
            velocity = velocity * 2
            asteroid = AsteroidHoming(position, velocity, speed*2, self.player)
        elif roll <= CHANCE_EXPLOSIVE:
            velocity = velocity
            asteroid = AsteroidExplosive(position, velocity, speed)
        else:
            velocity = velocity
            asteroid = AsteroidBasic(position, velocity, speed, radius)
