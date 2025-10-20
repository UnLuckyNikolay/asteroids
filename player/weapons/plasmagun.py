import pygame

from player.weapons.weapon import Weapon
from player.weapons.projectiles.projectileplasma import ProjectilePlasma


class PlasmaGun(Weapon):
    def __init__(self):
        super().__init__("PlasmaGun")
        self._projectile_speed = 500
        self._cooldown = 0.4

        self._level_projectiles = 1


    def upgrade_projectiles(self):
        self._level += 1
        self._level_projectiles += 1

    def attempt_shot(self, position, rotation, time_since_last_shot):
        if time_since_last_shot >= self._cooldown:
            if self._level_projectiles == 1 or self._level_projectiles == 3:
                self._spawn_bullet((0, 23), position, rotation)

            if self._level_projectiles == 2 or self._level_projectiles == 3:
                self._spawn_bullet((20, 9), position, rotation)
                self._spawn_bullet((-20, 9), position, rotation)
            
            return True
        else:
            return False

    
    def _spawn_bullet(self, dot, position, rotation):
        spawn = pygame.Vector2(dot).rotate(rotation)
        velocity = pygame.Vector2(0, 1).rotate(rotation) * self._projectile_speed
        shot = ProjectilePlasma(pygame.Vector2(position.x + spawn.x, position.y + spawn.y), velocity)
