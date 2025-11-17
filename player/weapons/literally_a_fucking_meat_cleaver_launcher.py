import pygame

from sfx_manager import SFXManager, SFX
from player.weapons.weapon import Weapon
from player.weapons.projectiles.literally_a_fucking_meat_cleaver import (
    LiterallyAFuckingMeatCleaverSprite1,
    LiterallyAFuckingMeatCleaverSprite2,
    LiterallyAFuckingMeatCleaverSprite3
)


# https://www.youtube.com/watch?v=vjBFftpQxxM is fire
class LiterallyAFuckingMeatCleaverLauncher(Weapon):
    def __init__(self, sfxm : SFXManager):
        super().__init__("MeatCleavers")
        self.sfxm = sfxm

        self._projectile_speed = 300
        self._cooldown = 1.0

        self._level = 666


    def attempt_shot(self, position, rotation, time_since_last_shot):
        if time_since_last_shot >= self._cooldown:
            self.sfxm.play_sound(SFX.PLAYER_CLEAVERS)
            self._spawn_cleaver(LiterallyAFuckingMeatCleaverSprite1, (20, 20), position, rotation-45)
            self._spawn_cleaver(LiterallyAFuckingMeatCleaverSprite2, (0, 33), position, rotation)
            self._spawn_cleaver(LiterallyAFuckingMeatCleaverSprite3, (-20, 20), position, rotation+45)
            return True
        else:
            return False

    def _spawn_cleaver(self, cleaver, dot, position, rotation):
        spawn = pygame.Vector2(dot).rotate(rotation)
        velocity = pygame.Vector2(0, 1).rotate(rotation) * self._projectile_speed
        cleaver(pygame.Vector2(position.x + spawn.x, position.y + spawn.y), velocity, rotation)
