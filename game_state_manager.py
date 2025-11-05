# pyright: reportAttributeAccessIssue=false

import pygame, json, os
from enum import Enum
from typing import Any

from constants import *
from json_helper.leaderboard.validator import ValidateLeaderboard
from json_helper.profile.validator import ValidateProfile

from ui.elements.container import Container
from ui.elements.buttons import ButtonBase, Button, Switch
from ui.elements.sprites.leaderboard import Leaderboard
from ui.font_builder import FontBuilder

from ui.menus.enum import Menu
from ui.menus.addition_mini_settings import add_mini_settings_and_cheats
from ui.menus.menu_profile_selection import initialize_profile_selection
from ui.menus.menu_new_profile import initialize_new_profile
from ui.menus.menu_main import initialize_main_menu
from ui.menus.menu_player_info import initialize_player_info
from ui.menus.menu_name_edit import initialize_name_edit
from ui.menus.menu_leaderboard import initialize_leaderboard
from ui.menus.menu_hud import initialize_hud
from ui.menus.menu_pause import initialize_pause_menu
from ui.menus.menu_round_end import initialize_round_end
from ui.menus.menu_test import initialize_test_menu

from round_state_manager import RoundStateManager
from player.player import Player
from player.player_stats import PlayerStats
from player.ship import Ship, ShipModel


