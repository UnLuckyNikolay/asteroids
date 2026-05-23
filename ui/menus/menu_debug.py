from typing import Callable

from ui.menus.base_menu import _MenuBase
from ui.menus.enum_action import Action
from game_state_manager import GameStateManager

import globals as g
from ui.colors import *
from ui.elements.container import Container, Allignment
from ui.elements.buttons import ButtonBase, Button, ButtonRound, Switch, InfoButton, ModKey
from ui.elements.text import TextPlain, TextUpdated
from ui.font_builder import FontBuilder
from ui.menus.enum_menu import Menu
from ui.elements.simple_sprites.symbols import *
from ui.elements.personal_sprites.getter import get_personal_sprite
from ui.menus.addition_mini_settings import add_mini_settings_and_cheats

class MenuDebug(_MenuBase):
    def __init__(
        self,
        gsm : GameStateManager,
        fonts : FontBuilder,
        switch_function : Callable[[Menu], None],
    ):
        super().__init__(gsm, switch_function)

        self.input_handlers = {
            Action.MENU_SWITCH_DEBUG : self._switch_state,
        }

        self._is_active : bool = False
        
        text_start_y = 8
        text_row_y = 20
        text_nudge_x = 8

        # <> Containers <>

        # Profile
        c_debug = Container(
            (-3, -3), 
            (250, 16+text_row_y*5), 
            (0, 5, 5, 5)
        )
        c_debug.set_outline_color(color_green_hacker)
        c_debug.set_fill_color((20, 20, 20, 200))
        c_debug.add_element(
            TextPlain(
                "Group sizes:", fonts.very_small, color_green_hacker
            ),
            nudge=(text_nudge_x, text_start_y)
        )
        c_debug.add_element(
            TextUpdated(
                "Drawable: {}", fonts.very_small, color_green_hacker,
                lambda: g.GM.drawable.__len__()
            ),
            nudge=(text_nudge_x, text_start_y+text_row_y*1)
        )
        c_debug.add_element(
            TextUpdated(
                "Updatable UI: {}", fonts.very_small, color_green_hacker,
                lambda: g.GM.updatable_ui.__len__()
            ),
            nudge=(text_nudge_x, text_start_y+text_row_y*2)
        )
        c_debug.add_element(
            TextUpdated(
                "Updatable Gameplay: {}", fonts.very_small, color_green_hacker,
                lambda: g.GM.updatable_gameplay.__len__()
            ),
            nudge=(text_nudge_x, text_start_y+text_row_y*3)
        )
        c_debug.add_element(
            TextUpdated(
                "Asteroids: {}", fonts.very_small, color_green_hacker,
                lambda: g.GM.asteroids.__len__()
            ),
            nudge=(text_nudge_x, text_start_y+text_row_y*4)
        )

        self._containers.extend(
            [c_debug]
        )

    def draw(self, screen):
        if self._is_active:
            super().draw(screen)

    def _switch_state(self):
        self._is_active = False if self._is_active else True