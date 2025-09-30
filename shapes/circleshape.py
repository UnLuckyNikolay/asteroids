import pygame

from constants import *


class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        if hasattr(self, "containers"):
            super().__init__(self.containers) # pyright: ignore[reportAttributeAccessIssue]
        else:
            super().__init__()
        
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius


    def draw(self, screen):
        pass

    def update(self, dt):
        pass

    def check_colision(self, object):
        distance = pygame.math.Vector2.distance_to(self.position, object.position)
        if distance > (self.radius + object.radius):
            return False
        else:
            return True
