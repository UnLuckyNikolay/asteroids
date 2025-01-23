import pygame, pygame.gfxdraw, random, math
from constants import *
from circleshape import CircleShape


class Explosion(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.timer = 0
        self.explosion_count = 3
        self.points_for_drawing = self.get_points_for_drawing()


    def get_points_for_drawing(self):
        amount_of_points = int(self.radius / ASTEROID_MIN_RADIUS * 2 + 6 + random.randint(1, 4) * 2)
        points = []
        random_radius = self.radius * random.uniform(0.8, 1)
        point_far = True

        for i in range(amount_of_points):
            angle = (2 * math.pi * i) / amount_of_points
            x = self.position.x + math.cos(angle) * random_radius
            y = self.position.y + math.sin(angle) * random_radius
            points.append((x, y))
            if point_far:
                random_radius = self.radius * random.uniform(0.35, 0.6)
                point_far = False
            else:
                random_radius = self.radius * random.uniform(0.7, 1) 
                point_far = True                 
        return points
    

    def recalculate_points_for_drawing(self):
        old_points = self.points_for_drawing
        new_points = []
        for point in old_points:
            new_points.append((int(point[0]) + self.position.x, int(point[1]) + self.position.y))
        return new_points


    def update(self, dt):
        self.timer += dt
        if self.timer > 0.2:
            if self.explosion_count > 0:
                self.points_for_drawing = self.get_points_for_drawing()
                self.timer = 0
                self.explosion_count -= 1
            else:
                pygame.sprite.Sprite.kill(self)


    def draw(self, screen):
        pygame.gfxdraw.aapolygon(screen, self.points_for_drawing, (255, 100, 0))