import pygame, pygame.gfxdraw, random, math
from constants import *
from circleshape import CircleShape


class Explosion(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.timer = 0
        self.explosion_count = 3
        self.points_for_drawing_L = []
        self.points_for_drawing_M = []
        self.points_for_drawing_S = []

        self.get_points_all()


    def get_points_all(self):
        self.points_for_drawing_L, self.points_for_drawing_M, self.points_for_drawing_S = self.get_points_for_drawing(1, 0.8, 0.6)


    def get_points_for_drawing(self, size_L, size_M, size_S):
        amount_of_points = int(self.radius / ASTEROID_MIN_RADIUS * 2 + 6 + random.randint(1, 4) * 2)
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