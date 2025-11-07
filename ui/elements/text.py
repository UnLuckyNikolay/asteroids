import pygame, math
from typing import Callable
from enum import Enum

class TextPlain(pygame.sprite.Sprite):
    """
    Used to place text inside of buttons/containers.
    
    Takes any number of strings and replaces {} with them using .format(). Gets all text during initialization.
    """
    def __init__(
        self, 
        text : str, 
        font : pygame.font.Font, 
        color : tuple[int, int, int, int], 
        *formatting_strings,
        local_pos : tuple[int, int] = (0, 0), 
    ):
        if len(formatting_strings) > 0:
            self._text = text.format(*formatting_strings)
        else:
            self._text = text
        self._position = local_pos
        self._font = font
        self._color = color
        self.lock_color : bool = False

        self._surface : pygame.Surface = self._font.render(self._text, True, self._color)

    def set_color(self, color : tuple[int, int, int, int]):
        if not self.lock_color:
            self._color = color
            self._surface = self._font.render(self._text, True, self._color)

    def prepare_and_return_size(self):
        return self._surface.get_size()
    
    def get_width(self):
        # Used for button descriptions
        return self._surface.get_width()

    def draw(self, screen, position : tuple[int, int]):
        screen.blit(self._surface, (position[0] + self._position[0], position[1] + self._position[1]))

    def get_sprite(self) -> pygame.Surface:
        return self._surface

class TextUpdated(pygame.sprite.Sprite):
    """
    Used to place text inside of buttons/containers.

    Takes any number of getter functions and replaces {} with their return values. Updated before each .draw.
    """
    def __init__(
        self, 
        text : str, 
        font : pygame.font.Font, 
        color : tuple[int, int, int, int], 
        *formatting_getters : Callable,
        local_pos : tuple[int, int] = (0, 0),
    ):
        if hasattr(self, "containers"):
            super().__init__(self.containers) # pyright: ignore[reportAttributeAccessIssue]
        else:
            super().__init__()
        self._text = text
        self._position = local_pos
        self._font = font
        self._color = color
        self.lock_color : bool = False
        self._getters = formatting_getters
        
        self._surface : pygame.Surface

    def set_color(self, color : tuple[int, int, int, int]):
        if not self.lock_color:
            self._color = color

    def prepare_and_return_size(self):
        text = self._text
        for getter in self._getters:
            text = text.replace("{}", str(getter()), 1)
        self._surface = self._font.render(text, True, self._color)
        return self._surface.get_size()

    def draw(self, screen, position : tuple[int, int]):
        screen.blit(self._surface, (position[0] + self._position[0], position[1] + self._position[1]))

    def get_sprite(self) -> pygame.Surface:
        return self._surface

class TextAnimated(TextUpdated):
    """
    Animated version of TextUpdated.
    """

    def __init__(
        self, 
        text : str, 
        font : pygame.font.Font, 
        color : tuple[int, int, int, int], 
        *formatting_getters : Callable,
        local_pos : tuple[int, int] = (0, 0)
    ):
        super().__init__(text, font, color, *formatting_getters, local_pos=local_pos)
        
        self.is_anim_pulse_rotation : bool = False
        self.max_angle : float = 0.0
        self.is_anim_pulse_scale : bool = False
        self.scale_divider : float = 0.0

        self.dt : float = 0.0

    def update(self, dt):
        self.dt += dt

    def activate_animation_pulse_rotation(self, max_angle : float):
        """Continuously rotates text between negative and positive max angle."""

        self.is_anim_pulse_rotation = True
        self.max_angle = max_angle

    def activate_animation_pulse_scale(self, scale_divider : float):
        """Continuously scales text. By default it's +/-100% divided by scale_divider."""

        self.is_anim_pulse_scale = True
        self.scale_divider = scale_divider

    def prepare_and_return_size(self):
        text = self._text
        for getter in self._getters:
            text = text.replace("{}", str(getter()), 1)
        self._surface = self._font.render(text, True, self._color)

        if self.is_anim_pulse_rotation:
            angle = self.max_angle * math.sin(self.dt * 1.5)
            self._surface = pygame.transform.rotate(self._surface, angle)

        if self.is_anim_pulse_scale:
            scale = 1 + math.sin((self.dt + 1.57) * 3) / self.scale_divider
            self._surface = pygame.transform.scale_by(self._surface, scale)

        return self._surface.get_size()
