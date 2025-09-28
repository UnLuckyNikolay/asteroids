import pygame
from abc import ABC, abstractmethod


class Weapon(pygame.sprite.Sprite):
    def __init__(self, upgrade_costs, name):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.__level = 1
        self.__upgrade_costs = upgrade_costs
        self.__name = name

        
    @abstractmethod
    def attempt_shot(self):
        pass


    def get_upgrade_cost(self):
        if self.__level < len(self.__upgrade_costs):
            return self.__upgrade_costs[self.__level]
        else:
            return float('inf')
        

    def get_level(self):
        return self.__level
    
    def get_name(self):
        return self.__name
        

    def upgrade(self):
        if self.__level < len(self.__upgrade_costs):
            self.__level += 1