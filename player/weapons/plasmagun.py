import pygame

from sfx_manager import SFXManager, SFX
from player.weapons.weapon import Weapon
from player.weapons.projectiles.projectileplasma import ProjectilePlasma


class PlasmaGun(Weapon):
    def __init__(self, sfxm : SFXManager):
        super().__init__("PlasmaGun")
        self.sfxm = sfxm

        self._projectile_speed = 500
        self._cooldown = 0.4

        self._level_max = 5

        self._level_projectiles = 1
        self._level_max_projectiles = 3
        self._level_cooldown = 1
        self._level_max_cooldown = 3


    def upgrade_cooldown(self):
        match self._level_cooldown:
            case 1:
                self._level += 1
                self._level_cooldown += 1
                self._cooldown = 0.35
            case 2:
                self._level += 1
                self._level_cooldown += 1
                self._cooldown = 0.3

    def upgrade_projectiles(self):
        if self._level_projectiles < 3:
            self._level += 1
            self._level_projectiles += 1

    def attempt_shot(self, position, rotation, time_since_last_shot):
        if time_since_last_shot >= self._cooldown:
            self.sfxm.play_sound(SFX.PLAYER_PLASMA_SHOT)
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
        ProjectilePlasma(pygame.Vector2(position.x + spawn.x, position.y + spawn.y), velocity)
