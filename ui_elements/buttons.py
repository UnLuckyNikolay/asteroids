import pygame, pygame.gfxdraw
from typing import Callable
from enum import Enum

from ui_elements.container import Container, Allignment
from ui_elements.text import TextPlain
from ui_elements.helpers import get_points, draw_polygon


class ModKey(Enum):
    SHIFT = "Shift"
    CTRL = "Ctrl"
    ALT = "Alt"

class _ButtonBase(Container):
    def __init__(
            self,
            position : tuple[int, int], 
            size : tuple[int, int], 
            corners : tuple[int, int, int, int],
    ):
        super().__init__(
            position, 
            size,
            corners,
        )
        self._is_hovered = False
        self._description : TextPlain | None = None
        self._mod_key : int | None = None

    def make_weighted(self, mod_key : ModKey):
        """Makes the button pressable only if the modifier keyboard button is held."""

        match mod_key:
            case ModKey.SHIFT:
                self._mod_key = pygame.KMOD_SHIFT
            case ModKey.CTRL:
                self._mod_key = pygame.KMOD_CTRL
            case ModKey.ALT:
                self._mod_key = pygame.KMOD_ALT
        
    def switch_hovered_state(self):
        self._is_hovered = False if self._is_hovered else True

    def check_cursor_hover(self, position):
        return (
            position[0] > self._position[0] and
            position[0] < self._position[0] + self._size[0] and
            position[1] > self._position[1] and
            position[1] < self._position[1] + self._size[1]
        )

    def draw_description(self, screen, screen_res : tuple[int, int]):
        if self._description == None:
            return
        
        cursor_position = pygame.mouse.get_pos()
        width = self._description.get_width()
        if screen_res[0]-cursor_position[0]-30 < width:
            draw_polygon(screen, (cursor_position[0]-14-width, cursor_position[1]-25), (width+6, 17), (0, 4, 0, 4), (50, 50, 50, 200))
            pygame.draw.aalines(
                screen, (240, 240, 240, 255), False, 
                [cursor_position, 
                 (cursor_position[0]-8, cursor_position[1]-8), 
                 (cursor_position[0]-10-width, cursor_position[1]-8), 
                 (cursor_position[0]-14-width, cursor_position[1]-12)]
            )
            self._description.draw(screen, (cursor_position[0]-11-width, cursor_position[1]-25))
        else:
            draw_polygon(screen, (cursor_position[0]+8, cursor_position[1]-25), (width+6, 17), (4, 0, 4, 0), (50, 50, 50, 200))
            pygame.draw.aalines(
                screen, (240, 240, 240, 255), False, 
                [cursor_position, 
                 (cursor_position[0]+8, cursor_position[1]-8), 
                 (cursor_position[0]+10+width, cursor_position[1]-8), 
                 (cursor_position[0]+14+width, cursor_position[1]-12)]
            )
            self._description.draw(screen, (cursor_position[0]+11, cursor_position[1]-25))

    def add_description(self, text : TextPlain):
        self._description = text


class Button(_ButtonBase):
    def __init__(
            self,
            position : tuple[int, int], 
            size : tuple[int, int], 
            corners : tuple[int, int, int, int],
            key_func : Callable[[], None], 
            condition_func : Callable[[], bool] = lambda: True,
    ):
        super().__init__(
            position, 
            size,
            corners,
        )
        self._color_outline_inactive = (100, 100, 100, 255)
        self._color_fill_hover = self._get_divided_color_tuple(self._color_outline, 2, 150)

        self._key_func = key_func
        self._condition_func = condition_func
        self.set_outline_color((100, 200, 255, 255))

    def draw(self, screen):
        is_possible = self._condition_func()
        self._check_element_color(is_possible)
        points = get_points(self._position, self._size, self._corners)
        if self._is_hovered and is_possible:
            pygame.gfxdraw.filled_polygon(screen, points, self._color_fill_hover)
        else:
            pygame.gfxdraw.filled_polygon(screen, points, self._color_fill)
        if is_possible:
            pygame.draw.polygon(screen, self._color_outline, points, 3)
        else:
            pygame.draw.polygon(screen, self._color_outline_inactive, points, 3)

        self._draw_elements(screen)

    def add_element(
            self, 
            element, 
            allignment : Allignment = Allignment.UPPER_LEFT_CORNER,
            nudge : tuple[int, int] = (0, 0),
            color_override_and_lock : tuple[int, int, int, int] | None = None
        ):
        if color_override_and_lock == None and not self._condition_func() and isinstance(element, self._colored_sprites):
            element.set_color(self._color_outline_inactive)
        super().add_element(element, allignment, nudge, color_override_and_lock)

    def run_if_possible(self) -> bool:
        mods = pygame.key.get_mods()
        if (
            (self._mod_key == None or (self._mod_key != None and mods & self._mod_key)) # Check for modifier keys if weighted
            and self._condition_func()
        ):
            self._key_func()
            return True
        return False
    
    def set_outline_color(self, color : tuple[int, int, int, int]):
        """Default value - blue (100, 200, 255, 255)."""

        self._color_outline = color
        self._color_fill_hover = self._get_divided_color_tuple(self._color_outline, 2, 150)

    def set_inactive_outline_color(self, color : tuple[int, int, int, int]):
        """Default value - dark grey (100, 100, 100, 255)"""
        self._color_outline_inactive = color

    def set_hover_fill_color(self, color : tuple[int, int, int, int]):
        self._color_fill_hover = color

    def _check_element_color(self, is_possible : bool):
        if is_possible:
            self._set_element_color(self._color_outline)
        else:
            self._set_element_color(self._color_outline_inactive)


