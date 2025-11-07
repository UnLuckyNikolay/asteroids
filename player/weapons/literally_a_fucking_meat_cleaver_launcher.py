import pygame

from player.weapons.weapon import Weapon
from player.weapons.projectiles.literally_a_fucking_meat_cleaver import LiterallyAFuckingMeatCleaver


class LiterallyAFuckingMeatCleaverLauncher(Weapon):
    def __init__(self):
        super().__init__("MeatCleavers")
        self._projectile_speed = 300
        self._cooldown = 0.75


    def attempt_shot(self, position, rotation, time_since_last_shot):
        if time_since_last_shot >= self._cooldown:
            self._spawn_cleaver((0, 33), position, rotation)
            self._spawn_cleaver((20, 20), position, rotation-45)
            self._spawn_cleaver((-20, 20), position, rotation+45)
            return True
        else:
            return False

    def _spawn_cleaver(self, dot, position, rotation):
        spawn = pygame.Vector2(dot).rotate(rotation)
        velocity = pygame.Vector2(0, 1).rotate(rotation) * self._projectile_speed
        LiterallyAFuckingMeatCleaver(pygame.Vector2(position.x + spawn.x, position.y + spawn.y), velocity, rotation)
