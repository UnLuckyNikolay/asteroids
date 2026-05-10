from typing import Callable

from ui.menus.base_menu import _MenuBase
from ui.menus.enum_action import Action
from game_state_manager import GameStateManager

from ui.colors import *
from ui.elements.container import Container, Allignment
from ui.elements.buttons import Button, ButtonRound, Switch, InfoButton, ModKey
from ui.elements.text import TextPlain, TextUpdated
from ui.font_builder import FontBuilder
from ui.menus.enum_menu import Menu
from player.ship_enums import ShipModel
from ui.elements.sprites.leaderboard import Leaderboard
from sfx_manager import SFX

class MenuLeaderboard(_MenuBase):
    def __init__(
        self,
        gsm : GameStateManager,
        fonts : FontBuilder,
        switch_function : Callable[[Menu], None],
    ):
        super().__init__(gsm, switch_function)

        self._containers : list[Container | Leaderboard] = []
        self._buttons : list[Button | Switch] = []

        res = gsm.screen_resolution
        
        # <> Containers <>

        # Name of the menu
        c_menu_name = Container((int(res[0] / 2 - 185), 35), (370, 72), (8, 8, 20, 20))
        c_menu_name.add_element(
            TextPlain("Leaderboard", fonts.big, color_white),
            Allignment.CENTER
        )
        # List of high __scores
        c_leaderboard = Leaderboard(int(res[0]/2)-540, 145, 
            fonts.medium, gsm._scores
        )
        
        self._containers.extend(
            [c_menu_name, c_leaderboard]
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
        # Reset the leaderboard
        b_reset = Button(
            (res[0]-200, 68), (100, 36), (3, 6, 3, 6), 
            gsm._reset_leaderboard
        )
        b_reset.set_fill_color(color_red_fill)
        b_reset.make_weighted(ModKey.SHIFT)
        b_reset.set_outline_color(color_red)
        b_reset.add_description(
            TextPlain("SHIFT+Click to RESET the leaderboard", fonts.very_small, color_white)
        )
        b_reset.add_element(
            TextPlain("Reset", fonts.small, color_red),
            Allignment.CENTER
        )
        
        self._buttons.extend(
            [b_back, b_reset]
        )

        # UFO secret
        if not gsm.player.stats.check_unlocked_ship(ShipModel.UFO2):
            b_ufo = ButtonRound(
                (res[0]-30, res[1]-20), 6,
                lambda: gsm.unlock_ship(ShipModel.UFO2)
            )
            b_ufo.set_outline_color(color_gray)
            b_ufo.set_fill_color(color_green)
            b_ufo.set_hover_fill_color(color_green)
            b_ufo.add_description(
                TextPlain("Do you want to believe?", fonts.very_small, color_green)
            )
            b_ufo.set_click_success_sfx(SFX.SECRET_UFO)
            b_ufo.set_one_time_usage()
            
            self._buttons.append(b_ufo)