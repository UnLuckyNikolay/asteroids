import pygame

from player.weapons.weapon import Weapon
from player.weapons.projectiles.projectileplasma import ProjectilePlasma


class PlasmaGun(Weapon):
    def __init__(self):
        super().__init__("PlasmaGun", 3)
        self.__projectile_speed = 500
        self.__cooldown = 0.4


    def attempt_shot(self, position, rotation, time_since_last_shot):
        if time_since_last_shot >= self.__cooldown:
            level = self.get_level()

            if level == 1 or level == 3:
                self.__spawn_bullet((0, 23), position, rotation)

            if level == 2 or level == 3:
                self.__spawn_bullet((20, 9), position, rotation)
                self.__spawn_bullet((-20, 9), position, rotation)
            
            return True
        else:
            return False

    
    def __spawn_bullet(self, dot, position, rotation):
        spawn = pygame.Vector2(dot).rotate(rotation)
        velocity = pygame.Vector2(0, 1).rotate(rotation) * self.__projectile_speed
        shot = ProjectilePlasma(pygame.Vector2(position.x + spawn.x, position.y + spawn.y), velocity)
