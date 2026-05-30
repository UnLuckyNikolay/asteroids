import pygame
from typing import Callable

import globals as g
from ui.menus.base_menu import _MenuBase
from ui.menus.enum_action import Action
from game_state_manager import GameStateManager

from ui.colors import *
from ui.elements.container import Container, Allignment
from ui.elements.buttons import ButtonBase, Button, ButtonRound, Switch, InfoButton, ModKey
from ui.elements.text import TextPlain, TextUpdated
from ui.font_builder import FontBuilder
from ui.menus.enum_menu import Menu
from ui.elements.simple_sprites.symbols import *
from ui.elements.personal_sprites.getter import get_personal_sprite
from ui.menus.addition_mini_settings import add_mini_settings_and_cheats

class MenuShipContructor(_MenuBase):
    def __init__(
        self,
        gsm : GameStateManager,
        fonts : FontBuilder,
        switch_function : Callable[[Menu], None],
    ):
        super().__init__(gsm, switch_function)

        self.input_handlers = {
        }

        res = gsm.screen_resolution
        bg_width = 800
        bg_height = 500
        offset_x = int((gsm.screen_resolution[0] - bg_width)/2)
        offset_y = int((gsm.screen_resolution[1] - bg_height)/2) + 50
        
        # <> Containers <>

        # Background
        c_background = Container((offset_x, offset_y), (bg_width, bg_height), (20, 20, 8, 15))
        c_background.set_fill_color((75, 75, 100, 150))

        # Ship - BIG
        c_background = Container((offset_x, offset_y), (bg_width, bg_height), (20, 20, 8, 15))
        c_background.set_fill_color((75, 75, 100, 150))

        # Name of the menu
        c_menu_name = Container((int(res[0] / 2 - 250), 35), (500, 72), (8, 8, 20, 20))
        c_menu_name.add_element(
            TextPlain("Ship Constructor", fonts.big, color_white),
            Allignment.CENTER
        )
        
        self._containers.extend(
            [c_menu_name, c_background]
        )
        
        # <> Buttons <>

        # Returns to the Main Menu
        b_back = Button(
            (100, 68), (100, 36), (15, 3, 3, 15), 
            lambda: switch_function(Menu.MAIN_MENU)
        )
        b_back.add_element(
            TextPlain("Back", fonts.small, color_blue),
            Allignment.CENTER
        )
        
        self._buttons.extend(
            [b_back]
        )
