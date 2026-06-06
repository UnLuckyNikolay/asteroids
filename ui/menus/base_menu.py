import pygame
from typing import Callable

from ui.menus.enum_menu import Menu
from ui.menus.enum_action import Action
from game_state_manager import GameStateManager

class _MenuBase:
    def __init__(self, gsm : GameStateManager, function_switch_menu : Callable[[Menu], None]):
        self.gsm = gsm
        self.switch_menu = function_switch_menu

        self._containers = []
        self._buttons = []
        self._hovered_button = None
        self.input_handlers : dict[Action, Callable[[]]] = {}

    def draw(self, screen):
        for container in self._containers:
            container.draw(screen)
        
        for button in self._buttons:
            button.draw(screen)

        if self._hovered_button != None:
            self._hovered_button.draw_description(screen, self.gsm.screen_resolution)

    def kill(self):
        for c in self._containers:
            c.kill()
        for b in self._buttons:
            b.kill()

    def check_special_input(self, input : pygame.event.Event):
        """
        Override this method to add more complicated chains of imputs (for example for cheat sequences).
        """
        pass

    def check_action(self, action : Action):
        try:
            self.input_handlers[action]()
        except KeyError:
            return