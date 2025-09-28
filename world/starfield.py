import pygame, pygame.gfxdraw, opensimplex, numpy
from random import randint

from constants import *


class StarField(pygame.sprite.Sprite):
    """Countless procedurally generated planets as Todd intended"""
    layer = 0 # pyright: ignore
    def __init__(self):
        if hasattr(self, "containers"):
            super().__init__(self.containers) # pyright: ignore[reportAttributeAccessIssue]
        else:
            super().__init__()

        self.stars_big_amount = STAR_BIG_AMOUNT
        self.stars_medium_amount = STAR_MEDIUM_AMOUNT
        self.stars_small_amount = STAR_SMALL_AMOUNT

        color_seed = randint(0, len(SPACE_COLOR_LIST)-1)
        color = SPACE_COLOR_LIST[color_seed]

        color_seed_2 = randint(1, len(SPACE_COLOR_LIST)-1) # Ignores the black color
        if color_seed_2 == color_seed:
            color_seed_2 = 0
        color_2 = SPACE_COLOR_LIST[color_seed_2]
        
        self.array_x = 64
        self.array_y = 36
        self.scale = 10 # Used to get noise gradient
        self.multiplier = 20 # Used to get array up to display resolution

        noise_seed = randint(0, 100000)
        print(f"Setting noise seed to {noise_seed}")
        opensimplex.seed(noise_seed)

        #rng = numpy.random.default_rng(seed=0) # Might need to switch to arrays later
        #ix, iy = rng.random(array_x), rng.random(array_y)
        #array = opensimplex.noise2array(ix, iy)

        bg = pygame.Surface((self.array_x, self.array_y))
        for x in range(self.array_x):
            for y in range(self.array_y):
                gradient = (opensimplex.noise2(x/self.scale, y/self.scale)+1) * 0.5
                bg.set_at((x,y), 
                            (int(color[0] * gradient + color_2[0] * (1 - gradient)), 
                                int(color[1] * gradient + color_2[1] * (1 - gradient)), 
                                int(color[2] * gradient + color_2[2] * (1 - gradient))))

        self.bg_big = pygame.Surface((self.array_x*self.multiplier, self.array_y*self.multiplier))
        self.bg_big = pygame.transform.smoothscale_by(bg, self.multiplier)

        self._generate_stars(self.bg_big)

    def _generate_stars(self, surface):
        """Generates stars and draws them on the surface"""
        for i in range (self.stars_small_amount):
            star = self._generate_star(0)
            self._draw_star(surface, star)
        for i in range (self.stars_medium_amount):
            star = self._generate_star(1)
            self._draw_star(surface, star)
        for i in range (self.stars_big_amount):
            size = randint(2, 4)
            star = self._generate_star(size)
            self._draw_star(surface, star)

    def _generate_star(self, size):
        """Generates and returns a star"""
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
                
    def _draw_star(self, surface, star):
        """Draws the star on the surface"""
        pygame.gfxdraw.filled_circle(surface, *star)
        if star[2] > 0:
            pygame.gfxdraw.filled_circle(surface, star[0], star[1], max(star[2] - 2, 0), (255, 255, 255))

    def draw(self, screen):
        screen.blit(self.bg_big, (0, 0))

    def regenerate(self):
        """Regenerates the background with a new gradient and stars"""
        noise_seed = randint(0, 100000)
        print(f"Setting noise seed to {noise_seed}")
        opensimplex.seed(noise_seed)

        color_seed = randint(0, len(SPACE_COLOR_LIST)-1)
        color = SPACE_COLOR_LIST[color_seed]

        color_seed_2 = randint(1, len(SPACE_COLOR_LIST)-1) # Ignores the black color
        if color_seed_2 == color_seed:
            color_seed_2 = 0
        color_2 = SPACE_COLOR_LIST[color_seed_2]

        bg = pygame.Surface((self.array_x, self.array_y))
        for x in range(self.array_x):
            for y in range(self.array_y):
                gradient = (opensimplex.noise2(x/self.scale, y/self.scale)+1) * 0.5
                bg.set_at((x,y), 
                            (int(color[0] * gradient + color_2[0] * (1 - gradient)), 
                                int(color[1] * gradient + color_2[1] * (1 - gradient)), 
                                int(color[2] * gradient + color_2[2] * (1 - gradient))))

        self.bg_big = pygame.transform.smoothscale_by(bg, self.multiplier)

        self._generate_stars(self.bg_big)
