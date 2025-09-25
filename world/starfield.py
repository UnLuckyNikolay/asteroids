import pygame, pygame.gfxdraw
from random import randint

from constants import *


class StarField(pygame.sprite.Sprite):
    layer = 0 # pyright: ignore[reportAssignmentType]
    def __init__(self):
        if hasattr(self, "containers"):
            super().__init__(self.containers) # pyright: ignore[reportAttributeAccessIssue]
        else:
            super().__init__()

        self.stars_amount = STAR_AMOUNT
        self.start_small_amount = STAR_SMALL_AMOUNT
        self.stars = self._generate_stars()

    def _generate_stars(self):
        stars = []
        for i in range (0, self.stars_amount):
            size = randint(2, 4)
            stars.append(self._generate_star(size))
        for i in range (0, self.start_small_amount):
            stars.append(self._generate_star(1))
        return stars

    def _generate_star(self, size):
            color = randint(1, 4)
            #color = 3
            match color:
                case 1:
                    return (randint(5, SCREEN_WIDTH - 5),
                            randint(5, SCREEN_HEIGHT - 5),
                            size,
                            (randint(150, 210), randint(150, 210), randint(150, 210)))
                case 2:
                    return (randint(5, SCREEN_WIDTH - 5),
                            randint(5, SCREEN_HEIGHT - 5),
                            size,
                            (randint(50, 100), randint(150, 210), randint(150, 210)))
                case 3:
                    return (randint(5, SCREEN_WIDTH - 5),
                            randint(5, SCREEN_HEIGHT - 5),
                            size,
                            (randint(150, 210), randint(50, 100), randint(150, 210)))
                case 4:
                    return (randint(5, SCREEN_WIDTH - 5),
                            randint(5, SCREEN_HEIGHT - 5),
                            size,
                            (randint(150, 210), randint(150, 210), randint(50, 100)))

    def draw(self, screen):
        for star in self.stars:
            pygame.gfxdraw.filled_circle(screen, star[0], star[1], star[2], star[3])
            pygame.gfxdraw.filled_circle(screen, star[0], star[1], max(star[2] - 2, 0), (255, 255, 255))
