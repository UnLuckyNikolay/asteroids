from typing import Callable
from ui.container import Container
from ui.textf import TextF
from ui.texth import TextH

class Button(Container):
    layer = 100 # pyright: ignore
    def __init__(self,
                 x, y, 
                 width, height,
                 corner_topleft, corner_topright, corner_bottomright, corner_bottomleft, 
                 key_func : Callable, 
                 condition_func : Callable,
                 color,
                 *elements
    ):
        super().__init__(
            x, y, 
            width, height, 
            corner_topleft, corner_topright, corner_bottomright, corner_bottomleft, 
            color,
            *elements
        )
        self.key_func = key_func
        self.condition_func = condition_func
    
    def check_click(self, position):
        if (position[0] > self.x and
            position[0] < self.x + self.width and
            position[1] > self.y and
            position[1] < self.y + self.height):
            return True
        else:
            return False

    def run_if_possible(self):
        if type(self.elements[0]) is TextH or type(self.elements[0]) is TextF:
            print(f"Clicked the `{self.elements[0].text}` button")
        if self.condition_func():
            self.key_func()
