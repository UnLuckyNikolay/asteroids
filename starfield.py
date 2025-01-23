import pygame, pygame.gfxdraw, random
from constants import *


class StarField(pygame.sprite.Sprite):
    def __init__(self):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.stars_amount = STAR_AMOUNT
        self.stars = self.generate_stars()

    
    def generate_stars(self):
        stars = []
        for i in range (0, self.stars_amount):
            stars.append((random.randint(5, SCREEN_WIDTH - 5),
                          random.randint(5, SCREEN_HEIGHT - 5),
                          random.randint(0, 3),
                          (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))))
        return stars
    

    def draw(self, screen):
        for star in self.stars:
            pygame.gfxdraw.filled_circle(screen, star[0], star[1], star[2], star[3])
