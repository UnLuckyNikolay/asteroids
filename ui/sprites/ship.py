import pygame, pygame.gfxdraw, copy
from enum import Enum

from constants import *

class ShipType(Enum):
    POLY = "Poly.v1"
    POLY2 = "Poly.v2"

class Ship():
    def __init__(self, type : ShipType):
        self.type = type

        self.color_outline = list(PLAYER_COLOR_OUTLINE)
        self.color_fill = list(PLAYER_COLOR_FILL)
        self.color_glass = list(PLAYER_COLOR_GLASS)

        # Each part is [[color_override],  [list of dots]]
        self.parts_poly2 = [
            [[],  [[-25, -4], [25, -4], [22, 5], [0, 11], [-22, 5]]], # Wings
            [[],  [[20, -4], [20, -9]]],   # Wing guns
            [[],  [[-20, -4], [-20, -9]]], # ^
            [[],  [[7, 0], [-7, 0], [-4, -18], [4, -18]]], # Cockpit
            [self.color_glass,  [[5, 3], [-5, 3], [-2, -15], [2, -15]]], # Cockpit window
            [[],  [[15, 0], [-15, 0], [-10, 12], [10, 12]]], # Center part
            [[],  [[-5, 12], [5, 12], [8, 20], [-8, 20]]], # Engine
            [[],  [[0, -18], [0, -23]]] # Gun
        ]

    def draw_rotated(self, screen, x : int, y : int, rotation : int):
        """Used to draw ships during gameplay."""
        
        #if PLAYER_SHOW_HITBOX:   # Draws player hit box in dark gray.
        #    pygame.draw.circle(screen, (50, 50, 50), (x ,y), 1, 2)
        #    pygame.draw.circle(screen, (50, 50, 50), (x ,y), self.radius, 2)

        match self.type:
            case ShipType.POLY2:
                parts = self.parts_poly2
            case _:
                print(f"Error: trying to draw invalid ship `{type}`")
                return

        for part in self._rotate_sprite(parts, x, y, rotation):
            if len(part[1]) == 2:
                pygame.draw.line(screen, self.color_outline, part[1][0], part[1][1], 2)
            elif len(part[1]) > 2:
                if len(part[0]) == 0:
                    pygame.gfxdraw.filled_polygon(screen, part[1], self.color_fill)
                    pygame.draw.polygon(screen, self.color_outline, part[1], 2)
                else: 
                    pygame.gfxdraw.filled_polygon(screen, part[1], part[0])

    def draw(self, screen, x, y, multiplier=2):
        """Used to draw ships in menus."""

        match self.type:
            case ShipType.POLY2:
                parts = self.parts_poly2
            case _:
                print(f"Error: trying to draw invalid ship `{type}`")
                return

        for part in self._move_and_scale_sprite(parts, x, y, multiplier):
            if len(part[1]) == 2:
                pygame.draw.line(screen, self.color_outline, part[1][0], part[1][1], 2)
            elif len(part[1]) > 2:
                if len(part[0]) == 0:
                    pygame.gfxdraw.filled_polygon(screen, part[1], self.color_fill)
                    pygame.draw.polygon(screen, self.color_outline, part[1], 2)
                else: 
                    pygame.gfxdraw.filled_polygon(screen, part[1], part[0])


    def _move_and_scale_sprite(self, parts, x, y, multiplier):
        new_parts = copy.deepcopy(parts)

        for i in range(len(new_parts)):
            for j in range(len(new_parts[i][1])):
                new_parts[i][1][j] = [new_parts[i][1][j][0]*multiplier+x, new_parts[i][1][j][1]*multiplier+y]

        return new_parts
    
    def _rotate_sprite(self, parts, x, y, rotation):
        rotated_sprite = []
        for part in parts:
            rotated_part = []
            for dot in part[1]:
                dot_rotated = pygame.Vector2(dot).rotate(rotation)
                rotated_part.append((int(x + dot_rotated.x), int(y + dot_rotated.y)))
            rotated_sprite.append([part[0], rotated_part])
        return rotated_sprite
