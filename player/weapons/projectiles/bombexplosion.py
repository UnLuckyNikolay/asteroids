import pygame

from shapes.circleshape import CircleShape


class BombExplosion(CircleShape):
    def __init__(self, position, radius):
        super().__init__(position, pygame.Vector2(0,0) , radius)
        