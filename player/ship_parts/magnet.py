import pygame

from shapes.circleshape import CircleShape


class Magnet(CircleShape):
    layer = 49 # pyright: ignore
    def __init__(self, game, position):
        super().__init__(position, pygame.Vector2(0, 0), 0)
