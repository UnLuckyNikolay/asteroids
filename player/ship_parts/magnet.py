import pygame

from shapes.circleshape import CircleShape


class Magnet(CircleShape):
    def __init__(self, position, radius):
        super().__init__(position, pygame.Vector2(0, 0), radius, create_copy_of_position=False)
        self.radius_level : int = 1
        self.strength_level : int = 1
        self.strength : int = 4

    def upgrade_radius(self):
        match self.radius_level:
            case 1:
                self.radius_level = 2
                self.radius = 175
            case 2:
                self.radius_level = 3
                self.radius = 250

    def upgrade_strength(self):
        match self.strength_level:
            case 1:
                self.strength_level = 2
                self.strength = 7
            case 2:
                self.strength_level = 3
                self.strength = 10
