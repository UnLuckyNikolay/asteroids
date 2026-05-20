import pygame
from abc import ABC, abstractmethod

class SimpleSprite(pygame.sprite.Sprite):
    def __init__(self, local_x, local_y, color):
        if hasattr(self, "containers"):
            super().__init__(self.containers) # pyright: ignore[reportAttributeAccessIssue]
        else:
            super().__init__()
            
        self.x = local_x
        self.y = local_y
        self.color = color
        self.lock_color : bool = False
    
    @abstractmethod
    def draw(self, screen, position : tuple[int, int]):
        pass
    
    def set_color(self, color : tuple[int, int, int, int]):
        if not self.lock_color:
            self.color = color
    