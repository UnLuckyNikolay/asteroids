import pygame, math, pygame.gfxdraw

from shapes.circleshape import CircleShape
from player.weapons.projectiles.bombexplosion import BombExplosion
from vfx.explosion import Explosion


class Bomb(CircleShape):
    layer = 20 # pyright: ignore
    def __init__(self, position, velocity, explosion_radius):
        super().__init__(position, velocity, 15)
        self.time = 0
        self.color_change = 0
        self.explosion_radius = explosion_radius


    def update(self, dt):
        self.time += dt
        self.radius = int(15 - math.cos(10 * self.time) + 4 * self.time)
        self.color_change = 1 - math.cos(10 * self.time)

    def draw(self, screen):
        if self.time < 2.5:
            pygame.gfxdraw.filled_circle(screen, int(self.position.x), int(self.position.y), self.radius, 
                                         (int(155 + self.color_change * 50), int(self.color_change / 2 * 255), int(self.color_change / 2 * 255)))
            pygame.draw.circle(screen, (115, 0, 0), self.position, self.radius + 2, 3)
        else: 
            self.kill()
            explosion = Explosion(self.position, self.explosion_radius)
            hitbox = BombExplosion(self.position, self.explosion_radius)
            