import pygame

from shapes.circleshape import CircleShape


class Magnet(CircleShape):
    def __init__(self, position, radius):
        super().__init__(position, pygame.Vector2(0, 0), radius, create_copy_of_position=False)
