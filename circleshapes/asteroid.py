import pygame, random, math, pygame.gfxdraw
from constants import *
from circleshape import CircleShape


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.size = int(self.radius / ASTEROID_MIN_RADIUS)
        self.has_been_hit = False

        self.__color_fill = random.randint(30, 80)
        self.color_fill = (self.__color_fill, self.__color_fill, self.__color_fill)
        self.__color_outline = self.__color_fill + 50
        self.color_outline = (self.__color_outline, self.__color_outline, self.__color_outline)

        self.default_points = self.get_points_for_drawing()


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
        new_points = []
        for point in self.default_points:
            new_points.append((int(point[0]) + self.position.x, int(point[1]) + self.position.y))
        return new_points

    
    def draw(self, screen):
        new_points = self.recalculate_points_for_drawing()
        pygame.gfxdraw.filled_polygon(screen, new_points, self.color_fill)
        pygame.draw.polygon(screen, self.color_outline, new_points, self.size + 2)
#        pygame.gfxdraw.aapolygon(screen, points, (255, 255, 255))

    
    def update(self, dt):
        self.position += self.velocity * dt


    def split(self):
        pygame.sprite.Sprite.kill(self)
        self.has_been_hit = True
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            split_angle = random.uniform(20, 50)
            new_radius = self.radius - ASTEROID_MIN_RADIUS

            asteroid_1 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid_1.velocity = self.velocity.rotate(split_angle) * 1.3
            
            asteroid_2 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid_2.velocity = self.velocity.rotate(-split_angle) * 1.3
