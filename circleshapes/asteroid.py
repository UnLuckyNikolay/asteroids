import pygame, random, math, pygame.gfxdraw
from constants import *
from circleshape import CircleShape


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.points_for_drawing = self.get_points_for_drawing()
        

    def get_points_for_drawing(self):
        amount_of_points = int(self.radius / ASTEROID_MIN_RADIUS * 7 + 7)
        points = []
        random_radius = self.radius * random.uniform(0.7, 1.1)

        for i in range(amount_of_points):
            angle = (2 * math.pi * i) / amount_of_points
            x = math.cos(angle) * random_radius
            y = math.sin(angle) * random_radius
            points.append((x, y))
            random_radius = (random_radius + self.radius * random.uniform(0.7, 1.1)) / 2
        return points
    

    def recalculate_points_for_drawing(self):
        old_points = self.points_for_drawing
        new_points = []
        for point in old_points:
            new_points.append((int(point[0]) + self.position.x, int(point[1]) + self.position.y))
        return new_points

    
    def draw(self, screen):
        #pygame.draw.circle(screen, "white", (self.position.x, self.position.y), self.radius, 2)
        pygame.gfxdraw.aapolygon(screen, self.recalculate_points_for_drawing(), (255, 255, 255))

    
    def update(self, dt):
        self.position += self.velocity * dt


    def split(self):
        pygame.sprite.Sprite.kill(self)
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            split_angle = random.uniform(20, 50)
            new_radius = self.radius - ASTEROID_MIN_RADIUS

            asteroid_1 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid_1.velocity = self.velocity.rotate(split_angle) * 1.2
            
            asteroid_2 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid_2.velocity = self.velocity.rotate(-split_angle) * 1.2
