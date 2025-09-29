import pygame, pygame.gfxdraw, copy
from enum import Enum

from constants import *


class ShipType(Enum):
    POLY = "Poly.v1"
    POLY2BP = "Poly.v2:Bp"
    POLY2 = "Poly.v2"
    POLY3 = "Poly.v3"

class Ship():
    def __init__(self, type : ShipType, hitbox_radius, show_hitbox):
        self.type = type
        self.hitbox_radius = hitbox_radius
        self.show_hitbox = show_hitbox

        self.color_outline = PLAYER_COLOR_OUTLINE
        self.color_fill = PLAYER_COLOR_FILL
        self.color_glass = PLAYER_COLOR_GLASS
        self.alpha = 255

        # Each part is [colors[fill_override, outline_override],  [list of dots]]
        self.parts_poly = [
            [[(0, 0, 0), (255, 255, 255)],  [[0, -20], [-10, 15], [10, 15]]]
        ]
        self.parts_poly2bp = [
            [[(20, 100, 200), (255, 255, 255)],  [[-25, -4], [25, -4], [22, 5], [0, 11], [-22, 5]]], # Wings
            [[(20, 100, 200), (255, 255, 255)],  [[20, -4], [20, -9]]],   # Wing guns
            [[(20, 100, 200), (255, 255, 255)],  [[-20, -4], [-20, -9]]], # ^
            [[(20, 100, 200), (255, 255, 255)],  [[7, 0], [-7, 0], [-4, -18], [4, -18]]], # Cockpit
            [[(20, 100, 200), (255, 255, 255)],  [[5, 3], [-5, 3], [-2, -15], [2, -15]]], # Cockpit window
            [[(20, 100, 200), (255, 255, 255)],  [[15, 0], [-15, 0], [-10, 12], [10, 12]]], # Center part
            [[(20, 100, 200), (255, 255, 255)],  [[-5, 12], [5, 12], [8, 20], [-8, 20]]], # Engine
            [[(20, 100, 200), (255, 255, 255)],  [[0, -18], [0, -23]]] # Gun
        ]
        self.parts_poly2 = [
            [[],  [[-25, -4], [25, -4], [22, 5], [0, 11], [-22, 5]]], # Wings
            [[],  [[20, -4], [20, -9]]],   # Wing guns
            [[],  [[-20, -4], [-20, -9]]], # ^
            [[],  [[7, 0], [-7, 0], [-4, -18], [4, -18]]], # Cockpit
            [[self.color_glass],  [[5, 3], [-5, 3], [-2, -15], [2, -15]]], # Cockpit window
            [[],  [[15, 0], [-15, 0], [-10, 12], [10, 12]]], # Center part
            [[],  [[-5, 12], [5, 12], [8, 20], [-8, 20]]], # Engine
            [[],  [[0, -18], [0, -23]]] # Gun
        ]
        black = (41, 41, 41)
        gray_light = (150, 150, 170)
        gray_mid = (119, 119, 132)
        gray_dark = (90, 90, 103)
        glass_light = (90, 120, 150)
        glass_mid = (72, 100, 128)
        glass_dark = (50, 73, 96)
        self.parts_poly3 = [
            [[None, gray_dark],  [[20, -4], [20, -9]]],   # Guns
            [[None, gray_dark],  [[-20, -4], [-20, -9]]], # ^
            [[None, gray_dark],  [[0, -18], [0, -23]]],   # ^
            [[gray_light],  [[-25, -4], [0, -8], [25, -4], [29, 7], [22, 3], [-22, 3], [-29, 7]]], # Wings - light
            [[gray_mid],  [[-23, 1], [23, 1], [29, 7], [22, 3], [-22, 3], [-29, 7]]],              # Wings - mid
            [[gray_dark],  [[4, -18], [-4, -18], [-7, 0], [-11, 3], 
                            [-5, 12], [-8, 20], [8, 20], [5, 12], [11, 3], [7, 0]]], # Body - dark
            [[gray_mid],  [[4, -18], [-4, -18], [-2, -16], [-5, 1], [-6, 3], 
                            [-4, 12], [-6, 20], [6, 20], [4, 12], [6, 3], [5, 1], [2, -16]]], # Body - mid
            [[gray_light],  [[-1, -15], [-3, 3], [-2, 12], [-3, 20], [3, 20], [2, 12], [3, 3], [1, -15]]], # Body - light
            [[glass_dark],  [[-2, -16], [-5, 1], [-3, 3], [3, 3], [5, 1], [2, -16]]], # Glass - dark
            [[glass_mid],  [[-2, -16], [-1, -15], [1, -15], [2, -16]]], # Glass - dark
            [[glass_light],  [[-1, -15], [1, -15], [3, 3], [0, 4], [-3, 3]]], # Glass - dark
        ]

    def switch_model(self, model : ShipType):
        self.type = model

    def draw_rotated(self, screen, x : int, y : int, rotation : int, timer_invul=0):
        """Used to draw ships during gameplay."""
        
        if self.show_hitbox:   # Draws player hit box in dark gray.
            pygame.draw.circle(screen, (50, 50, 50), (x ,y), 1, 2)
            pygame.draw.circle(screen, (50, 50, 50), (x ,y), self.hitbox_radius, 2)

        # Get ship parts
        parts = self.__get_parts(self.type)
        if parts == None:
            return

        # Set opacity based on invulnerability timer
        if timer_invul > 0:
            self.alpha = int(255 - min(timer_invul, PLAYER_TIMER_INVUL) / PLAYER_TIMER_INVUL * 255)

        # Rotate and draw parts
        for part in self.__rotate_sprite(parts, x, y, rotation):
            if len(part[1]) == 2:
                if len(part[0]) < 2:
                    pygame.draw.line(screen, (*self.color_outline, self.alpha), part[1][0], part[1][1], 2)
                else:
                    pygame.draw.line(screen, (*part[0][1], self.alpha), part[1][0], part[1][1], 2)
            elif len(part[1]) > 2:
                if len(part[0]) == 0:
                    pygame.gfxdraw.filled_polygon(screen, part[1], (*self.color_fill, self.alpha))
                    pygame.draw.polygon(screen, (*self.color_outline, self.alpha), part[1], 2)
                else:
                    if part[0][0] != None:
                        pygame.gfxdraw.filled_polygon(screen, part[1], (*part[0][0], self.alpha))
                    if len(part[0]) > 1:
                        pygame.draw.polygon(screen, (*part[0][1], self.alpha), part[1], 2)

    def draw(self, screen, x, y, multiplier=2):
        """Used to draw ships in menus."""

        parts = self.__get_parts(self.type)
        if parts == None:
            return

        for part in self.__move_and_scale_sprite(parts, x, y, multiplier):
            if len(part[1]) == 2:
                if len(part[0]) < 2:
                    pygame.draw.line(screen, self.color_outline, part[1][0], part[1][1], 2)
                else:
                    pygame.draw.line(screen, part[0][1], part[1][0], part[1][1], 2)
            elif len(part[1]) > 2:
                if len(part[0]) == 0:
                    pygame.gfxdraw.filled_polygon(screen, part[1], self.color_fill)
                    pygame.draw.polygon(screen, self.color_outline, part[1], 2)
                else:
                    if part[0][0] != None:
                        pygame.gfxdraw.filled_polygon(screen, part[1], part[0][0])
                    if len(part[0]) > 1:
                        pygame.draw.polygon(screen, part[0][1], part[1], 2)

    
    def __get_parts(self, type):
        match type:
            case ShipType.POLY:
                return self.parts_poly
            case ShipType.POLY2BP:
                return self.parts_poly2bp
            case ShipType.POLY2:
                return self.parts_poly2
            case ShipType.POLY3:
                return self.parts_poly3
            case _:
                print(f"Error: trying to draw invalid ship `{type}`")
                return None

    def __move_and_scale_sprite(self, parts, x, y, multiplier):
        new_parts = copy.deepcopy(parts)

        for i in range(len(new_parts)):
            for j in range(len(new_parts[i][1])):
                new_parts[i][1][j] = [new_parts[i][1][j][0]*multiplier+x, new_parts[i][1][j][1]*multiplier+y]

        return new_parts
    
    def __rotate_sprite(self, parts, x, y, rotation):
        rotated_sprite = []
        for part in parts:
            rotated_part = []
            for dot in part[1]:
                dot_rotated = pygame.Vector2(dot).rotate(rotation)
                rotated_part.append((int(x + dot_rotated.x), int(y + dot_rotated.y)))
            rotated_sprite.append([part[0], rotated_part])
        return rotated_sprite