class Switch(_ButtonBase):
    """
    Runs the key functions on press and switches it's state between on/off.

    If is_active is a function that returns boolean - it's ran every time before drawing to recheck if it's still active.
    """

    def __init__(
            self,
            position : tuple[int, int], 
            size : tuple[int, int], 
            corners : tuple[int, int, int, int],
            key_func : Callable[[], None], 
            is_active : bool | Callable[[], bool],
    ):
        super().__init__(
            position, 
            size,
            corners,
        )
        self._color_outline = (100, 200, 255, 255)
        self._color_outline_active = (0, 255, 0, 255)
        self._color_fill_hover_inactive = self._get_divided_color_tuple(self._color_outline, 2, 150)
        self._color_fill_hover_active = self._get_divided_color_tuple(self._color_outline_active, 2, 150)
        
        self._key_func = key_func
        if callable(is_active):
            self._active_func = is_active
            self._is_active = is_active()
        else:
            self._active_func = None
            self._is_active = is_active

    def draw(self, screen):
        if self._active_func != None:
            self._is_active = self._active_func()
        points = get_points(self._position, self._size, self._corners)
        self._check_element_color()
        if self._is_hovered and self._is_active:
            pygame.gfxdraw.filled_polygon(screen, points, self._color_fill_hover_active)
        elif self._is_hovered and not self._is_active:
            pygame.gfxdraw.filled_polygon(screen, points, self._color_fill_hover_inactive)
        else:
            pygame.gfxdraw.filled_polygon(screen, points, self._color_fill)
        if self._is_active:
            pygame.draw.polygon(screen, self._color_outline_active, points, 3)
        else:
            pygame.draw.polygon(screen, self._color_outline, points, 3)

        self._draw_elements(screen)

    def add_element(
            self, 
            element, 
            allignment : Allignment = Allignment.UPPER_LEFT_CORNER,
            nudge : tuple[int, int] = (0, 0),
            color_override_and_lock : tuple[int, int, int, int] | None = None
        ):
        if color_override_and_lock == None and self._is_active and isinstance(element, self._colored_sprites):
            element.set_color(self._color_outline_active)
        super().add_element(element, allignment, nudge, color_override_and_lock)
    
    def run_if_possible(self) -> bool:
        mods = pygame.key.get_mods()
        if (
            self._mod_key == None or (self._mod_key != None and mods & self._mod_key) # Check for modifier keys if weighted
        ):
            self._key_func()
            self._is_active = False if self._is_active else True
            return True
        return False
    
    def set_outline_color(self, color : tuple[int, int, int, int]):
        """Default value - blue (100, 200, 255, 255)."""
        
        self._color_outline = color
        self._color_fill_hover_inactive = self._get_divided_color_tuple(self._color_outline, 2, 150)

    def set_active_outline_color(self, color : tuple[int, int, int, int]):
        """Default value - green (0, 255, 0, 255)."""

        self._color_outline_active = color
        self._color_fill_hover_active = self._get_divided_color_tuple(self._color_outline_active, 2, 150)

    def _check_element_color(self):
        if self._is_active:
            self._set_element_color(self._color_outline_active)
        else:
            self._set_element_color(self._color_outline)
            

class ButtonRound(Button):
    def __init__(
            self,
            position : tuple[int, int], 
            radius : int, 
            key_func : Callable[[], None], 
            condition_func : Callable[[], bool] = lambda: True,
    ):
        super().__init__(
            position,
            (0, 0),
            (0, 0, 0, 0),
            key_func,
            condition_func
        )
        self._radius = radius

    def check_cursor_hover(self, position):
        return (
            (self._position[0]-position[0])**2 + (self._position[1]-position[1])**2 < self._radius**2
        )
    
    def draw(self, screen):
        is_possible = self._condition_func()
        if self._is_hovered and is_possible:
            pygame.gfxdraw.filled_circle(screen, *self._position, self._radius-2, self._color_fill_hover)
        else:
            pygame.gfxdraw.filled_circle(screen, *self._position, self._radius-2, self._color_fill)
        if is_possible:
            pygame.draw.circle(screen, self._color_outline, self._position, self._radius, 3)
        else:
            pygame.draw.circle(screen, self._color_outline_inactive, self._position, self._radius, 3)

        self._draw_elements(screen)

    def set_corners(self, topleft : int, topright : int, bottomright : int, bottomleft : int):
        """Does nothing for round buttons."""
        return
    