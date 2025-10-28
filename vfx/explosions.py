import pygame, pygame.gfxdraw, random, math

from constants import *
from shapes.circleshape import CircleShape


class ExplosionBase(CircleShape):
    """Only used for groups!"""
    layer = 10 # pyright: ignore
    def __init__(self, position, radius):
        super().__init__(position, pygame.Vector2(0, 0), radius)


class ExplosionSpiky(ExplosionBase):
    def __init__(self, position : pygame.Vector2, radius : int):
        super().__init__(position, radius)
        self.timer : float = 0
        self.explosion_count : int = 3

        self.points_for_drawing_L = []
        self.points_for_drawing_M = []
        self.points_for_drawing_S = []

        self.get_points_all()

    def get_points_all(self):
        self.points_for_drawing_L, self.points_for_drawing_M, self.points_for_drawing_S = self.get_points_for_drawing(1, 0.8, 0.6)

    def get_points_for_drawing(self, size_L, size_M, size_S):
        amount_of_points = int(self.radius / ASTEROID_MIN_RADIUS * 2 + 6 + random.randint(1, 4) * 2)
        if amount_of_points % 2 == 1:
            amount_of_points += 1
        points_L, points_M, points_S = [], [], []
        random_radius = self.radius * random.uniform(0.8, 1)
        point_far = True

        for i in range(amount_of_points):
            angle = (2 * math.pi * i) / amount_of_points
            points_L.append(((self.position.x + math.cos(angle) * random_radius * size_L), (self.position.y + math.sin(angle) * random_radius * size_L)))
            points_M.append(((self.position.x + math.cos(angle) * random_radius * size_M), (self.position.y + math.sin(angle) * random_radius * size_M)))
            points_S.append(((self.position.x + math.cos(angle) * random_radius * size_S), (self.position.y + math.sin(angle) * random_radius * size_S)))
            if point_far:
                random_radius = self.radius * random.uniform(0.35, 0.6)
                point_far = False
            else:
                random_radius = self.radius * random.uniform(0.7, 1) 
                point_far = True                 
        return points_L, points_M, points_S

    def update(self, dt):
        self.timer += dt
        if self.timer > 0.2:
            if self.explosion_count > 0:
                self.get_points_all()
                self.timer = 0
                self.explosion_count -= 1
            else:
                pygame.sprite.Sprite.kill(self)

    def draw(self, screen):
        pygame.gfxdraw.filled_polygon(screen, self.points_for_drawing_L, (80, 60, 40))
        pygame.gfxdraw.filled_polygon(screen, self.points_for_drawing_M, (255, 50, 0))
        pygame.gfxdraw.filled_polygon(screen, self.points_for_drawing_S, (255, 200, 0))


class ExplosionRound(ExplosionBase):
    """
    Explosion for the player's death.
    
    FOLLOWS PLAYER'S POSITION!
    """

    layer = 90 # Above player
    def __init__(self, position : pygame.Vector2):
        super().__init__(position, 0)
        self.position = position
        self.timer : float = 0
        self.explosion_count : int = 5

        self.explosion_time : float = 2
        self.explosion_pause : float = 0.3

        self.max_radius : int = 30
        self.max_explosion_radius : int = 30
        self.size = self.max_radius + self.max_explosion_radius
        self.size_tuple = pygame.Vector2(self.size, self.size)

        self.explosion_anchors : list[tuple[int, int]] = []
        self.next_angle = random.randint(1, 360)

    def update(self, dt : float):
        self.timer += dt
        while (
            len(self.explosion_anchors) < self.explosion_count 
            and (self.timer // self.explosion_pause) >= len(self.explosion_anchors)
        ):
            distance = random.randint(int(self.max_radius*0.8), self.max_radius)
            new_anchor = pygame.Vector2(distance, 0)
            new_anchor.rotate_ip(self.next_angle)
            self.explosion_anchors.append((int(new_anchor.x+self.size), int(new_anchor.y+self.size))) # Whatever the fuck is here was written after 1 am (=_=)

            self.next_angle += random.randint(139, 149)

    def draw(self, screen : pygame.Surface):
        black = (80, 60, 40)
        red = (255, 50, 0)
        yellow = (255, 200, 0)
        empty = (255, 255, 255)
        colors = (black, red, yellow, empty)

        next_frame = pygame.Surface((self.size*2, self.size*2))
        next_frame.set_colorkey(empty)
        next_frame.fill(empty)

        mp = 25

        phase_pause = 0
        for color in colors:
            for i in range(len(self.explosion_anchors)):
                anchor = self.explosion_anchors[i]
                start_time = self.timer - self.explosion_pause * i

                radius = int(max(start_time-phase_pause, 0)*mp)
                if radius > 0:
                    pygame.gfxdraw.filled_circle(
                        next_frame, 
                        *anchor, 
                        min(self.max_explosion_radius, radius), 
                        color
                    )
            phase_pause += 1

        screen.blit(next_frame, (self.position.x-self.size, self.position.y-self.size))
