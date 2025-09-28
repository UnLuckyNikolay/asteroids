import pygame
from player.weapons.weapon import Weapon
from player.weapons.projectiles.bomb import Bomb


class BombLauncher(Weapon):
    def __init__(self):
        super().__init__((50,), "BombLauncher")
        self.__cooldown = 1.0


    def attempt_shot(self, position, rotation, time_since_last_shot):
        if time_since_last_shot >= self.__cooldown:
            self.spawn_bomb((0, -25), position, rotation)
            return True
        else:
            return False
        
    
    def spawn_bomb(self, dot, position, rotation):
        spawn = pygame.Vector2(dot).rotate(rotation)
        bomb = Bomb(int(position.x + spawn.x), int(position.y + spawn.y))