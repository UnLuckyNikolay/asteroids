import pygame

from shapes.circleshape import CircleShape


class Magnet(CircleShape):
    def __init__(self, position, radius):
        super().__init__(position, pygame.Vector2(0, 0), radius, create_copy_of_position=False)
        self.radius_level = 1


    def upgrade_radius(self):
        match self.radius_level:
            case 1:
                self.radius_level = 2
                self.radius = 150
            case 2:
                self.radius_level = 3
                self.radius = 200

    #def can_upgrade(self, weapon_num):
    #    return (self.money >= self.get_price_weapons(weapon_num))
    
    #def buy_upgrade(self, weapon_num):
    #    self.money = self.money - self.get_price_weapons(weapon_num)
    #    self.weapons[weapon_num].upgrade()