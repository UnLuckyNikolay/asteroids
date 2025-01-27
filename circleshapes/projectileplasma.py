import pygame, pygame.gfxdraw
from constants import *
from circleshape import CircleShape


class ProjectilePlasma(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, 5)

    
    def draw(self, screen):
        pygame.gfxdraw.filled_circle(screen, int(self.position.x), int(self.position.y), self.radius, (150, 255, 150))
        pygame.gfxdraw.filled_circle(screen, int(self.position.x), int(self.position.y), int(self.radius * 0.6), (255, 255, 255))

    
    def update(self, dt):
        self.position += self.velocity * dt
