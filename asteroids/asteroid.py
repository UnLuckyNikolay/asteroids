import pygame, random, math, pygame.gfxdraw
from abc import ABC, abstractmethod

from constants import *
from shapes.circleshape import CircleShape


class Asteroid(CircleShape):
    layer = 30 # pyright: ignore
    def __init__(self, 
                 position : pygame.Vector2, 
                 velocity : pygame.Vector2, 
                 max_speed : int, 
                 radius : int, 
                 color_fill : tuple[int, int, int], 
                 color_outline : tuple[int, int, int], 
                 reward : int
    ):
        super().__init__(position, velocity, radius)
        self.max_speed : int = max_speed
        self.size : int = int(self.radius / ASTEROID_MIN_RADIUS)
        self.is_dead : bool = False
        self.reward : int = reward

        self.color_fill = color_fill
        self.color_outline = color_outline

        self.default_points = self.__get_points_for_drawing()


    @abstractmethod
    def split(self):
        pass

    
    def draw(self, screen):
        new_points = self.__recalculate_points_for_drawing()
        pygame.gfxdraw.filled_polygon(screen, new_points, self.color_fill)
        pygame.draw.polygon(screen, self.color_outline, new_points, self.size + 2)
    
    def update(self, dt):
        self.position += self.velocity * dt

    def __get_points_for_drawing(self):
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
    
    def __recalculate_points_for_drawing(self):
        new_points = []
        for point in self.default_points:
            new_points.append((int(point[0]) + self.position[0], int(point[1]) + self.position[1]))
        return new_points
