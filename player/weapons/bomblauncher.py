import pygame

from sfx_manager import SFXManager, SFX
from player.weapons.weapon import Weapon
from player.weapons.projectiles.bomb import Bomb


class BombLauncher(Weapon):
    def __init__(self, sfxm : SFXManager):
        super().__init__("BombLauncher")
        self.sfxm = sfxm

        self._cooldown = 1.5
        self._explosion_radius = 100
        self._fuse_timer = 2.5

        self._level_max = 5

        self._level_radius = 1
        self._level_max_radius = 3
        self._level_fuse = 1
        self._level_max_fuse = 3


    def upgrade_fuse(self):
        match self._level_fuse:
            case 1:
                self._level += 1
                self._level_fuse += 1
                self._fuse_timer = 2.1
            case 2:
                self._level += 1
                self._level_fuse += 1
                self._fuse_timer = 1.7

    def upgrade_radius(self):
        match self._level_radius:
            case 1:
                self._level += 1
                self._level_radius += 1
                self._explosion_radius = 150
            case 2:
                self._level += 1
                self._level_radius += 1
                self._explosion_radius = 200

    def attempt_shot(self, position, rotation, time_since_last_shot):
        if time_since_last_shot >= self._cooldown:
            self._spawn_bomb((0, -25), position, rotation)
            return True
        else:
            return False
        
    
    def _spawn_bomb(self, dot, position, rotation):
        spawn = pygame.Vector2(dot).rotate(rotation)
        Bomb(pygame.Vector2(position.x + spawn.x, position.y + spawn.y), pygame.Vector2(0, 0), self._explosion_radius, self._fuse_timer, self.sfxm)
                