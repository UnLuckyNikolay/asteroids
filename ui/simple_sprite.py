from abc import ABC, abstractmethod

class SimpleSprite():
    def __init__(self, local_x, local_y, color):
        self.x = local_x
        self.y = local_y
        self.color = color
    
    @abstractmethod
    def draw(self, screen, x, y, color_override=None):
        pass
    