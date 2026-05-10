import pygame
from typing import Callable

from ui.menus.base_menu import _MenuBase
from ui.menus.enum_action import Action
from game_state_manager import GameStateManager

from constants import PLAYER_MAX_NAME_LENGTH
from ui.colors import *
from ui.elements.container import Container, Allignment
from ui.elements.buttons import Button, ButtonRound, Switch, InfoButton, ModKey
from ui.elements.text import TextPlain, TextUpdated
from ui.font_builder import FontBuilder
from ui.menus.enum_menu import Menu

class MenuNameEdit(_MenuBase):
    def __init__(
        self,
        gsm : GameStateManager,
        fonts : FontBuilder,
        switch_function : Callable[[Menu], None],
    ):
        super().__init__(gsm, switch_function)

        root_x = int(gsm.screen_resolution[0]/2-225)
        root_y = int(gsm.screen_resolution[1]/2-85)
        
        # <> Containers <>

        c_background = Container((root_x, root_y), (450, 170), (10, 25, 10, 25))
        c_background.add_element(
            TextPlain("Edit your name:", fonts.medium, color_white),
            nudge=(15, 7)
        )

        c_name = Container((root_x+10, root_y+50), (430, 50), (3, 10, 3, 10))
        c_name.add_element(
            TextUpdated(
                "{}", fonts.medium, color_white, 
                lambda: gsm.player.stats.name
                ),
                Allignment.LEFT_WALL,
                nudge=(10, 0)

        )

        self._containers.extend(
            [c_background, c_name]
        )
        
        # <> Buttons <>

        b_confirm = Button(
            (root_x+125, root_y+110), (200, 50), (3, 10, 3, 10),
            lambda: switch_function(Menu.RETURN),
            lambda: len(gsm.player.stats.name.strip()) > 0
        )
        b_confirm.add_element(
            TextPlain("Confirm", fonts.medium, color_blue),
            Allignment.CENTER
        )

        self._buttons.extend(
            [b_confirm]
        )

    def check_special_input(self, event : pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.gsm.player.stats.name = self.gsm.player.stats.name[:-1]
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                if len(self.gsm.player.stats.name.strip()) > 0:
                    self.switch_menu(Menu.RETURN)
            else:
                k = event.dict["unicode"]
                if k != "" and len(self.gsm.player.stats.name) < PLAYER_MAX_NAME_LENGTH:
                    self.gsm.player.stats.name = self.gsm.player.stats.name + k
