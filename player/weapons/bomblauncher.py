import pygame

from player.weapons.weapon import Weapon
from player.weapons.projectiles.bomb import Bomb


class BombLauncher(Weapon):
    def __init__(self):
        super().__init__("BombLauncher")
        self._cooldown = 1.0

        self._level_radius = 1


    def upgrade_radius(self):
        self._level += 1
        self._level_radius += 1

    def attempt_shot(self, position, rotation, time_since_last_shot):
        if time_since_last_shot >= self._cooldown:
            self._spawn_bomb((0, -25), position, rotation)
            return True
        else:
            return False
        
    
    def _spawn_bomb(self, dot, position, rotation):
        spawn = pygame.Vector2(dot).rotate(rotation)
        match self._level_radius:
            case 1:
                bomb = Bomb(pygame.Vector2(position.x + spawn.x, position.y + spawn.y), pygame.Vector2(0, 0), 100)
            case 2:
                bomb = Bomb(pygame.Vector2(position.x + spawn.x, position.y + spawn.y), pygame.Vector2(0, 0), 150)
            case 3:
                bomb = Bomb(pygame.Vector2(position.x + spawn.x, position.y + spawn.y), pygame.Vector2(0, 0), 200)
                