# pyright: reportAttributeAccessIssue=false

import pygame, json, os
from enum import Enum
from typing import Any

from constants import *
from json_helper.leaderboard.validator import ValidateLeaderboard
from json_helper.profile.validator import ValidateProfile

from ui_elements.container import Container, Allignment
from ui_elements.buttons import Button, Switch, ModKey, ButtonRound
from ui_elements.text import TextPlain, TextUpdated
from ui_elements.sprites.healthbar import HealthBar
from ui_elements.sprites.leaderboard import Leaderboard
from ui_elements.simple_sprites.symbols import *
from ui_elements.personal_sprites.getter import get_personal_sprite

from round_state_manager import RoundStateManager
from player.player import Player, ShipUpgrade, ShipPart
from player.player_stats import PlayerStats
from player.ship import Ship, ShipType


# New menus should be added to:
# .check_hovered_button 
# .draw (+ new function)
# .initialize_current_menu (+ new function)
class Menu(Enum): # Remember not to name 2 the same ever fucking again
    PROFILE_SELECTION = "Profile selection"
    NEW_PROFILE = "New profile"
    MAIN_MENU = "Main Menu"
    PLAYER_INFO = "Player Info"
    NAME_EDIT = "Name edit"
    LEADERBOARD = "Leaderboard"
    HUD = "HUD"
    PAUSE_MENU = "Pause"
    NAME_CHECK = "Name check" # REDO AFTERWARDS TO ROUND_END
    TEST_MENU = "Test Menu"

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
        self.__hovered_button : Button | Switch | None = None
        self.__current_menu : Menu = Menu.PROFILE_SELECTION # Menu.PROFILE_SELECTION | Menu.TEST_MENU

        # Getting the font
        font_path = "./fonts/anita-semi-square.normaali.ttf" #"../../fonts/anita-semi-square.normaali.ttf"
        print(f"Trying to access file `{font_path}`")
        try:
            with open(font_path, "r"):
                pass
        except FileNotFoundError:
            print("Error: font not found")
            font_path = None
        
        # Checking if ./saves/ folder exists
        self.__saves_folder_path = "./saves/"
        if not os.path.exists(self.__saves_folder_path):
            print(f"Creating a `{self.__saves_folder_path}` folder")
            os.makedirs(self.__saves_folder_path)

        # Getting the scores
        self.__leaderboard_path = f"{self.__saves_folder_path}leaderboard.json"
        self.__scores = ValidateLeaderboard(self.__leaderboard_path)

        # Getting profiles
        self.__current_profile : int | None = None
        self.__profile_paths : list[str] = [
            f"{self.__saves_folder_path}profile_0.json",
            f"{self.__saves_folder_path}profile_1.json",
            f"{self.__saves_folder_path}profile_2.json"
        ]
        self.__profiles : list[dict[str, Any] | None] = [
            ValidateProfile(self.__profile_paths[0]), 
            ValidateProfile(self.__profile_paths[1]), 
            ValidateProfile(self.__profile_paths[2])
        ]

        # Defaults used for loading save in profile selection if something is missing
        self.__default_player_name = "Player"
        self.__default_ship_model_value = 130 # Value of the ShipType Enum

        # Fonts
        self.__font_very_small = pygame.font.Font(font_path, 16)
        self.__font_small = pygame.font.Font(font_path, 24)
        self.__font_medium = pygame.font.Font(font_path, 32)
        self.__font_big = pygame.font.Font(font_path, 48)

        # Colors
        self.__color_white = (240, 240, 240, 255)
        """(240, 240, 240, 255)"""
        self.__color_gray = (100, 100, 100, 255)
        """(100, 100, 100, 255)"""
        self.__color_blue = (100, 200, 255, 255)
        """(100, 200, 255, 255)"""
        self.__color_red = (200, 0, 0, 255)
        """(200, 0, 0, 255)"""
        self.__color_red_fill = (100, 0, 0, 75)
        """(100, 0, 0, 75)"""
        self.__color_green = (0, 255, 0, 255)
        """(0, 255, 0, 255)"""
        self.__color_golden = (255, 215, 0, 255)
        """(255, 215, 0, 255)"""

        # Secrets
        self.__konami_sequence : list[int] = [82, 82, 81, 81, 80, 79, 80, 79, 5, 4, 40]
        self.__konami_progress : int = 0

    def start_round(self, rsm):
        self.rsm = rsm
        self.switch_menu(Menu.HUD)

    def switch_menu(self, menu : Menu):
        self.__current_menu = menu
        if self.__hovered_button != None and self.__hovered_button._is_hovered:
            self.__hovered_button.switch_hovered_state()
        self.__hovered_button = None
        self.initialize_current_menu()

    def check_hovered_button(self):
        """Checks mouse position against all the buttons in the current menus and tries to run the button function."""

        position = pygame.mouse.get_pos()

        if self.__hovered_button == None:

            # Getting button list
            match self.__current_menu:
                case Menu.PROFILE_SELECTION:
                    button_list = self.__buttons_profile_selection
                case Menu.NEW_PROFILE:
                    button_list = self.__buttons_new_profile
                case Menu.MAIN_MENU:
                    button_list = self.__buttons_main_menu
                case Menu.PLAYER_INFO:
                    button_list = self.__buttons_player_info
                case Menu.NAME_EDIT:
                    button_list = self.__buttons_name_edit
                case Menu.LEADERBOARD:
                    button_list = self.__buttons_leaderboard
                case Menu.HUD:
                    return # No buttons currently planned for HUD
                case Menu.PAUSE_MENU:
                    button_list = self.__buttons_pause_menu
                case Menu.NAME_CHECK:
                    button_list = self.__buttons_name_check
                case Menu.TEST_MENU:
                    button_list = self.__buttons_test_menu
                case _:
                    print(f"Error: menu `{self.__current_menu.value}` missing in userinterface.check_hovered_button")

            # Check for a button hover
            for i in range(len(button_list)):
                if button_list[i].check_cursor_hover(position):
                    self.__hovered_button = button_list[i]
                    self.__hovered_button.switch_hovered_state()
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

    def __load_profile(self, number):
        self.__current_profile = number
        profile = self.__profiles[number]

        if profile["version"] >= 1:
            self.player_stats.load_save(profile["player_stats_save"])

        self.switch_menu(Menu.MAIN_MENU)

    def __new_profile(self, number):
        self.switch_menu(Menu.NEW_PROFILE)
        self.__current_profile = number
        if self.game.get_player_name():
            self.switch_menu(Menu.MAIN_MENU)
        else:
            self.__current_profile = None # In case game is exited while creating a new profile

    def __delete_profile(self, number):
        try:
            os.remove(self.__profile_paths[number])
            print(f"Removed file `{self.__profile_paths[number]}`")
            self.__profiles[number] = None
        except Exception as e:
            print(f"Error removing file `{self.__profile_paths[number]}`: {e}")
        self.initialize_current_menu()

    def __rename_player(self, starting_menu : Menu):
        self.switch_menu(Menu.NAME_EDIT)
        if self.game.get_player_name():
            self.switch_menu(starting_menu)
        elif self.player_stats.name == "":
            self.player_stats.name = "Player"

    def __return_to_profile_selection(self):
        """Used to return from the Main Menu back to the Profile Selection."""

        if self.__current_profile != None:
            self.save_profile()
            self.__profiles[self.__current_profile] = ValidateProfile(self.__profile_paths[self.__current_profile])
        self.__current_profile = None
        self.game.initialize_new_player()
        self.switch_menu(Menu.PROFILE_SELECTION)

    def check_score(self, new_score) -> tuple[bool, int]:
        """
        Returns (True, place : int) if new leaderboard record is set.
        
        Otherwise (False, 0).
        """

        is_updated = False

        while len(self.__scores) > LEADERBOARD_LENGTH:   # Shortens leaderboard if max length was reduced
            is_updated = True
            self.__scores.pop()

        for i in range(len(self.__scores)):
            if new_score > self.__scores[i]["score"]:
                if len(self.__scores) == LEADERBOARD_LENGTH:
                    self.__scores.pop()
                self.__scores.append({"name": self.player_stats.name, "score": new_score})
                self.__scores.sort(key=lambda x: x["score"], reverse=True)
                self.__save_leaderboard()
                return True, i
            
        return False, 0

    def __reset_leaderboard(self):
        self.__scores = []
        self.__save_leaderboard()
        self.__initialize_leaderboard()

    def __save_leaderboard(self):
        print(f"Saving leaderboard to `{self.__leaderboard_path}`")
        with open(self.__leaderboard_path, "w") as file:
            json.dump(self.__scores, file)

    ### Drawing menus

    def draw(self, screen):
        match self.__current_menu:
            case Menu.PROFILE_SELECTION:
                self.__draw_profile_selection(screen)
            case Menu.NEW_PROFILE:
                self.__draw_new_profile(screen)
            case Menu.MAIN_MENU:
                self.__draw_main_menu(screen)
            case Menu.PLAYER_INFO:
                self.__draw_player_info(screen)
            case Menu.NAME_EDIT:
                self.__draw_name_edit(screen)
            case Menu.LEADERBOARD:
                self.__draw_leaderboard(screen)
            case Menu.HUD:
                self.__draw_hud(screen)
            case Menu.PAUSE_MENU:
                self.__draw_pause_menu(screen)
            case Menu.NAME_CHECK:
                self.__draw_name_check(screen)
            case Menu.TEST_MENU:
                self.__draw_test_menu(screen)
            case _:
                print(f"> Error: missing menu {self.__current_menu.value} in UserInterface.draw")

        if self.__hovered_button != None:
            self.__hovered_button.draw_description(screen, self.game.screen_resolution)

    def __draw_profile_selection(self, screen):
        for container in self.__containers_profile_selection:
            container.draw(screen)
        
        for button in self.__buttons_profile_selection:
            button.draw(screen)

    def __draw_new_profile(self, screen):
        for container in self.__containers_new_profile:
            container.draw(screen)
        
        for button in self.__buttons_new_profile:
            button.draw(screen)

    def __draw_main_menu(self, screen):
        for container in self.__containers_main_menu:
            container.draw(screen)
        
        for button in self.__buttons_main_menu:
            button.draw(screen)

    def __draw_player_info(self, screen):
        for container in self.__containers_player_info:
            container.draw(screen)
        
        for button in self.__buttons_player_info:
            button.draw(screen)

    def __draw_name_edit(self, screen):
        for container in self.__containers_name_edit:
            container.draw(screen)
        
        for button in self.__buttons_name_edit:
            button.draw(screen)

    def __draw_leaderboard(self, screen):
        for container in self.__containers_leaderboard:
            container.draw(screen)

        for button in self.__buttons_leaderboard:
            button.draw(screen)
            
    def __draw_hud(self, screen):
        for container in self.__containers_hud:
            container.draw(screen)

    def __draw_pause_menu(self, screen):
        for container in self.__containers_pause_menu:
            container.draw(screen)

        for button in self.__buttons_pause_menu:
            button.draw(screen)

    def __draw_name_check(self, screen):
        for container in self.__containers_name_check:
            container.draw(screen)

        for button in self.__buttons_name_check:
            button.draw(screen)

    def __draw_test_menu(self, screen):
        for container in self.__containers_test_menu:
            container.draw(screen)

        for button in self.__buttons_test_menu:
            button.draw(screen)

    ### Buttons and containers
    # Remember to add new buttons and containers to the lists to draw them
    
    def initialize_current_menu(self):
        match self.__current_menu:
            case Menu.PROFILE_SELECTION:
                self.__initialize_profile_selection()
            case Menu.NEW_PROFILE:
                self.__initialize_new_profile()
            case Menu.MAIN_MENU:
                self.__initialize_main_menu()
            case Menu.PLAYER_INFO:
                self.__initialize_player_info()
            case Menu.NAME_EDIT:
                self.__initialize_name_edit()
            case Menu.LEADERBOARD:
                self.__initialize_leaderboard()
            case Menu.HUD:
                self.__initialize_hud()
            case Menu.PAUSE_MENU:
                self.__initialize_pause_menu()
            case Menu.NAME_CHECK:
                self.__initialize_name_check()
            case Menu.TEST_MENU:
                self.__initialize_test_menu()
            case _:
                print(f"> Error: missing menu {self.__current_menu.value} in UserInterface.initialize_current_menu")

    def __add_mini_settings_and_cheats(self, container_list : list, button_list : list):
        """Adds some options and cheats (if found at the buttom part of the screen)."""

        res = self.game.screen_resolution
        
        # <> Containers <>        

        # # Settings
        c_settings = Container((10, res[1]-80), (90, 20), (8, 2, 8, 2))
        c_settings.add_element(
            TextPlain("Settings", self.__font_very_small, self.__color_white),
            Allignment.CENTER
        )

        if self.player_stats.found_cheats:
            # Cheats
            c_cheats = Container((res[0]-100, res[1]-80), (90, 20), (2, 8, 2, 8))
            c_cheats.add_element(
                TextPlain("Cheats", self.__font_very_small, self.__color_white),
                Allignment.CENTER
            )
            
            container_list.extend(
                [c_cheats]
            )

        container_list.extend(
            [c_settings]
        )
        
        # <> Buttons <>
        
        # Regenerate background
        b_background = Button(
            (10, self.game.screen_resolution[1]-50), (40, 40), (8, 8, 8, 8),
            self.game.handler_regenerate_background
        )
        b_background.add_description(
            TextPlain("Generate new background", self.__font_very_small, self.__color_white)
        )
        b_background.add_element(
            TextPlain("BG", self.__font_small, self.__color_blue),
            Allignment.CENTER
        )
        # Switch Fullscreen
        s_fullscreen = Switch(
            (60, self.game.screen_resolution[1]-50), (40, 40), (8, 8, 8, 8),
            self.game.switch_fullscreen,
            self.game.is_fullscreen
        )
        s_fullscreen.add_description(
            TextPlain("Switch the FULLSCREEN mode on/off", self.__font_very_small, self.__color_white)
        )
        s_fullscreen.add_element(
            SymbolFullscreen(0, 0, self.__color_blue), 
            Allignment.CENTER
        )
        # Low FPS
        s_slow = Switch(
            (110, self.game.screen_resolution[1]-50), (40, 40), (8, 8, 8, 8),
            self.game.switch_low_fps,
            self.game.is_slow
        )
        s_slow.add_description(
            TextPlain("DEBUG: Switch max FPS between 75 and 10", self.__font_very_small, self.__color_white)
        )
        s_slow.add_element(
            TextPlain("SL", self.__font_small, self.__color_blue),
            Allignment.CENTER
        )

        if self.player_stats.found_cheats:
            # Cheat - Show hitbox
            s_hitbox = Switch(
                (self.game.screen_resolution[0]-150, self.game.screen_resolution[1]-50), (40, 40), (8, 8, 8, 8),
                self.player_stats.switch_hitbox,
                self.player_stats.cheat_hitbox
            )
            s_hitbox.add_description(
                TextPlain("Switch the HITBOX cheat on/off", self.__font_very_small, self.__color_white)
            )
            s_hitbox.set_active_outline_color(self.__color_golden)
            s_hitbox.add_element(
                TextPlain("HB", self.__font_small, self.__color_blue),
                Allignment.CENTER
            )
            s_hitbox.set_active_outline_color = self.__color_golden
            # Cheat - Money cheat
            s_money = Switch(
                (self.game.screen_resolution[0]-100, self.game.screen_resolution[1]-50), (40, 40), (8, 8, 8, 8),
                self.player_stats.switch_stonks,
                self.player_stats.cheat_stonks
            )
            s_money.add_description(
                TextPlain("Switch the STONKS cheat on/off", self.__font_very_small, self.__color_white)
            )
            s_money.set_active_outline_color(self.__color_golden)
            s_money.add_element(
                SymbolStonks(0, 0, self.__color_blue),
                Allignment.CENTER
            )
            s_money.set_active_outline_color = self.__color_golden
            # Cheat - Godmode
            s_godmode = Switch(
                (self.game.screen_resolution[0]-50, self.game.screen_resolution[1]-50), (40, 40), (8, 8, 8, 8),
                self.player_stats.switch_godmode,
                self.player_stats.cheat_godmode
            )
            s_godmode.add_description(
                TextPlain("Switch the GODMODE cheat on/off", self.__font_very_small, self.__color_white)
            )
            s_godmode.set_active_outline_color(self.__color_golden)
            s_godmode.add_element(
                TextPlain("GM", self.__font_small, self.__color_blue),
                Allignment.CENTER
            )
            s_godmode.set_active_outline_color = self.__color_golden
                
            button_list.extend(
                [s_hitbox, s_money, s_godmode]
            )

        button_list.extend(
            [b_background, s_fullscreen, s_slow]
        )

    def __initialize_profile_selection(self):
        self.__containers_profile_selection : list[Container] = []
        self.__buttons_profile_selection : list[Button | Switch] = []
        
        res = self.game.screen_resolution
        offset_x = res[0]/2-400
        offset_y = res[1]/2-285

        # 30 between elements

        # <> Containers <>

        c_menu_name = Container((offset_x+75, offset_y), (650, 60), (20, 20, 8, 8))
        c_menu_name.add_element(
            TextPlain("Select the Profile", self.__font_big, self.__color_white),
            Allignment.CENTER
        )

        self.__containers_profile_selection.extend(
            [c_menu_name]
        )
        
        # <> Buttons <>

        b_corners = (7, 30, 7, 30)
        # Profile 0
        if self.__profiles[0] != None:
            b_pf0 = Button(
                (offset_x, offset_y+90+170*0), (800, 140), b_corners,
                lambda: self.__load_profile(0)
            )
            b_pf0.add_element(
                TextPlain(
                    "{}", self.__font_big, self.__color_blue,
                    self.__profiles[0]["player_stats_save"].get("name", self.__default_player_name)
                ),
                nudge=(35, 18)
            )
            b_pf0.add_element(
                TextPlain(
                    "Max Score: {}", self.__font_medium, self.__color_white,
                    self.__profiles[0]["player_stats_save"].get("max_score", 0)
                ),
                nudge=(35, 77),
                color_override_and_lock=self.__color_white
            )
            b_pf0.add_element(
                Ship(self.__profiles[0]["player_stats_save"].get("ship_model_value", self.__default_ship_model_value), 0),
                Allignment.UPPER_RIGHT_CORNER,
                nudge=(-70, 70)
            )
            personal_sprite = get_personal_sprite(self.__profiles[0]["player_stats_save"].get("name", self.__default_player_name))
            if personal_sprite != None:
                b_pf0.add_element(
                    personal_sprite(10, -10),
                    Allignment.BOTTOM_LEFT_CORNER
                )
                
            b_pf0_delete = Button(
                (offset_x+830, offset_y+140+170*0), (40, 40), (8, 8, 8, 8),
                lambda: self.__delete_profile(0)
            )
            b_pf0_delete.make_weighted(ModKey.SHIFT)
            b_pf0_delete.set_outline_color(self.__color_red)
            b_pf0_delete.set_fill_color(self.__color_red_fill)
            b_pf0_delete.add_description(
                TextPlain("SHIFT+Click to DELETE the Profile", self.__font_very_small, self.__color_white)
            )
            b_pf0_delete.add_element(
                SymbolCross(0, 0, self.__color_red), 
                Allignment.CENTER
            )

            self.__buttons_profile_selection.extend(
                [b_pf0_delete]
            )
            
        else: # Empty profile
            b_pf0 = Button(
                (offset_x, offset_y+90+170*0), (800, 140), b_corners,
                lambda: self.__new_profile(0)
            )
            b_pf0.add_element(
                TextPlain("Null", self.__font_big, self.__color_blue),
                nudge=(35, 18)
            )

        # Profile 1
        if self.__profiles[1] != None:
            b_pf1 = Button(
                (offset_x, offset_y+90+170*1), (800, 140), b_corners,
                lambda: self.__load_profile(1)
            )
            b_pf1.add_element(
                TextPlain(
                    "{}", self.__font_big, self.__color_blue,
                    self.__profiles[1]["player_stats_save"].get("name", self.__default_player_name)
                ),
                nudge=(35, 18)
            )
            b_pf1.add_element(
                TextPlain(
                    "Max Score: {}", self.__font_medium, self.__color_white,
                    self.__profiles[1]["player_stats_save"].get("max_score", 0)
                ),
                nudge=(35, 77),
                color_override_and_lock=self.__color_white
            )
            b_pf1.add_element(
                Ship(self.__profiles[1]["player_stats_save"].get("ship_model_value", self.__default_ship_model_value), 0),
                Allignment.UPPER_RIGHT_CORNER,
                nudge=(-70, 70)
            )
            personal_sprite = get_personal_sprite(self.__profiles[1]["player_stats_save"].get("name", self.__default_player_name))
            if personal_sprite != None:
                b_pf1.add_element(
                    personal_sprite(10, -10),
                    Allignment.BOTTOM_LEFT_CORNER
                )

            b_pf1_delete = Button(
                (offset_x+830, offset_y+140+170*1), (40, 40), (8, 8, 8, 8),
                lambda: self.__delete_profile(1)
            )
            b_pf1_delete.make_weighted(ModKey.SHIFT)
            b_pf1_delete.set_outline_color(self.__color_red)
            b_pf1_delete.set_fill_color(self.__color_red_fill)
            b_pf1_delete.add_description(
                TextPlain("SHIFT+Click to DELETE the Profile", self.__font_very_small, self.__color_white)
            )
            b_pf1_delete.add_element(
                SymbolCross(0, 0, self.__color_red), 
                Allignment.CENTER
            )

            self.__buttons_profile_selection.extend(
                [b_pf1_delete]
            )

        else: # Empty profile
            b_pf1 = Button(
                (offset_x, offset_y+90+170*1), (800, 140), b_corners,
                lambda: self.__new_profile(1)
            )
            b_pf1.add_element(
                TextPlain("Null", self.__font_big, self.__color_blue),
                nudge=(35, 18)
            )

        # Profile 2
        if self.__profiles[2] != None:
            b_pf2 = Button(
                (offset_x, offset_y+90+170*2), (800, 140), b_corners,
                lambda: self.__load_profile(2)
            )
            b_pf2.add_element(
                TextPlain(
                    "{}", self.__font_big, self.__color_blue,
                    self.__profiles[2]["player_stats_save"].get("name", self.__default_player_name)
                ),
                nudge=(35, 18)
            )
            b_pf2.add_element(
                TextPlain(
                    "Max Score: {}", self.__font_medium, self.__color_white,
                    self.__profiles[2]["player_stats_save"].get("max_score", 0)
                ),
                nudge=(35, 77),
                color_override_and_lock=self.__color_white
            )
            b_pf2.add_element(
                Ship(self.__profiles[2]["player_stats_save"].get("ship_model_value", self.__default_ship_model_value), 0),
                Allignment.UPPER_RIGHT_CORNER,
                nudge=(-70, 70)
            )
            personal_sprite = get_personal_sprite(self.__profiles[2]["player_stats_save"].get("name", self.__default_player_name))
            if personal_sprite != None:
                b_pf2.add_element(
                    personal_sprite(10, -10),
                    Allignment.BOTTOM_LEFT_CORNER
                )

            b_pf2_delete = Button(
                (offset_x+830, offset_y+140+170*2), (40, 40), (8, 8, 8, 8),
                lambda: self.__delete_profile(2)
            )
            b_pf2_delete.make_weighted(ModKey.SHIFT)
            b_pf2_delete.set_outline_color(self.__color_red)
            b_pf2_delete.set_fill_color(self.__color_red_fill)
            b_pf2_delete.add_description(
                TextPlain("SHIFT+Click to DELETE the Profile", self.__font_very_small, self.__color_white)
            )
            b_pf2_delete.add_element(
                SymbolCross(0, 0, self.__color_red), 
                Allignment.CENTER
            )

            self.__buttons_profile_selection.extend(
                [b_pf2_delete]
            )
            
        else: # Empty profile
            b_pf2 = Button(
                (offset_x, offset_y+90+170*2), (800, 140), b_corners,
                lambda: self.__new_profile(2)
            )
            b_pf2.add_element(
                TextPlain("Null", self.__font_big, self.__color_blue),
                nudge=(35, 18)
            )

        self.__buttons_profile_selection.extend(
            [b_pf0, b_pf1, b_pf2]
        )

    def __initialize_new_profile(self):
        self.__containers_new_profile : list[Container] = []
        self.__buttons_new_profile : list[Button | Switch] = []

        root_x = self.game.screen_resolution[0]/2-225
        root_y = self.game.screen_resolution[1]/2-105
        
        # <> Containers <>

        c_background = Container((root_x, root_y), (450, 210), (10, 25, 10, 25))
        c_background.add_element(
            TextPlain("Creating a new Profile.", self.__font_medium, self.__color_white),
            nudge=(15, 7)
        )
        c_background.add_element(
            TextPlain("Enter your name:", self.__font_medium, self.__color_white),
            nudge=(15, 47)
        )

        c_name = Container((root_x+10, root_y+90), (430, 50), (3, 10, 3, 10))
        c_name.add_element(
            TextUpdated(
                "{}", self.__font_medium, self.__color_white, 
                lambda: self.player_stats.name
            ),
            nudge=(10, 8)
        )

        self.__containers_new_profile.extend(
            [c_background, c_name]
        )
        
        # <> Buttons <>

        b_confirm = Button(
            (root_x+125, root_y+150), (200, 50), (3, 10, 3, 10),
            self.game.finish_getting_player_name
        )
        b_confirm.add_element(
            TextPlain("Confirm", self.__font_medium, self.__color_blue),
            Allignment.CENTER
        )

        self.__buttons_new_profile.extend(
            [b_confirm]
        )

    def __initialize_main_menu(self):
        self.__containers_main_menu : list[Container] = []
        self.__buttons_main_menu : list[Button | Switch] = []

        self.__konami_progress = 0 # Resets Konami sequence

        res = self.game.screen_resolution
        center_x = int((res[0])/2)
        center_y = int((res[1])/2)

        root_x = center_x-400
        root_y = 10
        text_nudge_x = 35
        
        # <> Containers <>
        
        # Profile
        c_profile = Container(
            (center_x-400, 10), (800, 140), (7, 7, 30, 30)
        )
        c_profile.add_element(
            TextPlain(
                "{}", self.__font_big, self.__color_white,
                self.player_stats.name
            ),
            nudge=(text_nudge_x+46, 18)
        )
        c_profile.add_element(
            TextPlain(
                "Max Score: {}", self.__font_medium, self.__color_white,
                self.player_stats.max_score
            ),
            nudge=(text_nudge_x, 77)
        )
        c_profile.add_element(
            Ship(self.player_stats.ship_model_value, 0),
            Allignment.UPPER_RIGHT_CORNER,
            nudge=(-70, 70)
        )
        personal_sprite = get_personal_sprite(self.player_stats.name)
        if personal_sprite != None:
            c_profile.add_element(
                personal_sprite(10, -10),
                Allignment.BOTTOM_LEFT_CORNER
            )
        
        self.__containers_main_menu.extend(
            [c_profile]
        )
        
        # <> Buttons <>

        # Profile
        # Rename
        b_rename = Button(
            (root_x+text_nudge_x, root_y+26), (35, 35), (3, 3, 3, 3),
            lambda: self.__rename_player(Menu.MAIN_MENU)
        )
        b_rename.add_element(
            SymbolPencil(0, 0, self.__color_blue),
            Allignment.CENTER
        )
        # Open
        b_open_info = Button(
            (center_x-15, 125), (50, 20), (3, 3, 3, 3),
            lambda: self.switch_menu(Menu.PLAYER_INFO)
        )
        b_open_info.add_element(
            SymbolArrowDown(0, 0, self.__color_blue),
            Allignment.CENTER
        )

        # Main buttons
        # Space between - 28

        amount_of_buttons = 4
        b_offset_y = (res[1] - (amount_of_buttons*100+28))/2 + 75

        # Start button, starts a Round
        b_start = Button(
            (center_x-185, b_offset_y+100*0), (370, 72), (8, 8, 20, 20), 
            self.game.game_loop
        )
        b_start.add_element(
            TextPlain("Start", self.__font_big, self.__color_blue),
            Allignment.CENTER
        )
        # Opens the Leaderboard
        b_leaderboard = Button(
            (center_x-185, b_offset_y+100*1), (370, 72), (8, 8, 20, 20), 
            lambda: self.switch_menu(Menu.LEADERBOARD)
        )
        b_leaderboard.add_element(
            TextPlain("Leaderboard", self.__font_big, self.__color_blue),
            Allignment.CENTER
        )
        # Back to profile selection
        b_profiles = Button(
            (center_x-185, b_offset_y+100*2), (370, 72), (8, 8, 20, 20), 
            self.__return_to_profile_selection
        )
        b_profiles.add_element(
            TextPlain("Profiles", self.__font_big, self.__color_blue),
            Allignment.CENTER
        )
        # Exits the game
        b_exit = Button(
            (center_x-185, b_offset_y+100*3), (370, 72), (8, 8, 20, 20), 
            self.game.handler_turn_off
        )
        b_exit.add_element(
            TextPlain("Exit", self.__font_big, self.__color_blue),
            Allignment.CENTER
        )
        
        self.__buttons_main_menu.extend(
            [b_start, b_leaderboard, b_exit, b_profiles, b_open_info,
             b_rename]
        )

        self.__add_mini_settings_and_cheats(self.__containers_main_menu, self.__buttons_main_menu)
    
    def __initialize_player_info(self):
        self.__containers_player_info : list[Container] = []
        self.__buttons_player_info : list[Button | Switch] = []
        
        res = self.game.screen_resolution
        center_x = int(res[0]/2)
        root_x = center_x-400
        root_y = 10
        size_y = 483

        text_start_y = 157
        text_row_y = 30
        text_nudge_x = 35

        # <> Containers <>

        # Profile
        c_profile = Container(
            (root_x, root_y), (800, size_y), (7, 7, 30, 30)
        )
        c_profile.add_element(
            Ship(self.player_stats.ship_model_value, 0),
            Allignment.UPPER_RIGHT_CORNER, 
            nudge=(-70, 70)
        )
        c_profile.add_element( # (35, 18)
            TextPlain(
                "{}", self.__font_big, self.__color_white,
                self.player_stats.name
            ),
            nudge=(text_nudge_x+46, 18)
        )
        c_profile.add_element(
            TextPlain(
                "Max Score: {}", self.__font_medium, self.__color_white,
                self.player_stats.max_score
            ),
            nudge=(text_nudge_x, 77)
        )
        c_profile.add_element(
            TextPlain(
                "Longest run: {}", self.__font_medium, self.__color_white,
                self.player_stats.get_longest_time_as_text()
            ),
            nudge=(text_nudge_x, 117)
        )
        c_profile.add_element(
            TextPlain(
                "Asteroids destroyed: {}", self.__font_small, self.__color_white,
                self.player_stats.destroyed_asteroids
            ),
            nudge=(text_nudge_x, text_start_y)
        )
        c_profile.add_element(
            TextPlain(
                "- Basic: {}", self.__font_small, self.__color_white,
                self.player_stats.destroyed_asteroids_basic
            ),
            nudge=(text_nudge_x, text_start_y+text_row_y*1)
        )
        c_profile.add_element(
            TextPlain(
                "- Explosive: {}", self.__font_small, self.__color_white,
                self.player_stats.destroyed_asteroids_explosive
            ),
            nudge=(text_nudge_x, text_start_y+text_row_y*2)
        )
        c_profile.add_element(
            TextPlain(
                "- Golden: {}", self.__font_small, self.__color_white,
                self.player_stats.destroyed_asteroids_golden
            ),
            nudge=(text_nudge_x, text_start_y+text_row_y*3)
        )
        c_profile.add_element(
            TextPlain(
                "- Homing: {}", self.__font_small, self.__color_white,
                self.player_stats.destroyed_asteroids_homing
            ),
            nudge=(text_nudge_x, text_start_y+text_row_y*4)
        )
        c_profile.add_element(
            TextPlain(
                "Loot collected: {}", self.__font_small, self.__color_white,
                self.player_stats.collected_loot
            ),
            nudge=(text_nudge_x, text_start_y+text_row_y*5)
        )
        c_profile.add_element(
            TextPlain(
                "- Copper ore: {}", self.__font_small, self.__color_white,
                self.player_stats.collected_ores_copper
            ),
            nudge=(text_nudge_x, text_start_y+text_row_y*6)
        )
        c_profile.add_element(
            TextPlain(
                "- Silver ore: {}", self.__font_small, self.__color_white,
                self.player_stats.collected_ores_silver
            ),
            nudge=(text_nudge_x, text_start_y+text_row_y*7)
        )
        c_profile.add_element(
            TextPlain(
                "- Golden ore: {}", self.__font_small, self.__color_white,
                self.player_stats.collected_ores_golden
            ),
            nudge=(text_nudge_x, text_start_y+text_row_y*8)
        )
        c_profile.add_element(
            TextPlain(
                "- Diamonds: {}", self.__font_small, self.__color_white,
                self.player_stats.collected_diamonds
            ),
            nudge=(text_nudge_x, text_start_y+text_row_y*9)
        )
        personal_sprite = get_personal_sprite(self.player_stats.name)
        if personal_sprite != None:
            c_profile.add_element(
                personal_sprite(10, -10),
                Allignment.BOTTOM_LEFT_CORNER
            )

        self.__containers_player_info.extend(
            [c_profile]
        )
        
        # <> Buttons <>

        # Close
        b_close_info = Button(
            (center_x-15, size_y-15), (50, 20), (3, 3, 3, 3),
            lambda: self.switch_menu(Menu.MAIN_MENU)
        )
        b_close_info.add_element(
            SymbolArrowUp(0, 0, self.__color_blue),
            Allignment.CENTER
        )
        # Rename
        b_rename = Button(
            (root_x+text_nudge_x, root_y+26), (35, 35), (3, 3, 3, 3),
            lambda: self.__rename_player(Menu.PLAYER_INFO)
        )
        b_rename.add_element(
            SymbolPencil(0, 0, self.__color_blue),
            Allignment.CENTER
        )

        self.__buttons_player_info.extend(
            [b_close_info, b_rename]
        )

        self.__add_mini_settings_and_cheats(self.__containers_player_info, self.__buttons_player_info)
    
    def __initialize_name_edit(self):
        self.__containers_name_edit : list[Container] = []
        self.__buttons_name_edit : list[Button | Switch] = []

        root_x = self.game.screen_resolution[0]/2-225
        root_y = self.game.screen_resolution[1]/2-85
        
        # <> Containers <>

        c_background = Container((root_x, root_y), (450, 170), (10, 25, 10, 25))
        c_background.add_element(
            TextPlain("Edit your name:", self.__font_medium, self.__color_white),
            nudge=(15, 7)
        )

        c_name = Container((root_x+10, root_y+50), (430, 50), (3, 10, 3, 10))
        c_name.add_element(
            TextUpdated(
                "{}", self.__font_medium, self.__color_white, 
                lambda: self.player_stats.name
                ),
                Allignment.LEFT_WALL,
                nudge=(10, 0)

        )

        self.__containers_name_edit.extend(
            [c_background, c_name]
        )
        
        # <> Buttons <>

        b_confirm = Button(
            (root_x+125, root_y+110), (200, 50), (3, 10, 3, 10),
            self.game.finish_getting_player_name
        )
        b_confirm.add_element(
            TextPlain("Confirm", self.__font_medium, self.__color_blue),
            Allignment.CENTER
        )

        self.__buttons_name_edit.extend(
            [b_confirm]
        )

    def __initialize_leaderboard(self):
        self.__containers_leaderboard : list[Container | Leaderboard] = []
        self.__buttons_leaderboard : list[Button | Switch] = []

        res = self.game.screen_resolution
        
        # <> Containers <>

        # Name of the menu
        c_menu_name = Container((res[0] / 2 - 185, 35), (370, 72), (8, 8, 20, 20))
        c_menu_name.add_element(
            TextPlain("Leaderboard", self.__font_big, self.__color_white),
            Allignment.CENTER
        )
        # List of high __scores
        c_leaderboard = Leaderboard(int(res[0]/2)-540, 145, 
            self.__font_medium, self.__scores
        )
        
        self.__containers_leaderboard.extend(
            [c_menu_name, c_leaderboard]
        )
        
        # <> Buttons <>

        # Returns to the Main Menu
        b_back = Button(
            (100, 68), (100, 36), (15, 3, 3, 15), 
            lambda: self.switch_menu(Menu.MAIN_MENU)
        )
        b_back.add_element(
            TextPlain("Back", self.__font_small, self.__color_blue),
            Allignment.CENTER
        )
        
        self.__buttons_leaderboard.extend(
            [b_back]
        )
        # Reset the leaderboard
        b_reset = Button(
            (res[0]-200, 68), (100, 36), (3, 6, 3, 6), 
            self.__reset_leaderboard
        )
        b_reset.set_fill_color(self.__color_red_fill)
        b_reset.make_weighted(ModKey.SHIFT)
        b_reset.set_outline_color(self.__color_red)
        b_reset.add_description(
            TextPlain("SHIFT+Click to RESET the leaderboard", self.__font_very_small, self.__color_white)
        )
        b_reset.add_element(
            TextPlain("Reset", self.__font_small, self.__color_red),
            Allignment.CENTER
        )
        
        self.__buttons_leaderboard.extend(
            [b_back, b_reset]
        )

        # UFO secret
        if not self.player_stats.check_unlocked_ship(ShipType.UFO):
            b_ufo = ButtonRound(
                (res[0]-30, res[1]-20), 6,
                lambda: self.unlock_ship(ShipType.UFO)
            )
            b_ufo.set_outline_color(self.__color_gray)
            b_ufo.set_fill_color(self.__color_green)
            b_ufo.set_hover_fill_color(self.__color_green)
            b_ufo.add_description(
                TextPlain("Do you want to believe?", self.__font_very_small, self.__color_green)
            )
            
            self.__buttons_leaderboard.append(b_ufo)

    def __initialize_hud(self):
        self.__containers_hud : list[Container] = []

        # Space between elements - 10
        
        # <> Containers <>

        # Current weapon
        c_weapon = Container((25, 25), (362, 36), (10, 5, 5, 5))
        c_weapon.add_element(
            TextUpdated(
                "{}.v{}", self.__font_small, self.__color_white, 
                self.player.get_current_weapon_name,
                self.player.get_current_weapon_level
            ),
            Allignment.LEFT_WALL,
            nudge=(9, 0)
        )
        # Timer
        c_timer = Container((397, 25), (176, 36), (5, 10, 5, 5))
        c_timer.add_element(
            TextUpdated(
                "Time: {}", self.__font_small, self.__color_white, 
                self.game.rsm.get_current_time_as_text
            ),
            Allignment.LEFT_WALL,
            nudge=(9, 0)
        )
        # Current score
        c_score = Container((25, 71), (176, 36), (5, 3, 5, 10))
        c_score.add_element(
            TextUpdated(
                "{}pts", self.__font_small, self.__color_white, 
                lambda: self.rsm.score
            ),
            Allignment.LEFT_WALL,
            nudge=(9, 0)
        )
        # Current money
        c_money = Container((211, 71), (176, 36), (3, 3, 3, 3))
        c_money.add_element(
            TextUpdated(
                "{}g", self.__font_small, self.__color_golden, 
                self.player.get_money
            ),
            Allignment.LEFT_WALL,
            nudge=(9, 0)
        )
        # Current health bar
        c_health = Container((397, 71), (176, 36), (3, 5, 10, 5))
        c_health.add_element(
            TextPlain("Lives", self.__font_small, self.__color_white),
            Allignment.LEFT_WALL,
            nudge=(9, 0)
        )
        c_health.add_element(
            HealthBar(
                (102, 5), 2, 6,
                self.player.get_lives,
                self.player_stats.cheat_godmode
            )
        )
        
        self.__containers_hud.extend(
            [c_weapon, c_score, c_money, c_health, c_timer]
        )

        # Cheats detected
        if self.player.is_sus:
            c_cheats = Container((self.game.screen_resolution[0]-399, self.game.screen_resolution[1]-24), (400, 25), (5, 0, 0, 0))
            c_cheats.add_element(
                TextPlain("Cheats enabled! Score won't be saved.", self.__font_very_small, self.__color_white),
                Allignment.CENTER
            )

            self.__containers_hud.append(c_cheats)

    def __initialize_pause_menu(self):
        self.__containers_pause_menu : list[Container] = []
        self.__buttons_pause_menu : list[Button | Switch] = []

        # Space between elements - 15
        offset_x = int((self.game.screen_resolution[0] - 1280)/2)
        offset_y = int((self.game.screen_resolution[1] - 720)/2)
        row_height = 51
        
        # <> Containers <>

        # Background
        c_background = Container((offset_x+50, offset_y+50), (1180, 540), (20, 20, 8, 15))
        c_background.set_fill_color((75, 75, 100, 150))
                
        # Current ship
        c_ship = Container((offset_x+65, offset_y+65), (210, 210), (12, 6, 6, 6))
        c_ship.add_element(
            self.player.get_ship, 
            Allignment.CENTER
        )

        # List - ship
        c_model = Container((offset_x+290, offset_y+65), (455, 36), (6, 6, 6, 6))
        c_model.add_element(
            TextUpdated(
                "Model: {}", self.__font_small, self.__color_white,
                self.player.ship.get_name
            ),
            Allignment.LEFT_WALL,
            nudge=(12, 0)
        )
        
        c_switch_model = Container((offset_x+336, offset_y+65+row_height*1), (363, 36), (3, 3, 3, 3))
        c_switch_model.add_element(
            TextPlain("Switch model", self.__font_small, self.__color_white),
            Allignment.LEFT_WALL,
            nudge=(12, 0)
        )

        c_heal = Container((offset_x+290, offset_y+65+row_height*2), (409, 36), (6, 3, 3, 6))
        c_heal.add_element(
            TextUpdated(
                "Heal: {}g", self.__font_small, self.__color_white,
                self.player.get_price_heal
            ),
            Allignment.LEFT_WALL,
            nudge=(12, 0)
        )
        
        c_magnet = Container((offset_x+290, offset_y+65+row_height*3), (455, 36), (6, 6, 6, 6))
        c_magnet.add_element(
            TextUpdated(
                "Magnet.v{}", self.__font_small, self.__color_white,
                lambda: self.player.get_part_level(ShipPart.MAGNET)
            ),
            Allignment.LEFT_WALL,
            nudge=(12, 0)
        )
        
        c_magnet_rad = Container((offset_x+290, offset_y+65+row_height*4), (409, 36), (6, 3, 3, 6))
        c_magnet_rad.add_element(
            TextUpdated(
                "Radius: {}", self.__font_small, self.__color_white,
                lambda: self.player.get_upgrade_price_as_text(ShipUpgrade.MAGNET_RADIUS)
            ),
            Allignment.LEFT_WALL,
            nudge=(12, 0)
        )
        
        c_magnet_str = Container((offset_x+290, offset_y+65+row_height*5), (409, 36), (6, 3, 3, 6))
        c_magnet_str.add_element(
            TextUpdated(
                "Strength: {}", self.__font_small, self.__color_white,
                lambda: self.player.get_upgrade_price_as_text(ShipUpgrade.MAGNET_STRENGTH)
            ),
            Allignment.LEFT_WALL,
            nudge=(12, 0)
        )

        # Current stats
        # Score
        c_points = Container((offset_x+760, offset_y+65), (150, 36), (6, 3, 3, 6))
        c_points.add_element(
            TextUpdated(
                "{}pts", self.__font_small, self.__color_white, 
                lambda: self.rsm.score
            ),
            Allignment.LEFT_WALL,
            nudge=(9, 0)
        )
        # Money
        c_money = Container((offset_x+920, offset_y+65), (127, 36), (3, 3, 3, 3))
        c_money.add_element(
            TextUpdated(
                "{}g", self.__font_small, self.__color_golden, 
                self.player.get_money
            ),
            Allignment.LEFT_WALL,
            nudge=(9, 0)
        )
        # Health
        c_health = Container((offset_x+1057, offset_y+65), (158, 36), (3, 6, 6, 3))
        c_health.add_element(
            TextPlain("Lives", self.__font_small, self.__color_white),
            Allignment.LEFT_WALL,
            nudge=(9, 0)
        )
        c_health.add_element(
            HealthBar(
                (84, 5), 2, 2,
                self.player.get_lives,
                self.player_stats.cheat_godmode
            )
        )
        # List - weapons
        # Plasma Gun
        c_weapon_1 = Container((offset_x+760, offset_y+65+row_height*1), (455, 36), (6, 6, 6, 6))
        c_weapon_1.add_element(
            TextUpdated(
                "Weapon 1: {}.v{}", self.__font_small, self.__color_white,
                self.player.weapon_plasmagun.get_name,
                lambda: self.player.get_part_level(ShipPart.PLASMAGUN)
            ),
            Allignment.LEFT_WALL,
            nudge=(12, 0)
        )
        c_weapon_1_proj = Container((offset_x+760, offset_y+65+row_height*2), (409, 36), (6, 3, 3, 6))
        c_weapon_1_proj.add_element(
            TextUpdated(
                "Projectiles: {}", self.__font_small, self.__color_white,
                lambda: self.player.get_upgrade_price_as_text(ShipUpgrade.PLASMAGUN_PROJECTILES)
            ),
            Allignment.LEFT_WALL,
            nudge=(12, 0)
        )
        c_weapon_1_cd = Container((offset_x+760, offset_y+65+row_height*3), (409, 36), (6, 3, 3, 6))
        c_weapon_1_cd.add_element(
            TextUpdated(
                "Cooldown: {}", self.__font_small, self.__color_white,
                lambda: self.player.get_upgrade_price_as_text(ShipUpgrade.PLASMAGUN_COOLDOWN)
            ),
            Allignment.LEFT_WALL,
            nudge=(12, 0)
        )
        #Bomb Launcher
        c_weapon_2 = Container((offset_x+760, offset_y+65+row_height*4), (455, 36), (6, 6, 6, 6))
        c_weapon_2.add_element(
            TextUpdated(
                "Weapon 2: {}.v{}", self.__font_small, self.__color_white,
                self.player.weapon_bomblauncher.get_name,
                lambda: self.player.get_part_level(ShipPart.BOMBLAUNCHER)
            ),
            Allignment.LEFT_WALL,
            nudge=(12, 0)
        )
        c_weapon_2_rad = Container((offset_x+760, offset_y+65+row_height*5), (409, 36), (6, 3, 3, 6))
        c_weapon_2_rad.add_element(
            TextUpdated(
                "Radius: {}", self.__font_small, self.__color_white,
                lambda: self.player.get_upgrade_price_as_text(ShipUpgrade.BOMBLAUNCHER_RADIUS)
            ),
            Allignment.LEFT_WALL,
            nudge=(12, 0)
        )
        c_weapon_2_fuse = Container((offset_x+760, offset_y+65+row_height*6), (409, 36), (6, 3, 3, 6))
        c_weapon_2_fuse.add_element(
            TextUpdated(
                "Fuse: {}", self.__font_small, self.__color_white,
                lambda: self.player.get_upgrade_price_as_text(ShipUpgrade.BOMBLAUNCHER_FUSE)
            ),
            Allignment.LEFT_WALL,
            nudge=(12, 0)
        )

        self.__containers_pause_menu.extend(
            [c_background, c_ship, c_model, c_switch_model, c_heal,
             c_magnet, c_magnet_rad, c_magnet_str, c_points, c_money,
             c_health, c_weapon_1, c_weapon_1_proj, c_weapon_2, c_weapon_2_rad,
             c_weapon_2_fuse, c_weapon_1_cd]
        )
        
        # <> Buttons <>

        # Switch - Auto-Shoot
        s_auto_shoot = Switch(
            (offset_x+65, offset_y+535), (40, 40), (8, 8, 8, 8),
            self.player.switch_auto_shoot,
            self.player.is_auto_shooting
        )
        s_auto_shoot.add_description(
            TextPlain("Switch the AUTO-SHOOT on/off", self.__font_very_small, self.__color_white)
        )
        s_auto_shoot.set_active_outline_color(self.__color_green)
        s_auto_shoot.add_element(
            TextPlain("AU", self.__font_small, self.__color_blue),
            Allignment.CENTER
        )
        s_auto_shoot.set_active_outline_color = self.__color_green

        # Model switching
        b_model_left = Button(
            (offset_x+290, offset_y+65+row_height*1), (36, 36), (6, 3, 3, 6), 
            self.player_stats.switch_ship_model_to_previous
        )
        b_model_left.add_element(
            TextPlain("<", self.__font_small, self.__color_blue),
            Allignment.CENTER
        )

        b_model_right = Button(
            (offset_x+709, offset_y+65+row_height*1), (36, 36), (3, 6, 6, 3), 
            self.player_stats.switch_ship_model_to_next
        )
        b_model_right.add_element(
            TextPlain(">", self.__font_small, self.__color_blue),
            Allignment.CENTER
        )
        # Heal
        b_heal = Button(
           (offset_x+709, offset_y+65+row_height*2), (36, 36), (3, 6, 6, 3),
            self.player.buy_heal,
            self.player.can_heal
        )
        b_heal.set_outline_color(self.__color_green)
        b_heal.add_element(
            TextPlain("/\\", self.__font_small, self.__color_green),
            Allignment.CENTER
        )
        # Magnet
        b_magnet_rad = Button(
            (offset_x+709, offset_y+65+row_height*4), (36, 36), (3, 6, 6, 3),
            lambda: self.player.buy_upgrade(ShipUpgrade.MAGNET_RADIUS),
            lambda: self.player.can_buy_upgrade(ShipUpgrade.MAGNET_RADIUS)
        )
        b_magnet_rad.set_outline_color(self.__color_green)
        b_magnet_rad.add_element(
            TextPlain("/\\", self.__font_small, self.__color_green),
            Allignment.CENTER
        )

        b_magnet_str = Button(
            (offset_x+709, offset_y+65+row_height*5), (36, 36), (3, 6, 6, 3),
            lambda: self.player.buy_upgrade(ShipUpgrade.MAGNET_STRENGTH),
            lambda: self.player.can_buy_upgrade(ShipUpgrade.MAGNET_STRENGTH)
        )
        b_magnet_str.set_outline_color(self.__color_green)
        b_magnet_str.add_element(
            TextPlain("/\\", self.__font_small, self.__color_green),
            Allignment.CENTER
        )

        # Upgrade weapons
        b_weapon_1_proj_up = Button(
            (offset_x+1179, offset_y+65+row_height*2), (36, 36), (3, 6, 6, 3),
            lambda: self.player.buy_upgrade(ShipUpgrade.PLASMAGUN_PROJECTILES),
            lambda: self.player.can_buy_upgrade(ShipUpgrade.PLASMAGUN_PROJECTILES)
        )
        b_weapon_1_proj_up.set_outline_color(self.__color_green)
        b_weapon_1_proj_up.add_element(
            TextPlain("/\\", self.__font_small, self.__color_green),
            Allignment.CENTER
        )
        b_weapon_1_cd_up = Button(
            (offset_x+1179, offset_y+65+row_height*3), (36, 36), (3, 6, 6, 3),
            lambda: self.player.buy_upgrade(ShipUpgrade.PLASMAGUN_COOLDOWN),
            lambda: self.player.can_buy_upgrade(ShipUpgrade.PLASMAGUN_COOLDOWN)
        )
        b_weapon_1_cd_up.set_outline_color(self.__color_green)
        b_weapon_1_cd_up.add_element(
            TextPlain("/\\", self.__font_small, self.__color_green),
            Allignment.CENTER
        )
        
        b_weapon_2_rad_up = Button(
            (offset_x+1179, offset_y+65+row_height*5), (36, 36), (3, 6, 6, 3),
            lambda: self.player.buy_upgrade(ShipUpgrade.BOMBLAUNCHER_RADIUS),
            lambda: self.player.can_buy_upgrade(ShipUpgrade.BOMBLAUNCHER_RADIUS)
        )
        b_weapon_2_rad_up.set_outline_color(self.__color_green)
        b_weapon_2_rad_up.add_element(
            TextPlain("/\\", self.__font_small, self.__color_green),
            Allignment.CENTER
        )
        b_weapon_2_fuse_up = Button(
            (offset_x+1179, offset_y+65+row_height*6), (36, 36), (3, 6, 6, 3),
            lambda: self.player.buy_upgrade(ShipUpgrade.BOMBLAUNCHER_FUSE),
            lambda: self.player.can_buy_upgrade(ShipUpgrade.BOMBLAUNCHER_FUSE)
        )
        b_weapon_2_fuse_up.set_outline_color(self.__color_green)
        b_weapon_2_fuse_up.add_element(
            TextPlain("/\\", self.__font_small, self.__color_green),
            Allignment.CENTER
        )

        # Ends the run and returns to the main menu
        b_end_run = Button(
            (offset_x+890, offset_y+600), (340, 72), (8, 8, 20, 20),
            self.game.handler_finish_round
        )
        b_end_run.make_weighted(ModKey.SHIFT)
        b_end_run.set_outline_color(self.__color_red)
        b_end_run.set_fill_color(self.__color_red_fill)
        b_end_run.add_description(
            TextPlain("SHIFT+Click to end the run early", self.__font_very_small, self.__color_white)
        )
        b_end_run.add_element(
            TextPlain("End Run", self.__font_big, self.__color_red),
            Allignment.CENTER
        )

        self.__buttons_pause_menu.extend(
            [b_model_left, b_model_right, b_heal, b_magnet_rad, b_magnet_str,
             b_end_run, s_auto_shoot, b_weapon_1_cd_up, b_weapon_1_proj_up, b_weapon_2_fuse_up,
             b_weapon_2_rad_up]
        )

    def __initialize_name_check(self):
        self.__containers_name_check : list[Container] = []
        self.__buttons_name_check : list[Button | Switch] = []

        root_x = self.game.screen_resolution[0]/2-225
        root_y = self.game.screen_resolution[1]/2-105
        
        # <> Containers <>

        c_background = Container((root_x, root_y), (450, 210), (10, 25, 10, 25))
        c_background.add_element(
            TextPlain(
                "New record! {}pts", self.__font_medium, self.__color_white, 
                self.game.rsm.score
            ),
            nudge=(15, 7)
        )

        self.__containers_name_check.extend(
            [c_background]
        )
        
        # <> Buttons <>

        b_confirm = Button(
            (root_x+125, root_y+150), (200, 50), (3, 10, 3, 10),
            self.game.finish_round
        )
        b_confirm.add_element(
            TextPlain("Confirm", self.__font_medium, self.__color_blue),
            Allignment.CENTER
        )

        self.__buttons_name_check.extend(
            [b_confirm]
        )

    def __initialize_test_menu(self):
        """Place stuff here and assign as starting menu to test things without breaking anything else."""

        self.__containers_test_menu : list[Container] = []
        self.__buttons_test_menu : list[Button | Switch] = []
        
        res = self.game.screen_resolution

        # <> Containers <>

        container = Container((10, 10), (res[0]-20, res[1]-20), (5, 5, 5, 5))

        self.__containers_test_menu.extend(
            [container]
        )
        
        # <> Buttons <>

        self.__buttons_test_menu.extend(
            []
        )

    ### Template for menus

    # def __initialize_(self):
    #     self.__containers_ : list[Container] = []
    #     self.__buttons_ : list[Button | Switch] = []
        
    #     # <> Containers <>

    #     self.__containers_.extend(
    #         []
    #     )
        
    #     # <> Buttons <>

    #     self.__buttons_.extend(
    #         []
    #     )

    ### Secret stuff

    def handle_event_for_secrets(self, event : pygame.event.Event):
        match self.__current_menu:
            case Menu.MAIN_MENU:
                if event.type == pygame.KEYDOWN:
                    # Cheat visibility
                    if event.scancode == self.__konami_sequence[self.__konami_progress]:
                        self.__konami_progress += 1
                        if self.__konami_progress == 11:
                            self.__konami_progress = 0
                            self.player_stats.found_cheats = True
                            self.initialize_current_menu()
                    else:
                        self.__konami_progress = 0

    def unlock_ship(self, ship_type : ShipType):
        self.player_stats.unlock_ship(ship_type)
        self.initialize_current_menu()
