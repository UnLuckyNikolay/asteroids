import pygame
from abc import ABC, abstractmethod


class Weapon(pygame.sprite.Sprite):
    def __init__(self, name, max_level):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.__level = 1
        self.__max_level = max_level
        self.__name = name

        
    @abstractmethod
    def attempt_shot(self):
        pass


    def upgrade(self):
        if self.__level < self.__max_level:
            self.__level += 1

    def get_level(self):
        return self.__level
    
    def get_name(self):
        return self.__name
    