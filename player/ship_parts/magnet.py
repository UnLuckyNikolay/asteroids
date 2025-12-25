import pygame

from shapes.circleshape import CircleShape


class Magnet(CircleShape):
    def __init__(self, position):
        super().__init__(position, pygame.Vector2(0, 0), 100, create_copy_of_position=False)

        self._level : int = 1
        self._level_max : int = 5
        self._level_radius : int = 1
        self._level_max_radius : int = 3
        self._level_strength : int = 1
        self._level_max_strength : int = 3

        self._strength : int = 240

    def get_strength(self):
        return self._strength

    def upgrade_radius(self):
        self._level += 1
        match self._level_radius:
            case 1:
                self._level_radius = 2
                self.radius = 175
            case 2:
                self._level_radius = 3
                self.radius = 250

    def upgrade_strength(self):
        self._level += 1
        match self._level_strength:
            case 1:
                self._level_strength = 2
                self._strength = 360
            case 2:
                self._level_strength = 3
                self._strength = 600
