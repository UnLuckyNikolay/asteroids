import pygame, pygame.gfxdraw, opensimplex, numpy
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

        noise_seed = randint(0, 100000)
        print(f"Setting noise seed to {noise_seed}")
        opensimplex.seed(noise_seed)

        color_seed = randint(0, len(SPACE_COLOR_LIST)-1)
        color = SPACE_COLOR_LIST[color_seed]
        
        array_x = 64
        array_y = 36
        multiplier = 20
        scale = 10

        #rng = numpy.random.default_rng(seed=0) # Might need to switch to arrays later
        #ix, iy = rng.random(array_x), rng.random(array_y)
        #array = opensimplex.noise2array(ix, iy)

        self.bg = pygame.Surface((array_x, array_y))
        for x in range(array_x):
            for y in range(array_y):
                gradient = (opensimplex.noise2(x/scale, y/scale)+1) * 0.5
                self.bg.set_at((x,y), 
                               (int(color[0] * gradient), 
                                int(color[1] * gradient), 
                                int(color[2] * gradient)))

        self.bg_big = pygame.Surface((array_x*multiplier, array_y*multiplier))
        self.bg_big = pygame.transform.smoothscale_by(self.bg, multiplier)

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
        screen.blit(self.bg_big, (0, 0))
        for star in self.stars:
            pygame.gfxdraw.filled_circle(screen, star[0], star[1], star[2], star[3])
            pygame.gfxdraw.filled_circle(screen, star[0], star[1], max(star[2] - 2, 0), (255, 255, 255))
