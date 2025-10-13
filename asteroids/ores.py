import pygame, random, math, pygame.gfxdraw

from constants import *
from shapes.circleshape import CircleShape


class Ore(CircleShape):
    layer = 30 # pyright: ignore
    def __init__(self, position, velocity, color_fill, color_outline, price, radius, draw_points):
        super().__init__(position, velocity, radius)
        self.max_speed : int = 250
        self.size = int(self.radius / ASTEROID_MIN_RADIUS)
        self.price = price

        self.color_fill = color_fill
        self.color_outline = color_outline

        self.default_points = self.__get_points_for_drawing(draw_points)


    def draw(self, screen):
        new_points = self.__recalculate_points_for_drawing()
        pygame.gfxdraw.filled_polygon(screen, new_points, self.color_fill)
        pygame.draw.polygon(screen, self.color_outline, new_points, self.size + 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def home_towards(self, position : pygame.Vector2):
        direction_vector = (position - self.position).normalize() * self.max_speed
        self.velocity = self.velocity.move_towards(direction_vector, HOMING_SPEED)


    def __get_points_for_drawing(self, draw_points):
        amount_of_points = draw_points
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
            new_points.append((int(point[0]) + self.position[0], int(point[1]) + self.position[1])) # pyright: ignore[reportAttributeAccessIssue]
        return new_points
    
class Diamond(Ore):
    def __init__(self, position, velocity):
        super().__init__(position, velocity, (185, 242, 255), (125, 182, 195), 10, 5, 3)
    
class GoldenOre(Ore):
    def __init__(self, position, velocity):
        super().__init__(position, velocity, (235, 205, 0), (175, 145, 0), 5, 7, 5)
    
class SilverOre(Ore):
    def __init__(self, position, velocity):
        super().__init__(position, velocity, (224, 224, 224), (164, 164, 164), 3, 7, 5)
    
class CopperOre(Ore):
    def __init__(self, position, velocity):
        super().__init__(position, velocity, (206, 112, 43), (146, 72, 13), 1, 7, 5)
