import pygame
from abc import ABC, abstractmethod


class Weapon(pygame.sprite.Sprite):
    def __init__(self, upgrade_costs):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.__level = 0
        self.__upgrade_costs = upgrade_costs

        
    @abstractmethod
    def attempt_shot(self):
        pass


    def get_upgrade_cost(self):
        if self.__level < len(self.__upgrade_costs):
            return self.__upgrade_costs[self.__level]
        else:
            return None
        

    def get_level(self):
        return self.__level
        

    def upgrade(self):
        if self.__level < len(self.__upgrade_costs):
            self.__level += 1