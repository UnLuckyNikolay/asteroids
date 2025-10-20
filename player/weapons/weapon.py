import pygame
from abc import ABC, abstractmethod


class Weapon(pygame.sprite.Sprite):
    def __init__(self, name):
        if hasattr(self, "containers"):
            super().__init__(self.containers) # pyright: ignore[reportAttributeAccessIssue]
        else:
            super().__init__()
        self._level = 1
        self._name = name

        
    @abstractmethod
    def attempt_shot(self):
        pass


    def get_level(self):
        return self._level
    
    def get_name(self):
        return self._name
    