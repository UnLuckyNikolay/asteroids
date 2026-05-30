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
from player.ship import Ship
from ui.elements.simple_sprites.symbols import *
from ui.elements.personal_sprites.getter import get_personal_sprite
from ui.menus.addition_mini_settings import add_mini_settings_and_cheats

class MenuMain(_MenuBase):
    def __init__(
        self,
        gsm : GameStateManager,
        fonts : FontBuilder,
        switch_function : Callable[[Menu], None],
    ):
        super().__init__(gsm, switch_function)

        self._containers : list[Container] = []
        self._buttons : list[Button | Switch] = []

        gsm.konami_progress = 0 # Resets Konami sequence

        res = gsm.screen_resolution
        center_x = int((res[0])/2)
        center_y = int((res[1])/2)

        root_x = center_x-475
        root_y = 10
        text_nudge_x = 35
        
        # <> Containers <>
        
        # Profile
        c_profile = Container(
            (root_x, 10), (950, 140), (7, 7, 30, 30)
        )
        c_profile.add_element(
            TextPlain(
                "{}", fonts.big, color_white,
                gsm.player.stats.name
            ),
            nudge=(text_nudge_x+46, 18)
        )
        c_profile.add_element(
            TextPlain(
                "Max Score: {}", fonts.medium, color_white,
                gsm.player.stats.max_score
            ),
            nudge=(text_nudge_x, 77)
        )
        c_profile.add_element(
            Ship(gsm.player.stats.get_current_ship_model(), color_profile=gsm.player.stats.ship_color_profile),
            Allignment.UPPER_RIGHT_CORNER,
            nudge=(-70, 70)
        )
        personal_sprite = get_personal_sprite(gsm.player.stats.name)
        if personal_sprite != None:
            c_profile.add_element(
                personal_sprite(10, -10),
                Allignment.BOTTOM_LEFT_CORNER
            )
        
        self._containers.extend(
            [c_profile]
        )
        
        # <> Buttons <>

        # Profile
        # Rename
        b_rename = Button(
            (root_x+text_nudge_x, root_y+26), (35, 35), (3, 3, 3, 3),
            lambda: self.switch_menu(Menu.NAME_EDIT)
        )
        b_rename.add_element(
            SymbolPencil(0, 0, color_blue),
            Allignment.CENTER
        )
        # Open
        b_open_info = Button(
            (center_x-50, 125), (100, 20), (3, 3, 3, 3),
            lambda: self.switch_menu(Menu.PLAYER_INFO)
        )
        b_open_info.add_element(
            SymbolArrowDown(0, 0, color_blue),
            Allignment.CENTER
        )

        # Main buttons
        # Space between - 28

        amount_of_buttons = 4
        b_offset_y = int((res[1] - (amount_of_buttons*100+28))/2 + 75)

        # Start button, starts a Round
        b_start = Button(
            (center_x-185, b_offset_y+100*0), (370, 72), (8, 8, 20, 20), 
            gsm.start_round
        )
        b_start.add_element(
            TextPlain("Start", fonts.big, color_blue),
            Allignment.CENTER
        )
        # Opens the Leaderboard
        b_leaderboard = Button(
            (center_x-185, b_offset_y+100*1), (370, 72), (8, 8, 20, 20), 
            lambda: self.switch_menu(Menu.LEADERBOARD)
        )
        b_leaderboard.add_element(
            TextPlain("Leaderboard", fonts.big, color_blue),
            Allignment.CENTER
        )
        # Back to profile selection
        b_profiles = Button(
            (center_x-185, b_offset_y+100*2), (370, 72), (8, 8, 20, 20), 
            gsm._return_to_profile_selection
        )
        b_profiles.add_element(
            TextPlain("Profiles", fonts.big, color_blue),
            Allignment.CENTER
        )
        # Exits the game
        b_exit = Button(
            (center_x-185, b_offset_y+100*3), (370, 72), (8, 8, 20, 20), 
            gsm.handler_turn_off
        )
        b_exit.add_element(
            TextPlain("Exit", fonts.big, color_blue),
            Allignment.CENTER
        )

        b_test = Button(
            (center_x-700, b_offset_y+100*0), (370, 72), (8, 8, 20, 20), 
            lambda: switch_function(Menu.SHIP_CONSTRUCTOR)
        )
        b_test.add_element(
            TextPlain("Ship Constructor", fonts.big, color_blue),
            Allignment.CENTER
        )
        
        self._buttons.extend(
            [b_start, b_leaderboard, b_exit, b_profiles, b_open_info,
                b_rename, b_test]
        )

        add_mini_settings_and_cheats(self._containers, self._buttons, gsm, fonts)

    ### Secret stuff

    def check_special_input(self, event : pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            # Cheat visibility
            if event.scancode == self.gsm.konami_sequence[self.gsm.konami_progress]:
                self.gsm.konami_progress += 1
                if self.gsm.konami_progress == 11 and not self.gsm.player.stats.found_cheats:
                    self.gsm.konami_progress = 0
                    self.gsm.unlock_cheats()
            else:
                self.gsm.konami_progress = 0
    