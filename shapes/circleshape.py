import pygame
from copy import deepcopy

from constants import *


class CircleShape(pygame.sprite.Sprite):
    def __init__(self, position, velocity, radius, create_copy_of_position=True):
        if hasattr(self, "containers"):
            super().__init__(self.containers) # pyright: ignore[reportAttributeAccessIssue]
        else:
            super().__init__()
        
        if create_copy_of_position:
            self.position : pygame.Vector2 = deepcopy(position)
        else:
            self.position : pygame.Vector2 = position
        self.velocity : pygame.Vector2 = deepcopy(velocity)
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
