import pygame
from constants import *


class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
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


    def is_off_screen(self):
        return(
            self.position.x < -ASTEROID_MAX_RADIUS or
            self.position.x > SCREEN_WIDTH + ASTEROID_MAX_RADIUS or
            self.position.y < -ASTEROID_MAX_RADIUS or
            self.position.y > SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
        )