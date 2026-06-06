import pygame
from typing import Callable

from ui.menus.base_menu import _MenuBase
from ui.menus.enum_action import Action
from game_state_manager import GameStateManager

import globals as g
from config import PLAYER_MAX_NAME_LENGTH
from ui.colors import *
from ui.elements.container import Container, Allignment
from ui.elements.buttons import Button, ButtonRound, Switch, InfoButton, ModKey, InputButton
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

        self.input_handlers = {
            Action.MENU_CONFIRM : self._check_name_and_return
            Action.MENU_BACK : self._cancel_and_return
        }

        self.old_name = self.gsm.player.stats.name # For cancelling the name edit

        root_x = int(gsm.screen_resolution[0]/2-225)
        root_y = int(gsm.screen_resolution[1]/2-85)
        
        # <> Containers <>

        c_background = Container((root_x, root_y), (450, 170), (10, 25, 10, 25))
        c_background.add_element(
            TextPlain("Edit your name:", fonts.medium, color_white),
            nudge=(15, 7)
        )

        self._containers.extend(
            [c_background]
        )
        
        # <> Buttons <>

        b_name = InputButton(
            (root_x+10, root_y+50), (430, 50), (3, 10, 3, 10),
            lambda: gsm.player.stats.name
            gsm.player.stats.set_player_name,
            max_legth=PLAYER_MAX_NAME_LENGTH
        )
        b_name.add_element(
            TextUpdated(
                "{}", fonts.medium, color_white, 
                lambda: gsm.player.stats.name
            ),
            Allignment.LEFT_WALL,
            nudge=(10, 0)
        )

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
            [b_confirm, b_name]
        )

        g.SET_INPUT_BUTTON(b_name)

    def _check_name_and_return(self):
        if len(gsm.player.stats.name.strip()) > 0:
            g.SWITCH_MENU(Menu.RETURN)

    def _cancel_and_return(self):
        self.gsm.player.stats.name = self.old_name
        g.SWITCH_MENU(Menu.RETURN)