class GameStateManager(pygame.sprite.Sprite):
    layer = 100 # pyright: ignore
    def __init__(self, game):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.game = game
        self.rsm : RoundStateManager = None
        self.player : Player
        self.player_stats : PlayerStats
        self.__containers : list[Container | Leaderboard] = []
        self.__buttons : list[ButtonBase] = []
        self.__hovered_button : Button | Switch | None = None
        self.__current_menu : Menu = Menu.PROFILE_SELECTION # Menu.PROFILE_SELECTION | Menu.TEST_MENU

        # Fonts
        self.__fonts = FontBuilder()
        
        # Checking if ./saves/ folder exists
        self.__saves_folder_path = "./saves/"
        if not os.path.exists(self.__saves_folder_path):
            print(f"Creating a `{self.__saves_folder_path}` folder")
            os.makedirs(self.__saves_folder_path)

        # Getting the scores
        self.__leaderboard_path = f"{self.__saves_folder_path}leaderboard.json"
        self._scores = ValidateLeaderboard(self.__leaderboard_path)

        # Getting profiles
        self.__current_profile : int | None = None
        self.__profile_paths : list[str] = [
            f"{self.__saves_folder_path}profile_0.json",
            f"{self.__saves_folder_path}profile_1.json",
            f"{self.__saves_folder_path}profile_2.json"
        ]
        self._profiles : list[dict[str, Any] | None] = [
            ValidateProfile(self.__profile_paths[0]), 
            ValidateProfile(self.__profile_paths[1]), 
            ValidateProfile(self.__profile_paths[2])
        ]

        # Defaults used for loading save in profile selection if something is missing
        self._default_player_name = "Player"
        self._default_ship_model = ShipModel.HAWK3 # Value of the ShipType Enum

        # Secrets
        self.__konami_sequence : list[int] = [82, 82, 81, 81, 80, 79, 80, 79, 5, 4, 40]
        self._konami_progress : int = 0

    def draw(self, screen):
        for container in self.__containers:
            container.draw(screen)
        
        for button in self.__buttons:
            button.draw(screen)

        if self.__hovered_button != None:
            self.__hovered_button.draw_description(screen, self.game.screen_resolution)
    
    def initialize_current_menu(self):
        run_menu_function = lambda function: function(
            self.game,
            self,
            self.player_stats,
            self.player,
            self.__fonts
        )
        run_menu_function_with_rsm = lambda function: function(
            self.game,
            self,
            self.rsm,
            self.player_stats,
            self.player,
            self.__fonts
        )
        run_addition_function = lambda function: function(
            self.__containers,
            self.__buttons,
            self.game,
            self,
            self.player_stats,
            self.player,
            self.__fonts
        )

        match self.__current_menu:
            case Menu.PROFILE_SELECTION:
                self.__containers, self.__buttons = run_menu_function(initialize_profile_selection)
            case Menu.NEW_PROFILE:
                self.__containers, self.__buttons = run_menu_function(initialize_new_profile)
            case Menu.MAIN_MENU:
                self.__containers, self.__buttons = run_menu_function(initialize_main_menu)
                run_addition_function(add_mini_settings_and_cheats)
            case Menu.PLAYER_INFO:
                self.__containers, self.__buttons = run_menu_function(initialize_player_info)
                run_addition_function(add_mini_settings_and_cheats)
            case Menu.NAME_EDIT:
                self.__containers, self.__buttons = run_menu_function(initialize_name_edit)
            case Menu.LEADERBOARD:
                self.__containers, self.__buttons = run_menu_function(initialize_leaderboard)
            case Menu.HUD:
                self.__containers, self.__buttons = run_menu_function_with_rsm(initialize_hud)
            case Menu.PAUSE_MENU:
                self.__containers, self.__buttons = run_menu_function_with_rsm(initialize_pause_menu)
            case Menu.ROUND_END:
                self.__containers, self.__buttons = run_menu_function_with_rsm(initialize_round_end)
            case Menu.TEST_MENU:
                self.__containers, self.__buttons = run_menu_function(initialize_test_menu)
            case _:
                print(f"> Error: missing menu {self.__current_menu.value} in UserInterface.initialize_current_menu")

    def start_round(self, rsm):
        self.rsm = rsm
        self.switch_menu(Menu.HUD)

    def switch_menu(self, menu : Menu):
        if self.__current_menu == menu:
            return
        
        self.__current_menu = menu
        if self.__hovered_button != None and self.__hovered_button._is_hovered:
            self.__hovered_button.switch_hovered_state()
        self.__hovered_button = None
        self.initialize_current_menu()

    def check_hovered_button(self):
        """Checks mouse position against all the buttons in the current menus and tries to run the button function."""

        position = pygame.mouse.get_pos()

        if self.__hovered_button == None:

            # Check for a button hover
            for i in range(len(self.__buttons)):
                if self.__buttons[i].check_cursor_hover(position):
                    self.__hovered_button = self.__buttons[i]
                    self.__hovered_button.switch_hovered_state() # pyright: ignore[reportOptionalMemberAccess]
                    return
        
        # Check if cursor moved off the button
        elif not self.__hovered_button.check_cursor_hover(position):
            self.__hovered_button.switch_hovered_state()
            self.__hovered_button = None

    def try_button_press(self):
        if self.__hovered_button == None:
            return
        
        self.__hovered_button.run_if_possible()

    ### Saving

    def save_profile(self):
        if self.__current_profile == None: # In case game is exited before profile is chosen
            return

        path = self.__profile_paths[self.__current_profile]
        save = {
            "version" : 1,
            "player_stats_save" : self.player_stats.get_save()
        }
        print(f"Saving current profile to `{path}`")
        with open(path, "w") as file:
            json.dump(save, file)

    def _load_profile(self, number):
        self.__current_profile = number
        profile = self._profiles[number]

        if profile["version"] >= 1:
            self.player_stats.load_save(profile["player_stats_save"])

        self.switch_menu(Menu.MAIN_MENU)

    def _new_profile(self, number):
        self.switch_menu(Menu.NEW_PROFILE)
        self.__current_profile = number
        if self.game.get_player_name():
            self.switch_menu(Menu.MAIN_MENU)
        else:
            self.__current_profile = None # In case game is exited while creating a new profile

    def _delete_profile(self, number):
        try:
            os.remove(self.__profile_paths[number])
            print(f"Removed file `{self.__profile_paths[number]}`")
            self._profiles[number] = None
        except Exception as e:
            print(f"Error removing file `{self.__profile_paths[number]}`: {e}")
        self.initialize_current_menu()

    def _rename_player(self, starting_menu : Menu):
        self.switch_menu(Menu.NAME_EDIT)
        if self.game.get_player_name():
            self.switch_menu(starting_menu)
        elif self.player_stats.name == "":
            self.player_stats.name = "Player"

    def _return_to_profile_selection(self):
        """Used to return from the Main Menu back to the Profile Selection."""

        if self.__current_profile != None:
            self.save_profile()
            self._profiles[self.__current_profile] = ValidateProfile(self.__profile_paths[self.__current_profile])
        self.__current_profile = None
        self.game.initialize_new_player()
        self.switch_menu(Menu.PROFILE_SELECTION)

    def check_score(self, new_score) -> tuple[bool, int]:
        """
        Returns (True, place : int) if new leaderboard record is set.
        
        Otherwise (False, 0).
        """

        is_updated = False

        # Overfilled
        while len(self._scores) > LEADERBOARD_LENGTH:   # Shortens leaderboard if max length was reduced
            is_updated = True
            self._scores.pop()

        # Empty
        if len(self._scores) == 0:
            self._scores.append({"name": self.player_stats.name, "score": new_score})
            self.__save_leaderboard()
            return True, 1

        # Full/Partially filled
        for i in range(len(self._scores)):
            if new_score > self._scores[i]["score"]:
                if len(self._scores) == LEADERBOARD_LENGTH:
                    self._scores.pop()
                self._scores.append({"name": self.player_stats.name, "score": new_score})
                self._scores.sort(key=lambda x: x["score"], reverse=True)
                self.__save_leaderboard()
                return True, i+1
            
        # New lowest :sadge:
        if len(self._scores) < LEADERBOARD_LENGTH:
                self._scores.append({"name": self.player_stats.name, "score": new_score})
                self.__save_leaderboard()
                return True, len(self._scores)
            
        # No new record
        if is_updated: # In case was overfilled
            self.__save_leaderboard()
        return False, 0

    def _reset_leaderboard(self):
        self._scores = []
        self.__save_leaderboard()
        self.__initialize_leaderboard()

    def __save_leaderboard(self):
        print(f"Saving leaderboard to `{self.__leaderboard_path}`")
        with open(self.__leaderboard_path, "w") as file:
            json.dump(self._scores, file)

    ### Secret stuff

    def handle_event_for_secrets(self, event : pygame.event.Event):
        match self.__current_menu:
            case Menu.MAIN_MENU:
                if event.type == pygame.KEYDOWN:
                    # Cheat visibility
                    if event.scancode == self.__konami_sequence[self._konami_progress]:
                        self._konami_progress += 1
                        if self._konami_progress == 11:
                            self._konami_progress = 0
                            self.player_stats.found_cheats = True
                            self.initialize_current_menu()
                    else:
                        self._konami_progress = 0

    def unlock_ship(self, ship_type : ShipModel):
        self.player_stats.unlock_ship(ship_type)
        self.initialize_current_menu()
