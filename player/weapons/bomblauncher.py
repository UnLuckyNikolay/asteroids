import pygame
from player.weapons.weapon import Weapon


class BombLauncher(Weapon):
    def __init__(self):
        super().__init__((50))
        self.__cooldown = 0.4


    def attempt_shot(self, position, rotation, time_since_last_shot):
        if time_since_last_shot >= self.__cooldown:
            self.spawn_bullet((0, -25), position, rotation)
            return True
        else:
            return False
        
    
    def spawn_bullet(self, dot, position, rotation):
        spawn = pygame.Vector2(dot).rotate(rotation)
        #shot = ProjectilePlasma(int(position.x + spawn.x), int(position.y + spawn.y))