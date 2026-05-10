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
from ui.elements.sprites.healthbar import HealthBar

class MenuHud(_MenuBase):
    def __init__(
        self,
        gsm : GameStateManager,
        fonts : FontBuilder,
        switch_function : Callable[[Menu], None],
    ):
        super().__init__(gsm, switch_function)

        self.input_handlers = {
            Action.MENU_BACK : gsm.pause_game,
            Action.PLAYER_WEAPON_ONE : lambda: gsm.player.switch_weapon(0),
            Action.PLAYER_WEAPON_ONE_ALT : lambda: gsm.player.switch_weapon(0),
            Action.PLAYER_WEAPON_TWO : lambda: gsm.player.switch_weapon(1),
            Action.PLAYER_WEAPON_TWO_ALT : lambda: gsm.player.switch_weapon(1),
            Action.PLAYER_WEAPON_THREE : lambda: gsm.player.switch_weapon(2),
            Action.PLAYER_WEAPON_THREE_ALT : lambda: gsm.player.switch_weapon(2),
        }

        # Space between elements - 10
        
        # <> Containers <>

        # Current weapon
        c_weapon = Container((25, 25), (362, 36), (10, 5, 5, 5))
        c_weapon.add_element(
            TextUpdated(
                "{}.v{}", fonts.small, color_white, 
                gsm.player.get_current_weapon_name,
                gsm.player.get_current_weapon_level
            ),
            Allignment.LEFT_WALL,
            nudge=(9, 0)
        )
        # Timer
        c_timer = Container((397, 25), (176, 36), (5, 10, 5, 5))
        c_timer.add_element(
            TextUpdated(
                "Time: {}", fonts.small, color_white, 
                gsm.rs.get_time_as_text
            ),
            Allignment.LEFT_WALL,
            nudge=(9, 0)
        )
        # Current score
        c_score = Container((25, 71), (176, 36), (5, 3, 5, 10))
        c_score.add_element(
            TextUpdated(
                "{}pts", fonts.small, color_white, 
                lambda: gsm.rs.score
            ),
            Allignment.LEFT_WALL,
            nudge=(9, 0)
        )
        # Current money
        c_money = Container((211, 71), (176, 36), (3, 3, 3, 3))
        c_money.add_element(
            TextUpdated(
                "{}g", fonts.small, color_golden, 
                gsm.player.get_money
            ),
            Allignment.LEFT_WALL,
            nudge=(9, 0)
        )
        # Current health bar
        c_health = Container((397, 71), (176, 36), (3, 5, 10, 5))
        c_health.add_element(
            TextPlain("Lives", fonts.small, color_white),
            Allignment.LEFT_WALL,
            nudge=(9, 0)
        )
        c_health.add_element(
            HealthBar(
                (102, 5), 2, 6,
                gsm.player.get_lives,
                gsm.player.stats.cheat_godmode
            )
        )
        
        self._containers.extend(
            [c_weapon, c_score, c_money, c_health, c_timer]
        )

        # Cheats detected
        if gsm.player.is_sus:
            c_cheats = Container((gsm.screen_resolution[0]-399, gsm.screen_resolution[1]-24), (400, 25), (5, 0, 0, 0))
            c_cheats.add_element(
                TextPlain("Cheats enabled! Score won't be saved.", fonts.very_small, color_white),
                Allignment.CENTER
            )

            self._containers.append(c_cheats)