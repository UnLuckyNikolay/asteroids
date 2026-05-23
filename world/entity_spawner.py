import pygame, random
from typing import Callable, Any
from enum import Enum

from globals import *
from asteroids.asteroidbasic import AsteroidBasic
from asteroids.asteroidgolden import AsteroidGolden
from asteroids.asteroidexplosive import AsteroidExplosive
from asteroids.asteroidhoming import AsteroidHoming
from asteroids.asteroidbouncy import AsteroidBouncy


class ESMode(Enum):
    AMBIENT = 0
    ASTEROIDS_STANDARD = 1

class EntitySpawner(pygame.sprite.Sprite):
    def __init__(self, player, getter_screen_resolution : Callable[[], tuple[int, int]]):
        if hasattr(self, "containers"):
            super().__init__(self.containers) # pyright: ignore[reportAttributeAccessIssue]
        else:
            super().__init__()
            
        self.player = player
        self.getter_screen_res = getter_screen_resolution
        
        self._mode : ESMode = ESMode.AMBIENT
        self._time_passed : float # Isn't reduced
        self._time_passed_for_spawns : float # Reduced by spawns
        self._time_passed_for_difficulty : float

        self._edges : list[tuple[pygame.Vector2, Callable[[Any], pygame.Vector2]]]

        self._amount_homing : int = 0
        self._amount_homing_max : int = 3

        self._difficulty_increase_timer : float = DIFFICULTY_INCREASE_TIMER

        self._spawn_time : float # Base, depends on the screen resolution
        self._spawn_time_mp : float # Decreases with time
        self._spawn_time_mp_increase : float = DIFFICULTY_INCREASE_MP
        self._spawn_time_mp_min : float = 0.25

        self._speed_mod : int
        self._speed_mod_increase : int = 2
        self._speed_mod_max : int = 40

        self._chance_golden = CHANCE_GOLDEN
        self._chance_homing = self._chance_golden + CHANCE_HOMING
        self._chance_explosive = self._chance_homing + CHANCE_EXPLOSIVE
        self._chance_bouncy = self._chance_explosive + CHANCE_BOUNCY

        self.update_spawns(getter_screen_resolution())
        self.reset()


    def reset(self):
        self._spawn_time_mp = 1
        self._speed_mod = 0
        self._time_passed = 0.0
        self._time_passed_for_spawns = 0.0
        self._time_passed_for_difficulty = 0.0

    def update_spawns(self, screen_resolution : tuple[int, int]):
        self._edges = [
            (
                pygame.Vector2(1, 0),
                lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * screen_resolution[1]),
            ),
            (
                pygame.Vector2(-1, 0),
                lambda y: pygame.Vector2(screen_resolution[0] + ASTEROID_MAX_RADIUS, y * screen_resolution[1]),
            ),
            (
                pygame.Vector2(0, 1),
                lambda x: pygame.Vector2(x * screen_resolution[0], -ASTEROID_MAX_RADIUS),
            ),
            (
                pygame.Vector2(0, -1),
                lambda x: pygame.Vector2(x * screen_resolution[0], screen_resolution[1] + ASTEROID_MAX_RADIUS),
            ),
        ]
        self._spawn_time = (ASTEROID_SPAWN_RATE * (1280*720) / (screen_resolution[0]*screen_resolution[1])) # Very elegant, I know

    def kill_asteroid(self, asteroid):
        if not asteroid.is_dead:
            self._check_asteroid(asteroid)
            asteroid.is_dead = True
            asteroid.kill()

    def split_asteroid(self, asteroid):
        if not asteroid.is_dead:
            self._check_asteroid(asteroid)
            asteroid.is_dead = True
            asteroid.split()

    def _check_asteroid(self, asteroid):
        if isinstance(asteroid, AsteroidHoming):
            self._amount_homing -= 1
    
    def switch_mode(self, mode : ESMode):
        self._mode = mode
        self.reset()
    
    def update(self, dt):
        self._time_passed += dt

        # Asteroid spawn budget
        if self._mode == ESMode.AMBIENT:
            self._time_passed_for_spawns += dt/3
        else:
            self._time_passed_for_spawns += dt

        spawn_time = self._spawn_time*self._spawn_time_mp

        while self._time_passed_for_spawns > spawn_time:
            self._time_passed_for_spawns -= spawn_time

            edge = random.choice(self._edges)
            speed = random.randint(40, 80) + self._speed_mod
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            if self._mode == ESMode.AMBIENT:
                self._spawn_ambient(ASTEROID_MIN_RADIUS * kind, position, velocity, speed)
            else:
                self._spawn(ASTEROID_MIN_RADIUS * kind, position, velocity, speed)

        if self._mode != ESMode.AMBIENT:

            # Difficulty increase
            self._time_passed_for_difficulty += dt

            while self._time_passed_for_difficulty >= self._difficulty_increase_timer:
                self._time_passed_for_difficulty -= self._difficulty_increase_timer
                self._spawn_time_mp *= self._spawn_time_mp_increase
                if self._spawn_time_mp < self._spawn_time_mp_min:
                    self._spawn_time_mp = self._spawn_time_mp_min
                self._speed_mod += self._speed_mod_increase
                if self._speed_mod > self._speed_mod_max:
                    self._speed_mod = self._speed_mod_max


    def _spawn(self, radius, position, velocity, speed):
        roll = random.randint(1, 100)
        if roll <= self._chance_golden:
            AsteroidGolden(position, velocity*3, speed*3)
        elif roll <= self._chance_homing and self._amount_homing < self._amount_homing_max:
            self._amount_homing += 1
            AsteroidHoming(position, velocity*2, speed*2, self.player)
        elif roll <= self._chance_explosive:
            AsteroidExplosive(position, velocity, speed)
        elif roll <= self._chance_bouncy:
            AsteroidBouncy(position, velocity, speed, radius, self.getter_screen_res)
        else:
            AsteroidBasic(position, velocity, speed, radius)
    
    def _spawn_ambient(self, radius, position, velocity, speed):
        AsteroidBasic(position, velocity, speed, radius)
