import pygame, pygame.gfxdraw

from constants import *
from shapes.circleshape import CircleShape


class LiterallyAFuckingMeatCleaverBase(CircleShape):
    """Base class for type checking, use sprites instead."""

    layer = 60 # pyright: ignore
    def __init__(self, position, velocity, sprite_rotation):
        super().__init__(position, velocity, 50)
        self.is_single_use = False
        self.dt : float = sprite_rotation/360

        self.sprite : pygame.Surface
    
    def update(self, dt):
        self.position += self.velocity * dt
        self.dt += dt

    def draw(self, screen : pygame.Surface):
        next_frame = self.sprite.copy()
        next_frame = pygame.transform.rotate(next_frame, self.dt * 360)
        size = next_frame.get_size()
        screen.blit(next_frame, (self.position.x-size[0]/2, self.position.y-size[1]/2))

class LiterallyAFuckingMeatCleaverSprite1(LiterallyAFuckingMeatCleaverBase):
    def __init__(self, position, velocity, sprite_rotation):
        super().__init__(position, velocity, sprite_rotation)
        self.sprite = pygame.Surface((50, 50))
        self.sprite.set_colorkey((1, 1, 1))
        self.sprite.fill((1, 1, 1))

        pygame.gfxdraw.filled_polygon(self.sprite, ((10, 1), (49, 46), (46, 49), (33, 34), (19, 47), (2, 24)), (255, 255, 255))
        pygame.gfxdraw.filled_polygon(self.sprite, ((49, 46), (46, 49), (33, 34), (36, 31)), (255, 0, 0)) # Handle
        pygame.gfxdraw.filled_polygon(self.sprite, ((24, 42), (19, 47), (2, 24), (4, 22), (18, 27), (10, 26), (14, 34)), (255, 0, 0))
        pygame.gfxdraw.filled_circle(self.sprite, 22, 30, 2, (255, 0, 0))
        pygame.gfxdraw.filled_circle(self.sprite, 15, 25, 1, (255, 0, 0))
        pygame.gfxdraw.filled_circle(self.sprite, 19, 22, 1, (255, 0, 0))
        pygame.gfxdraw.filled_circle(self.sprite, 26, 27, 1, (255, 0, 0))
        pygame.gfxdraw.filled_circle(self.sprite, 13, 13, 3, (1, 1, 1))

        pygame.draw.polygon(self.sprite, (0, 0, 0), ((10, 1), (49, 46), (46, 49), (33, 34), (19, 47), (2, 24)), 3)
        pygame.draw.line(self.sprite, (0, 0, 0), (21, 45), (6, 24), 2)
        pygame.draw.line(self.sprite, (0, 0, 0), (33, 34), (35, 32), 3)
        pygame.draw.line(self.sprite, (0, 0, 0), (38, 39), (40, 37), 3)
        pygame.draw.circle(self.sprite, (0, 0, 0), (13, 13), 4, 2)

class LiterallyAFuckingMeatCleaverSprite2(LiterallyAFuckingMeatCleaverBase):
    def __init__(self, position, velocity, sprite_rotation):
        super().__init__(position, velocity, sprite_rotation)
        self.sprite = pygame.Surface((60, 50))
        self.sprite.set_colorkey((1, 1, 1))
        self.sprite.fill((1, 1, 1))

        pygame.gfxdraw.filled_polygon(self.sprite, ((26, 1), (28, 1), (34, 15), (59, 46), (56, 49), (43, 34), (29, 47), (12, 24), (6, 12)), (255, 255, 255))
        pygame.gfxdraw.filled_polygon(self.sprite, ((59, 46), (56, 49), (43, 34), (46, 31)), (255, 0, 0)) # Handle
        pygame.gfxdraw.filled_polygon(self.sprite, ((34, 42), (29, 47), (12, 24), (6, 12), (28, 14), (29, 15), (28, 16), (10, 16), (23, 22), (15, 20), (14, 22), (24, 34)), (255, 0, 0))
        pygame.gfxdraw.filled_circle(self.sprite, 30, 32, 2, (255, 0, 0))
        pygame.gfxdraw.filled_circle(self.sprite, 27, 25, 1, (255, 0, 0))
        pygame.gfxdraw.filled_circle(self.sprite, 29, 22, 1, (255, 0, 0))
        pygame.gfxdraw.filled_circle(self.sprite, 36, 27, 1, (255, 0, 0))
        pygame.gfxdraw.filled_circle(self.sprite, 25, 9, 3, (1, 1, 1))

        pygame.draw.polygon(self.sprite, (0, 0, 0), ((26, 1), (28, 1), (34, 15), (59, 46), (56, 49), (43, 34), (29, 47), (12, 24), (6, 12)), 3)
        pygame.draw.line(self.sprite, (0, 0, 0), (31, 45), (16, 24), 2)
        pygame.draw.line(self.sprite, (0, 0, 0), (43, 34), (45, 32), 3)
        pygame.draw.line(self.sprite, (0, 0, 0), (48, 39), (50, 37), 3)
        pygame.draw.circle(self.sprite, (0, 0, 0), (25, 9), 4, 2)

class LiterallyAFuckingMeatCleaverSprite3(LiterallyAFuckingMeatCleaverBase):
    def __init__(self, position, velocity, sprite_rotation):
        super().__init__(position, velocity, sprite_rotation)
        self.sprite = pygame.Surface((60, 50))
        self.sprite.set_colorkey((1, 1, 1))
        self.sprite.fill((1, 1, 1))

        pygame.gfxdraw.filled_polygon(self.sprite, ((32, 5), (39, 20), (59, 46), (56, 49), (43, 34), (29, 47), (12, 24), (6, 12), (18, 10)), (255, 255, 255))
        pygame.gfxdraw.filled_polygon(self.sprite, ((59, 46), (56, 49), (43, 34), (46, 31)), (255, 0, 0)) # Handle
        pygame.gfxdraw.filled_polygon(self.sprite, ((34, 42), (29, 47), (12, 24), (6, 12), (14, 20), (28, 27), (29, 28), (20, 26), (24, 34)), (255, 0, 0))
        pygame.gfxdraw.filled_circle(self.sprite, 30, 32, 2, (255, 0, 0))
        pygame.gfxdraw.filled_circle(self.sprite, 27, 25, 1, (255, 0, 0))
        pygame.gfxdraw.filled_circle(self.sprite, 29, 22, 1, (255, 0, 0))
        pygame.gfxdraw.filled_circle(self.sprite, 36, 27, 1, (255, 0, 0))
        pygame.gfxdraw.filled_circle(self.sprite, 29, 13, 3, (1, 1, 1))

        pygame.draw.polygon(self.sprite, (0, 0, 0), ((32, 5), (39, 20), (59, 46), (56, 49), (43, 34), (29, 47), (12, 24), (6, 12), (18, 10)), 3)
        pygame.draw.line(self.sprite, (0, 0, 0), (31, 45), (16, 24), 2)
        pygame.draw.line(self.sprite, (0, 0, 0), (43, 34), (45, 32), 3)
        pygame.draw.line(self.sprite, (0, 0, 0), (48, 39), (50, 37), 3)
        pygame.draw.circle(self.sprite, (0, 0, 0), (29, 13), 4, 2)