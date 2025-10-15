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
        self.time = 0

        self.show_hitbox = show_hitbox
        self.hitbox_radius = hitbox_radius

        self.color_outline = PLAYER_COLOR_OUTLINE
        self.color_fill = PLAYER_COLOR_FILL
        self.color_glass = PLAYER_COLOR_GLASS
        self.alpha = 255

        # Engine animation
        self.engine_vfx = [[[(-6, -2), (-6, 0), (-5, 4), (-4, 6), (-3, 7), (0, 8), (3, 7), (4, 6), (5, 4), (6, 0), (6, -2)], # frame 1
                            [(-4, -2), (-4, 0), (-3, 4), (-2, 6), (-1, 7), (0, 6), (1, 7), (2, 6), (3, 4), (4, 0), (4, -2)]],
                           [[(-5, -2), (-5, 0), (-4, 3), (-3, 5), (-2, 6), (0, 7), (2, 6), (3, 5), (4, 3), (5, 0), (5, -2)], # frame 2
                            [(-3, -2), (-3, 0), (-2, 3), (-1, 5), (0, 6), (1, 5), (2, 3), (3, 0), (3, -2)]]]
        self.engine_vfx_timer = 0.2 # Duration of a frame in sec
        self.engine_vfx_current_frame : int = -1

        # Colors for parts
        white = (255, 255, 255)
        gray_light = (150, 150, 170)
        gray_mid = (119, 119, 132)
        gray_dark = (90, 90, 103)
        black = (0, 0, 0)

        glass_light = (90, 120, 150)
        glass_mid = (72, 100, 128)
        glass_dark = (50, 73, 96)

        # Each part is [colors[fill_override(optional), outline_override(optional)],  [list of dots]]
        # ! Colors for the engine are in the reverse order and are not optional: [outline, fill]
        self.engine_anchor_poly = (0, 15)
        self.engine_colors_poly = [white, black]
        self.parts_poly = [
            [[black, white],  [[0, -20], [-10, 15], [10, 15]]]
        ]

        self.engine_anchor_poly2bp = (0, 20)
        self.engine_colors_poly2bp = [white, (20, 100, 200)]
        self.parts_poly2bp = [
            [[(20, 100, 200), white],  [[-25, -4], [25, -4], [22, 5], [0, 11], [-22, 5]]], # Wings
            [[(20, 100, 200), white],  [[20, -4], [20, -9]]],   # Wing guns
            [[(20, 100, 200), white],  [[-20, -4], [-20, -9]]], # ^
            [[(20, 100, 200), white],  [[7, 0], [-7, 0], [-4, -18], [4, -18]]], # Cockpit
            [[(20, 100, 200), white],  [[5, 3], [-5, 3], [-2, -15], [2, -15]]], # Cockpit window
            [[(20, 100, 200), white],  [[15, 0], [-15, 0], [-10, 12], [10, 12]]], # Center part
            [[(20, 100, 200), white],  [[-5, 12], [5, 12], [8, 20], [-8, 20]]], # Engine
            [[(20, 100, 200), white],  [[0, -18], [0, -23]]] # Gun
        ]

        self.engine_anchor_poly2 = (0, 20)
        self.engine_colors_poly2 = [(40, 170, 255), white]
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

        self.engine_anchor_poly3 = (0, 20)
        self.engine_colors_poly3 = [(40, 170, 255), (255, 255, 255)]
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
        
        self.switch_model(self.type)

    def update(self, dt):
        self.time += dt
        next_engine_frame = (self.time // self.engine_vfx_timer) % 2
        if next_engine_frame == 0 and self.engine_vfx_current_frame != 0:
            self.engine_vfx_current_frame = 0
            self.current_engine_vfx[0][1] = self.__get_moved_part(self.engine_vfx[0][0], self.current_engine_anchor)
            self.current_engine_vfx[1][1] = self.__get_moved_part(self.engine_vfx[0][1], self.current_engine_anchor)
        elif next_engine_frame == 1 and self.engine_vfx_current_frame != 1:
            self.engine_vfx_current_frame = 1
            self.current_engine_vfx[0][1] = self.__get_moved_part(self.engine_vfx[1][0], self.current_engine_anchor)
            self.current_engine_vfx[1][1] = self.__get_moved_part(self.engine_vfx[1][1], self.current_engine_anchor)

    def switch_model(self, type : ShipType):
        self.type = type
        self.current_parts, self.current_engine_anchor, colors = self.__get_parts(type)
        self.current_engine_vfx = [
            [[colors[0]], []],
            [[colors[1]], []]
        ]

    def draw_rotated(self, screen, position : pygame.Vector2, rotation : int, magnet_radius : int, is_accelerating : bool, timer_invul=0):
        """Used to draw ships during gameplay."""

        if self.current_parts == None:
            return
        
        if self.show_hitbox:   # Draws player hit box in dark red.
            pygame.draw.circle(screen, (50, 50, 100), position, magnet_radius, 2)
            pygame.draw.circle(screen, (100, 50, 50), position, 1, 2)
            pygame.draw.circle(screen, (100, 50, 50), position, self.hitbox_radius, 2)

        # Set opacity based on invulnerability timer
        if timer_invul > 0:
            self.alpha = int(255 - min(timer_invul, PLAYER_TIMER_INVUL) / PLAYER_TIMER_INVUL * 255)

        # Rotate and draw parts
        # Engine animation
        rotated_engine_vfx = self.__rotate_sprite(self.current_engine_vfx, position, rotation)

        if is_accelerating:
            for part in rotated_engine_vfx:
                pygame.gfxdraw.filled_polygon(screen, part[1], (*part[0][0], self.alpha))

        # Ship
        rotated_sprite = self.__rotate_sprite(self.current_parts, position, rotation)

        for part in rotated_sprite:
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

        if self.current_parts == None:
            return

        for part in self.__move_and_scale_sprite(self.current_parts, x, y, multiplier):
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

    
    def __get_parts(self, type) -> tuple[list, tuple, list]:
        """Returns list of parts, tuple(x, y) indicating engine vfx anchor spot, list of engine vfx colors"""

        match type:
            case ShipType.POLY:
                return self.parts_poly, self.engine_anchor_poly, self.engine_colors_poly
            case ShipType.POLY2BP:
                return self.parts_poly2bp, self.engine_anchor_poly2bp, self.engine_colors_poly2bp
            case ShipType.POLY2:
                return self.parts_poly2, self.engine_anchor_poly2, self.engine_colors_poly2
            case ShipType.POLY3:
                return self.parts_poly3, self.engine_anchor_poly3, self.engine_colors_poly3
            case _:
                print(f"Error: Missing `{type}` in ship.__get_parts")
                return None, None, None # pyright: ignore[reportReturnType]

    def __move_and_scale_sprite(self, parts, x, y, multiplier):
        """Returns a moved and scaled copy of the list of parts"""

        new_parts = copy.deepcopy(parts)
        for i in range(len(new_parts)):
            for j in range(len(new_parts[i][1])):
                new_parts[i][1][j] = [new_parts[i][1][j][0]*multiplier+x, new_parts[i][1][j][1]*multiplier+y]
        return new_parts
    
    def __rotate_sprite(self, parts, position : pygame.Vector2, rotation):
        """Returns a rotated copy of the list of parts"""

        rotated_sprite = []
        for part in parts:
            rotated_part = []
            for dot in part[1]:
                dot_rotated = pygame.Vector2(dot).rotate(rotation)
                rotated_part.append((int(position.x + dot_rotated.x), int(position.y + dot_rotated.y)))
            rotated_sprite.append([part[0], rotated_part])
        return rotated_sprite

    def __get_moved_part(self, part : list, move_xy : tuple) -> list:
        moved_part = []
        for dot in part:
            moved_part.append((dot[0]+move_xy[0], dot[1]+move_xy[1]))
        return moved_part