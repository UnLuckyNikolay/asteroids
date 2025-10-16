import pygame, pygame.gfxdraw, copy
from enum import Enum

from constants import *


class ShipType(Enum):
    POLY = "Poly.v1"
    POLY2BP = "Poly.v2:Bp"
    POLY2 = "Poly.v2"
    POLY3 = "Poly.v3"
    UFO = "UFO.v1"

class Ship():
    def __init__(self, type : ShipType, hitbox_radius, show_hitbox):
        self.type = type
        self.time = 0
        self.current_parts : list[PartPolygon | PartCircle | PartEngineVfx]
        self.alpha = 255

        self.show_hitbox = show_hitbox
        self.hitbox_radius = hitbox_radius

        # Engine animation
        self.engine_vfx_timer = 0.2 # Duration of a frame in sec
        self.engine_vfx_current_frame : int = 0

        # Colors for parts
        white = (255, 255, 255)
        gray_light = (150, 150, 170)
        gray_mid = (119, 119, 132)
        gray_dark = (90, 90, 103)
        gray_very_dark = (45, 45, 45)
        black = (0, 0, 0)

        glass_light = (90, 120, 150)
        glass_mid = (72, 100, 128)
        glass_dark = (50, 73, 96)

        energy_blue = (40, 170, 255)
        energy_green = (40, 255, 50)

        blue_bp = (20, 100, 200)

        # Ships
        # Order of parts determines the order of drawing
        self.parts_poly = [
            PartEngineVfx((0, 15), black, white),
            PartPolygon([(0, -20), (-10, 15), (10, 15)], black, white),
        ]

        self.parts_poly2bp = [
            PartEngineVfx((0, 20), blue_bp, white),

            PartPolygon([(0, -18), (0, -23)], white), # Guns
            PartPolygon([(20, -4), (20, -9)], white),
            PartPolygon([(-20, -4), (-20, -9)], white),

            PartPolygon([(-25, -4), (25, -4), (22, 5), (0, 11), (-22, 5)], blue_bp, white), # Wings
            PartPolygon([(7, 0), (-7, 0), (-4, -18), (4, -18)], blue_bp, white), # Cockpit
            PartPolygon([(5, 3), (-5, 3), (-2, -15), (2, -15)], blue_bp, white), # Cockpit window
            PartPolygon([(15, 0), (-15, 0), (-10, 12), (10, 12)], blue_bp, white), # Center part
            PartPolygon([(-5, 12), (5, 12), (8, 20), (-8, 20)], blue_bp, white), # Engine
        ]

        self.parts_poly2 = [
            PartEngineVfx((0, 20), white, energy_blue),

            PartPolygon([(0, -18), (0, -23)], gray_dark), # Guns
            PartPolygon([(20, -4), (20, -9)], gray_dark),
            PartPolygon([(-20, -4), (-20, -9)], gray_dark),

            PartPolygon([(-25, -4), (25, -4), (22, 5), (0, 11), (-22, 5)], gray_light, gray_dark), # Wings
            PartPolygon([(7, 0), (-7, 0), (-4, -18), (4, -18)], gray_light, gray_dark), # Cockpit
            PartPolygon([(5, 3), (-5, 3), (-2, -15), (2, -15)], glass_light), # Cockpit window
            PartPolygon([(15, 0), (-15, 0), (-10, 12), (10, 12)], gray_light, gray_dark), # Center part
            PartPolygon([(-5, 12), (5, 12), (8, 20), (-8, 20)], gray_light, gray_dark), # Engine
        ]

        self.parts_poly3 = [
            PartEngineVfx((0, 20), white, energy_blue),

            PartPolygon([(20, -4), (20, -9)], gray_dark), # Guns
            PartPolygon([(-20, -4), (-20, -9)], gray_dark),
            PartPolygon([(0, -18), (0, -23)], gray_dark),

            PartPolygon([(-25, -4), (0, -8), (25, -4), (29, 7), (22, 3), (-22, 3), (-29, 7)], gray_light), # Wings
            PartPolygon([(-23, 1), (23, 1), (29, 7), (22, 3), (-22, 3), (-29, 7)], gray_mid),
            PartPolygon([(4, -18), (-4, -18), (-7, 0), (-11, 3), 
                         (-5, 12), (-8, 20), (8, 20), (5, 12), (11, 3), (7, 0)], gray_dark), # Body
            PartPolygon([(4, -18), (-4, -18), (-2, -16), (-5, 1), (-6, 3), 
                         (-4, 12), (-6, 20), (6, 20), (4, 12), (6, 3), (5, 1), (2, -16)], gray_mid),
            PartPolygon([(-1, -15), (-3, 3), (-2, 12), (-3, 20), (3, 20), (2, 12), (3, 3), (1, -15)], gray_light),

            PartPolygon([(-2, -16), (-5, 1), (-3, 3), (3, 3), (5, 1), (2, -16)], glass_dark), # Window
            PartPolygon([(-2, -16), (-1, -15), (1, -15), (2, -16)], glass_mid),
            PartPolygon([(-1, -15), (1, -15), (3, 3), (0, 4), (-3, 3)], glass_light),
        ]

        self.parts_ufo = [
            PartEngineVfx((8, 21), white, energy_green),
            PartEngineVfx((-8, 21), white, energy_green),

            PartCircle((0, 0), 22, gray_mid),
            PartCircle((0, 0), 19, energy_green),
            PartCircle((0, 0), 18, gray_mid),
            PartCircle((0, 0), 16, gray_light),
            PartCircle((0, 0), 10, gray_mid),
            PartCircle((0, 0), 8, energy_blue),
            PartPolygon([(-7, 7), (-7, 6), (-1, 0), (-7, -6), (-6, -7), (0, -1), (6, -7), (7, -6), (1, 0), (7, 6), (7, 7), (0, 9)], gray_mid),
            #PartPolygon([(3, 0), (2, 2), (0, 3), (-2, 2), (-3, 0), (-2, -2), (0, -3), (2, -2)], gray_dark),
            PartCircle((0, 0), 5, gray_mid),
            PartCircle((0, 0), 3, gray_light),
        ]
        
        self.switch_model(self.type)

    def update(self, dt):
        self.time += dt
        next_engine_frame = (self.time // self.engine_vfx_timer) % 2
        if next_engine_frame == 0 and self.engine_vfx_current_frame != 0: # REWRITE THIS
            self.engine_vfx_current_frame = 0
        elif next_engine_frame == 1 and self.engine_vfx_current_frame != 1:
            self.engine_vfx_current_frame = 1

    def switch_model(self, type : ShipType):
        self.type = type
        self.current_parts = self.__get_parts(type)

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

        # Draw parts
        for part in self.current_parts:
            part.draw_rotated(screen, position, rotation, self.alpha, is_accelerating, self.engine_vfx_current_frame)

    def draw(self, screen, x, y, multiplier=2):
        """Used to draw ships in menus."""

        for part in self.current_parts:
            part.draw_scaled(screen, x, y, multiplier)

    
    def __get_parts(self, type) -> list:
        """Returns list of parts, tuple(x, y) indicating engine vfx anchor spot, list of engine vfx colors."""

        match type:
            case ShipType.POLY:
                return self.parts_poly
            case ShipType.POLY2BP:
                return self.parts_poly2bp
            case ShipType.POLY2:
                return self.parts_poly2
            case ShipType.POLY3:
                return self.parts_poly3
            case ShipType.UFO:
                return self.parts_ufo
            case _:
                print(f"> Error: Missing `{type}` in ship.__get_parts")
                return None, None, None # pyright: ignore[reportReturnType]


class PartPolygon():
    def __init__(self, 
                    dots : list[tuple[int, int]],
                    color_fill : tuple[int, int, int],
                    color_outline : tuple[int, int, int] | None = None
    ):
        """
        Outline is optional and is not affected by alpha.
        
        Having 2 dots makes a line with a fill color, outline is ignored.
        """

        self.dots = dots
        self.color_fill = color_fill
        self.color_outline = color_outline

    def draw_rotated(self, screen, position : pygame.Vector2, rotation : int, alpha : int, is_accelerating : bool, current_frame):
        dots = rotate_part(self.dots, position, rotation)

        if len(dots) == 2:
            pygame.draw.line(screen, (*self.color_fill, alpha), dots[0], dots[1], 2)
        else:
            pygame.gfxdraw.filled_polygon(screen, dots, (*self.color_fill, alpha))
            if self.color_outline != None:
                pygame.draw.polygon(screen, (*self.color_outline, alpha), dots, 2)
        
    def draw_scaled(self, screen, x, y, multiplier):
        dots = move_and_scale_part(self.dots, (x, y), multiplier)

        if len(dots) == 2:
            pygame.draw.line(screen, self.color_fill, dots[0], dots[1], 2)
        else:
            pygame.gfxdraw.filled_polygon(screen, dots, self.color_fill)
            if self.color_outline != None:
                pygame.draw.polygon(screen, self.color_outline, dots, 2)


class PartCircle():
    def __init__(self, 
                    center : tuple[int, int],
                    radius : int,
                    color_fill : tuple[int, int, int]
    ):
        self.center = center
        self.radius = radius
        self.color_fill = color_fill

    def draw_rotated(self, screen, position : pygame.Vector2, rotation : int, alpha : int, is_accelerating : bool, current_frame):
        pygame.gfxdraw.filled_circle(screen, int(self.center[0]+position[0]), int(self.center[1]+position[1]), self.radius, (*self.color_fill, alpha))
        
    def draw_scaled(self, screen, x, y, multiplier):
        pygame.gfxdraw.filled_circle(screen, int(self.center[0]+x), int(self.center[1]+y), self.radius*multiplier, self.color_fill)


class PartEngineVfx():
    def __init__(self, 
                    anchor : tuple[int, int],
                    color_fill : tuple[int, int, int],
                    color_outline : tuple[int, int, int] | None = None
    ):
        self.color_fill = color_fill
        self.color_outline = color_outline

        self.dots_all = [[[(-6, -2), (-6, 0), (-5, 4), (-4, 6), (-3, 7), (0, 8), (3, 7), (4, 6), (5, 4), (6, 0), (6, -2)], # frame 1
                          [(-4, -2), (-4, 0), (-3, 4), (-2, 6), (-1, 7), (0, 6), (1, 7), (2, 6), (3, 4), (4, 0), (4, -2)]],
                         [[(-5, -2), (-5, 0), (-4, 3), (-3, 5), (-2, 6), (0, 7), (2, 6), (3, 5), (4, 3), (5, 0), (5, -2)], # frame 2
                          [(-3, -2), (-3, 0), (-2, 3), (-1, 5), (0, 6), (1, 5), (2, 3), (3, 0), (3, -2)]]]
        for i in range(len(self.dots_all)):
            for j in range(len(self.dots_all[i])):
                self.dots_all[i][j] = get_moved_part(self.dots_all[i][j], anchor)

    def draw_rotated(self, screen, position : pygame.Vector2, rotation : int, alpha : int, is_accelerating : bool, current_frame):
        if not is_accelerating:
            return
    
        dots_outer = rotate_part(self.dots_all[current_frame][0], position, rotation)
        dots_inner = rotate_part(self.dots_all[current_frame][1], position, rotation)

        if self.color_outline != None:
            pygame.gfxdraw.filled_polygon(screen, dots_outer, (*self.color_outline, alpha))
        pygame.gfxdraw.filled_polygon(screen, dots_inner, (*self.color_fill, alpha))
        
    def draw_scaled(self, screen, x, y, multiplier):
        return # Engine VFX isn't drawn in menus
    

def rotate_part(part : list[tuple[int, int]], position : pygame.Vector2, rotation : float):
    """Returns a rotated copy of a part."""

    rotated_part = []
    for dot in part:
        dot_rotated = pygame.Vector2(dot).rotate(rotation)
        rotated_part.append((int(position.x + dot_rotated.x), int(position.y + dot_rotated.y)))
    return rotated_part

def move_and_scale_part(part, move_xy : tuple[int, int], multiplier : int):
    """Returns a moved and scaled copy of a part."""

    new_part = []
    for dot in part:
        new_part.append((dot[0]*multiplier+move_xy[0], dot[1]*multiplier+move_xy[1]))
    return new_part

def get_moved_part(part : list[tuple[int, int]], move_xy : tuple[int, int]) -> list:
    moved_part = []
    for dot in part:
        moved_part.append((dot[0]+move_xy[0], dot[1]+move_xy[1]))
    return moved_part
