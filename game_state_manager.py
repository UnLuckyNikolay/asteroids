# pyright: reportAttributeAccessIssue=false

import pygame, json, os
from enum import Enum
from typing import Any

from constants import *
from json_helper.leaderboard.validator import ValidateLeaderboard
from json_helper.profile.validator import ValidateProfile

from ui_elements.container import Container, Allignment
from ui_elements.buttons import Button, Switch, ModKey
from ui_elements.text import Text, TextH, TextF
from ui_elements.sprites.healthbar import HealthBar
from ui_elements.sprites.leaderboard import Leaderboard
from ui_elements.sprites.symbol_fullscreen import SymbolFullscreen
from ui_elements.sprites.symbol_cross import SymbolCross

from round_state_manager import RoundStateManager
from player.player import Player, ShipUpgrade, ShipPart
from player.player_stats import PlayerStats
from player.ship import Ship


# New menus should be added to:
# .initialize_current_menu
# .check_hovered_button 
# .draw (and make new function)
class Menu(Enum):
    PROFILE_SELECTION = "Profile selection" # WIP
    NEW_PROFILE = "Name edit" # NOT ADDED
    MAIN_MENU = "Main Menu"
    LEADERBOARD = "Leaderboard"
    HUD = "HUD"
    PAUSE_MENU = "Pause"
    NAME_CHECK = "Name check" # REDO AFTERWARDS TO ROUND_END

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
        self.__current_menu : Menu = Menu.PROFILE_SELECTION

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

        # Getting profile
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
        print(f"> Profile 0:\n{self.__profiles[0]}") # TEST
        print(f"> Profile 1:\n{self.__profiles[1]}")
        print(f"> Profile 2:\n{self.__profiles[2]}")

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
                case Menu.LEADERBOARD:
                    button_list = self.__buttons_leaderboard
                case Menu.HUD:
                    return # No buttons currently planned for HUD
                case Menu.PAUSE_MENU:
                    button_list = self.__buttons_pause_menu
                case Menu.NAME_CHECK:
                    button_list = self.__buttons_name_check
                case _:
                    print(f"Error: menu `{self.__current_menu.value}` missing in userinterface.check_hovered_button")

            # Check for a button hover
            for i in range(len(button_list)):
                if button_list[i].check_cursor_hover(position):
                    self.__hovered_button = button_list[i]
                    self.__hovered_button.switch_hovered_state()
                    return
        
        # Check if cursor moved off the button
        elif (
            position[0] < self.__hovered_button._position[0] or
            position[0] > self.__hovered_button._position[0] + self.__hovered_button._size[0] or
            position[1] < self.__hovered_button._position[1] or
            position[1] > self.__hovered_button._position[1] + self.__hovered_button._size[1]
        ):
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
        print(number)
        self.__current_profile = number
        profile = self.__profiles[number]

        if profile["version"] == 1:
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

    def check_score(self, new_score):
        is_updated = False

        while len(self.__scores) > LEADERBOARD_LENGTH:   # Shortens leaderboard if max length was reduced
            is_updated = True
            self.__scores.pop()
        
        if len(self.__scores) == LEADERBOARD_LENGTH and new_score > self.__scores[LEADERBOARD_LENGTH - 1]["score"]:
            is_updated = True
            self.__scores.pop()
        if len(self.__scores) != LEADERBOARD_LENGTH:
            is_updated = True
            self.game.get_player_name()
            self.__scores.append({"name": self.player_stats.name, "score": new_score})
            self.__scores.sort(key=lambda x: x["score"], reverse=True)

        if not is_updated:
            return

        self.__save_leaderboard()
        self.__initialize_leaderboard()

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
            case Menu.LEADERBOARD:
                self.__draw_leaderboard(screen)
            case Menu.HUD:
                self.__draw_hud(screen)
            case Menu.PAUSE_MENU:
                self.__draw_pause_menu(screen)
            case Menu.NAME_CHECK:
                self.__draw_name_check(screen)
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
            case Menu.LEADERBOARD:
                self.__initialize_leaderboard()
            case Menu.HUD:
                self.__initialize_hud()
            case Menu.PAUSE_MENU:
                self.__initialize_pause_menu()
            case Menu.NAME_CHECK:
                self.__initialize_name_check()
            case _:
                print(f"> Error: missing menu {self.__current_menu.value} in UserInterface.initialize_current_menu")

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
            Text(
                "Select the Profile", (83, 4), self.__font_big, self.__color_white
            )
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
                TextF("{}", (19, 10), self.__font_big, self.__color_blue,
                      self.__profiles[0]["player_stats_save"]["name"])
            )
            b_pf0.add_element(
                Ship(self.__profiles[0]["player_stats_save"]["ship_model"], 0),
                Allignment.CENTER_ON_THE_LEFT
            )
            b_pf0_delete = Button(
                (offset_x+830, offset_y+140+170*0), (40, 40), (8, 8, 8, 8),
                lambda: self.__delete_profile(0)
            )
            b_pf0_delete.make_weighted(ModKey.SHIFT)
            b_pf0_delete.set_outline_color(self.__color_red)
            b_pf0_delete.set_fill_color(self.__color_red_fill)
            b_pf0_delete.add_description(
                Text("SHIFT+Click to DELETE the Profile", (0, 0), self.__font_very_small, self.__color_white)
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
                Text("Null", (19, 10), self.__font_big, self.__color_blue)
            )

        # Profile 1
        if self.__profiles[1] != None:
            b_pf1 = Button(
                (offset_x, offset_y+90+170*1), (800, 140), b_corners,
                lambda: self.__load_profile(1)
            )
            b_pf1.add_element(
                TextF("{}", (19, 10), self.__font_big, self.__color_blue,
                      self.__profiles[1]["player_stats_save"]["name"])
            )
            b_pf1.add_element(
                Ship(self.__profiles[1]["player_stats_save"]["ship_model"], 0),
                Allignment.CENTER_ON_THE_LEFT
            )
            b_pf1_delete = Button(
                (offset_x+830, offset_y+140+170*1), (40, 40), (8, 8, 8, 8),
                lambda: self.__delete_profile(1)
            )
            b_pf1_delete.make_weighted(ModKey.SHIFT)
            b_pf1_delete.set_outline_color(self.__color_red)
            b_pf1_delete.set_fill_color(self.__color_red_fill)
            b_pf1_delete.add_description(
                Text("SHIFT+Click to DELETE the Profile", (0, 0), self.__font_very_small, self.__color_white)
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
                Text("Null", (19, 10), self.__font_big, self.__color_blue)
            )

        # Profile 2
        if self.__profiles[2] != None:
            b_pf2 = Button(
                (offset_x, offset_y+90+170*2), (800, 140), b_corners,
                lambda: self.__load_profile(2)
            )
            b_pf2.add_element(
                TextF("{}", (19, 10), self.__font_big, self.__color_blue,
                      self.__profiles[2]["player_stats_save"]["name"])
            )
            b_pf2.add_element(
                Ship(self.__profiles[2]["player_stats_save"]["ship_model"], 0),
                Allignment.CENTER_ON_THE_LEFT
            )
            b_pf2_delete = Button(
                (offset_x+830, offset_y+140+170*1), (40, 40), (8, 8, 8, 8),
                lambda: self.__delete_profile(2)
            )
            b_pf2_delete.make_weighted(ModKey.SHIFT)
            b_pf2_delete.set_outline_color(self.__color_red)
            b_pf1_delete.set_fill_color(self.__color_red_fill)
            b_pf2_delete.add_description(
                Text("SHIFT+Click to DELETE the Profile", (0, 0), self.__font_very_small, self.__color_white)
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
                Text("Null", (19, 10), self.__font_big, self.__color_blue)
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
            TextF("Creating a new Profile.", (15, 7), self.__font_medium, self.__color_white)
        )
        c_background.add_element(
            Text("Enter your name:", (15, 47), self.__font_medium, self.__color_white)
        )

        c_name = Container((root_x+10, root_y+90), (430, 50), (3, 10, 3, 10))
        c_name.add_element(
            TextH("{}", (10, 10), self.__font_medium, self.__color_white, 
                  lambda: self.player_stats.name)
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
            Text("Confirm", (10, 8), self.__font_medium, self.__color_blue)
        )

        self.__buttons_new_profile.extend(
            [b_confirm]
        )

    def __initialize_main_menu(self):
        self.__containers_main_menu : list[Container] = []
        self.__buttons_main_menu : list[Button | Switch] = []

        self.__konami_progress = 0 # Resets Konami sequence

        center_x = int((self.game.screen_resolution[0])/2)
        center_y = int((self.game.screen_resolution[1])/2)
        
        # <> Containers <>

        # Settings
        c_settings = Container((10, self.game.screen_resolution[1]-80), (90, 20), (8, 2, 8, 2))
        c_settings.add_element(
            Text("Settings", (5, 1), self.__font_very_small, self.__color_white)
        )

        if self.player_stats.found_cheats:
            # Cheats
            c_cheats = Container((self.game.screen_resolution[0]-100, self.game.screen_resolution[1]-80), (90, 20), (2, 8, 2, 8))
            c_cheats.add_element(
                Text("Cheats", (13, 1), self.__font_very_small, self.__color_white)
            )
            
            self.__containers_main_menu.extend(
                [c_cheats]
            )
        
        self.__containers_main_menu.extend(
            [c_settings]
        )
        
        # <> Buttons <>

        # Start button, starts a Round
        b_start = Button(
            (center_x-185, center_y-136), (370, 72), (8, 8, 20, 20), 
            self.game.game_loop
        )
        b_start.add_element(
            Text("Start", (117, 10), self.__font_big, self.__color_blue)
        )
        # Opens the Leaderboard
        b_leaderboard = Button(
            (center_x-185, center_y-36), (370, 72), (8, 8, 20, 20), 
            lambda: self.switch_menu(Menu.LEADERBOARD)
        )
        b_leaderboard.add_element(
            Text("Leaderboard", (16, 10), self.__font_big, self.__color_blue)
        )
        # Exits the game
        b_exit = Button(
            (center_x-185, center_y+64), (370, 72), (8, 8, 20, 20), 
            self.game.handler_turn_off
        )
        b_exit.add_element(
            Text("Exit", (135, 10), self.__font_big, self.__color_blue)
        )

        # Regenerate background
        b_background = Button(
            (10, self.game.screen_resolution[1]-50), (40, 40), (8, 8, 8, 8),
            self.game.handler_regenerate_background
        )
        b_background.add_description(
            Text("Generate new background", (0, 0), self.__font_very_small, self.__color_white)
        )
        b_background.add_element(
            Text("BG", (4, 7), self.__font_small, self.__color_blue)
        )
        # Switch Fullscreen
        s_fullscreen = Switch(
            (60, self.game.screen_resolution[1]-50), (40, 40), (8, 8, 8, 8),
            self.game.switch_fullscreen,
            self.game.is_fullscreen
        )
        s_fullscreen.add_description(
            Text("Switch the FULLSCREEN mode on/off", (0, 0), self.__font_very_small, self.__color_white)
        )
        s_fullscreen.add_element(
            SymbolFullscreen(0, 0, self.__color_blue), 
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
                Text("Switch the HITBOX cheat on/off", (0, 0), self.__font_very_small, self.__color_white)
            )
            s_hitbox.set_active_outline_color(self.__color_golden)
            s_hitbox.add_element(
                Text("HB", (3, 7), self.__font_small, self.__color_blue)
            )
            s_hitbox.set_active_outline_color = self.__color_golden
            # Cheat - Money cheat
            s_money = Switch(
                (self.game.screen_resolution[0]-100, self.game.screen_resolution[1]-50), (40, 40), (8, 8, 8, 8),
                self.player_stats.switch_stonks,
                self.player_stats.cheat_stonks
            )
            s_money.add_description(
                Text("Switch the MONEY cheat on/off", (0, 0), self.__font_very_small, self.__color_white)
            )
            s_money.set_active_outline_color(self.__color_golden)
            s_money.add_element(
                Text("MN", (2, 7), self.__font_small, self.__color_blue)
            )
            s_money.set_active_outline_color = self.__color_golden
            # Cheat - Godmode
            s_godmode = Switch(
                (self.game.screen_resolution[0]-50, self.game.screen_resolution[1]-50), (40, 40), (8, 8, 8, 8),
                self.player_stats.switch_godmode,
                self.player_stats.cheat_godmode
            )
            s_godmode.add_description(
                Text("Switch the GODMODE cheat on/off", (0, 0), self.__font_very_small, self.__color_white)
            )
            s_godmode.set_active_outline_color(self.__color_golden)
            s_godmode.add_element(
                Text("GM", (2, 7), self.__font_small, self.__color_blue)
            )
            s_godmode.set_active_outline_color = self.__color_golden
                
            self.__buttons_main_menu.extend(
                [s_hitbox, s_money, s_godmode]
            )
        
        self.__buttons_main_menu.extend(
            [b_start, b_leaderboard, b_exit, b_background, s_fullscreen]
        )
        
    def __initialize_leaderboard(self):
        self.__containers_leaderboard : list[Container | Leaderboard] = []
        self.__buttons_leaderboard : list[Button | Switch] = []
        
        # <> Containers <>

        # Name of the menu
        c_menu_name = Container((self.game.screen_resolution[0] / 2 - 185, 35), (370, 72), (8, 8, 20, 20))
        c_menu_name.add_element(
            Text("Leaderboard", (16, 10), self.__font_big, self.__color_white)
        )
        # List of high __scores
        c_leaderboard = Leaderboard(int(self.game.screen_resolution[0]/2)-540, 145, 
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
            Text("Back", (18, 5), self.__font_small, self.__color_blue)
        )
        
        self.__buttons_leaderboard.extend(
            [b_back]
        )
        # Reset the leaderboard
        b_reset = Button(
            (self.game.screen_resolution[0]-200, 68), (100, 36), (3, 6, 3, 6), 
            self.__reset_leaderboard
        )
        b_reset.set_fill_color(self.__color_red_fill)
        b_reset.make_weighted(ModKey.SHIFT)
        b_reset.set_outline_color(self.__color_red)
        b_reset.add_description(
            Text("SHIFT+Click to RESET the leaderboard", (0, 0), self.__font_very_small, self.__color_white)
        )
        b_reset.add_element(
            Text("Reset", (9, 5), self.__font_small, self.__color_red)
        )
        
        self.__buttons_leaderboard.extend(
            [b_back, b_reset]
        )

    def __initialize_hud(self):
        self.__containers_hud : list[Container] = []

        # Space between elements - 10
        
        # <> Containers <>

        # Current weapon
        c_weapon = Container((25, 25), (548, 36), (10, 10, 5, 5))
        c_weapon.add_element(
            TextH("Weapon: {}.v{}", (9, 5), self.__font_small, self.__color_white, 
                  self.player.get_current_weapon_name,
                  self.player.get_current_weapon_level)
        )
        # Current score
        c_score = Container((25, 71), (176, 36), (5, 3, 5, 10))
        c_score.add_element(
            TextH("{}pts", (9, 5), self.__font_small, self.__color_white, 
                  self.rsm.get_score)
        )
        # Current money
        c_money = Container((211, 71), (176, 36), (3, 3, 3, 3))
        c_money.add_element(
            TextH("{}g", (9, 5), self.__font_small, self.__color_golden, 
                  self.player.get_money)
        )
        # Current health bar
        c_health = Container((397, 71), (176, 36), (3, 5, 10, 5))
        c_health.add_element(
            Text("Lives", (9, 5), self.__font_small, self.__color_white)
        )
        c_health.add_element(
            HealthBar((102, 5), 2, 6,
                      self.player.get_lives)
        )
        
        self.__containers_hud.extend(
            [c_weapon, c_score, c_money, c_health]
        )

        # Cheats detected
        if self.player.is_sus:
            c_cheats = Container((self.game.screen_resolution[0]-399, self.game.screen_resolution[1]-24), (400, 25), (5, 0, 0, 0))
            c_cheats.add_element(
                Text("Cheats enabled! Score won't be saved.", (6, 3), self.__font_very_small, self.__color_white)
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
            TextH("Model: {}", (12, 5), self.__font_small, self.__color_white,
                  self.player.ship.get_name)
        )
        
        c_switch_model = Container((offset_x+336, offset_y+65+row_height*1), (363, 36), (3, 3, 3, 3))
        c_switch_model.add_element(
            Text("Switch model", (12, 5), self.__font_small, self.__color_white)
        )

        c_heal = Container((offset_x+290, offset_y+65+row_height*2), (409, 36), (6, 3, 3, 6))
        c_heal.add_element(
            TextH("Heal: {}g", (12, 5), self.__font_small, self.__color_white,
                  self.player.get_price_heal)
        )
        
        c_magnet = Container((offset_x+290, offset_y+65+row_height*3), (455, 36), (6, 6, 6, 6))
        c_magnet.add_element(
            TextH("Magnet.v{}", (12, 5), self.__font_small, self.__color_white,
                  lambda: self.player.get_part_level(ShipPart.MAGNET))
        )
        
        c_magnet_rad = Container((offset_x+290, offset_y+65+row_height*4), (409, 36), (6, 3, 3, 6))
        c_magnet_rad.add_element(
            TextH("Radius: {}", (12, 5), self.__font_small, self.__color_white,
                  lambda: self.player.get_upgrade_price_as_text(ShipUpgrade.MAGNET_RADIUS))
        )
        
        c_magnet_str = Container((offset_x+290, offset_y+65+row_height*5), (409, 36), (6, 3, 3, 6))
        c_magnet_str.add_element(
            TextH("Strength: {}", (12, 5), self.__font_small, self.__color_white,
                  lambda: self.player.get_upgrade_price_as_text(ShipUpgrade.MAGNET_STRENGTH))
        )

        # Current stats
        # Score
        c_points = Container((offset_x+760, offset_y+65), (150, 36), (6, 3, 3, 6))
        c_points.add_element(
            TextH("{}pts", (9, 5), self.__font_small, self.__color_white, 
                  self.rsm.get_score)
        )
        # Money
        c_money = Container((offset_x+920, offset_y+65), (127, 36), (3, 3, 3, 3))
        c_money.add_element(
            TextH("{}g", (9, 5), self.__font_small, self.__color_golden, 
                  self.player.get_money)
        )
        # Health
        c_health = Container((offset_x+1057, offset_y+65), (158, 36), (3, 6, 6, 3))
        c_health.add_element(
            Text("Lives", (9, 5), self.__font_small, self.__color_white)
        )
        c_health.add_element(
            HealthBar((84, 5), 2, 2,
            self.player.get_lives)
        )
        # List - weapons
        c_weapon_1 = Container((offset_x+760, offset_y+65+row_height*1), (455, 36), (6, 6, 6, 6))
        c_weapon_1.add_element(
            TextH("Weapon 1: {}.v{}", (12, 5), self.__font_small, self.__color_white,
                  self.player.weapon_plasmagun.get_name,
                  lambda: self.player.get_part_level(ShipPart.PLASMAGUN))
        )

        c_weapon_1_proj = Container((offset_x+760, offset_y+65+row_height*2), (409, 36), (6, 3, 3, 6))
        c_weapon_1_proj.add_element(
            TextH("Projectiles: {}", (12, 5), self.__font_small, self.__color_white,
                  lambda: self.player.get_upgrade_price_as_text(ShipUpgrade.PLASMAGUN_PROJECTILES))
        )
        
        c_weapon_2 = Container((offset_x+760, offset_y+65+row_height*3), (455, 36), (6, 6, 6, 6))
        c_weapon_2.add_element(
            TextH("Weapon 2: {}.v{}", (12, 5), self.__font_small, self.__color_white,
                  self.player.weapon_bomblauncher.get_name,
                  lambda: self.player.get_part_level(ShipPart.BOMBLAUNCHER))
        )
        
        c_weapon_2_rad = Container((offset_x+760, offset_y+65+row_height*4), (409, 36), (6, 3, 3, 6))
        c_weapon_2_rad.add_element(
            TextH("Radius: {}", (12, 5), self.__font_small, self.__color_white,
                  lambda: self.player.get_upgrade_price_as_text(ShipUpgrade.BOMBLAUNCHER_RADIUS))
        )

        self.__containers_pause_menu.extend(
            [c_background, c_ship, c_model, c_switch_model, c_heal,
             c_magnet, c_magnet_rad, c_magnet_str, c_points, c_money,
             c_health, c_weapon_1, c_weapon_1_proj, c_weapon_2, c_weapon_2_rad]
        )
        
        # <> Buttons <>

        # Switch - Auto-Shoot
        s_auto_shoot = Switch(
            (offset_x+65, offset_y+535), (40, 40), (8, 8, 8, 8),
            self.player.switch_auto_shoot,
            self.player.is_auto_shooting
        )
        s_auto_shoot.add_description(
            Text("Switch the AUTO-SHOOT on/off", (0, 0), self.__font_very_small, self.__color_white)
        )
        s_auto_shoot.set_active_outline_color(self.__color_green)
        s_auto_shoot.add_element(
            Text("AU", (1, 7), self.__font_small, self.__color_blue)
        )
        s_auto_shoot.set_active_outline_color = self.__color_green

        # Model switching
        b_model_left = Button(
            (offset_x+290, offset_y+65+row_height*1), (36, 36), (6, 3, 3, 6), 
            self.player_stats.switch_ship_model_to_previous
        )
        b_model_left.add_element(
            Text("<", (12, 5), self.__font_small, self.__color_blue)
        )

        b_model_right = Button(
            (offset_x+709, offset_y+65+row_height*1), (36, 36), (3, 6, 6, 3), 
            self.player_stats.switch_ship_model_to_next
        )
        b_model_right.add_element(
            Text(">", (12, 5), self.__font_small, self.__color_blue)
        )
        # Heal
        b_heal = Button(
           (offset_x+709, offset_y+65+row_height*2), (36, 36), (3, 6, 6, 3),
            self.player.buy_heal,
            self.player.can_heal
        )
        b_heal.set_outline_color(self.__color_green)
        b_heal.add_element(
            Text("/\\", (5, 5), self.__font_small, self.__color_green)
        )
        # Magnet
        b_magnet_rad = Button(
            (offset_x+709, offset_y+65+row_height*4), (36, 36), (3, 6, 6, 3),
            lambda: self.player.buy_upgrade(ShipUpgrade.MAGNET_RADIUS),
            lambda: self.player.can_buy_upgrade(ShipUpgrade.MAGNET_RADIUS)
        )
        b_magnet_rad.set_outline_color(self.__color_green)
        b_magnet_rad.add_element(
            Text("/\\", (5, 5), self.__font_small, self.__color_green)
        )

        b_magnet_str = Button(
            (offset_x+709, offset_y+65+row_height*5), (36, 36), (3, 6, 6, 3),
            lambda: self.player.buy_upgrade(ShipUpgrade.MAGNET_STRENGTH),
            lambda: self.player.can_buy_upgrade(ShipUpgrade.MAGNET_STRENGTH)
        )
        b_magnet_str.set_outline_color(self.__color_green)
        b_magnet_str.add_element(
            Text("/\\", (5, 5), self.__font_small, self.__color_green)
        )

        # Upgrade weapons
        b_weapon_1_up = Button(
            (offset_x+1179, offset_y+65+row_height*2), (36, 36), (3, 6, 6, 3),
            lambda: self.player.buy_upgrade(ShipUpgrade.PLASMAGUN_PROJECTILES),
            lambda: self.player.can_buy_upgrade(ShipUpgrade.PLASMAGUN_PROJECTILES)
        )
        b_weapon_1_up.set_outline_color(self.__color_green)
        b_weapon_1_up.add_element(
            Text("/\\", (5, 5), self.__font_small, self.__color_green)
        )
        
        b_weapon_2_up = Button(
            (offset_x+1179, offset_y+65+row_height*4), (36, 36), (3, 6, 6, 3),
            lambda: self.player.buy_upgrade(ShipUpgrade.BOMBLAUNCHER_RADIUS),
            lambda: self.player.can_buy_upgrade(ShipUpgrade.BOMBLAUNCHER_RADIUS)
        )
        b_weapon_2_up.set_outline_color(self.__color_green)
        b_weapon_2_up.add_element(
            Text("/\\", (5, 5), self.__font_small, self.__color_green)
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
            Text("SHIFT+Click to end the run early", (0, 0), self.__font_very_small, self.__color_white)
        )
        b_end_run.add_element(
            Text("End Run", (54, 10), self.__font_big, self.__color_red)
        )

        self.__buttons_pause_menu.extend(
            [b_model_left, b_model_right, b_heal, b_magnet_rad, b_magnet_str,
             b_weapon_1_up, b_weapon_2_up, b_end_run, s_auto_shoot]
        )

    def __initialize_name_check(self):
        self.__containers_name_check : list[Container] = []
        self.__buttons_name_check : list[Button | Switch] = []

        root_x = self.game.screen_resolution[0]/2-225
        root_y = self.game.screen_resolution[1]/2-105
        
        # <> Containers <>

        c_background = Container((root_x, root_y), (450, 210), (10, 25, 10, 25))
        c_background.add_element(
            TextF("New record! {}pts", (15, 7), self.__font_medium, self.__color_white, 
                  self.game.rsm.score)
        )
        c_background.add_element(
            Text("Enter your name:", (15, 47), self.__font_medium, self.__color_white)
        )

        c_name = Container((root_x+10, root_y+90), (430, 50), (3, 10, 3, 10))
        c_name.add_element(
            TextH("{}", (10, 10), self.__font_medium, self.__color_white, 
                  lambda: self.player_stats.name)
        )

        self.__containers_name_check.extend(
            [c_background, c_name]
        )
        
        # <> Buttons <>

        b_confirm = Button(
            (root_x+125, root_y+150), (200, 50), (3, 10, 3, 10),
            self.game.finish_getting_player_name
        )
        b_confirm.add_element(
            Text("Confirm", (10, 8), self.__font_medium, self.__color_blue)
        )

        self.__buttons_name_check.extend(
            [b_confirm]
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
