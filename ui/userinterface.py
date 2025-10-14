# pyright: reportAttributeAccessIssue=false

import pygame, json
from enum import Enum

from constants import *
from json_helper.leaderboards.validator import ValidateLeaderboards
from ui.container import Container, Allignment
from ui.button import Button
from ui.switch import Switch
from ui.text import Text, TextH, TextF
from ui.sprites.healthbar import HealthBar
from ui.sprites.leaderboards import Leaderboards
from ui.sprites.symbol_fullscreen import SymbolFullscreen
from gamestatemanager import GameStateManager
from player.player import Player, ShipPart


class Menu(Enum):
    MAIN_MENU = "Main Menu"
    LEADERBOARDS = "Leaderboards"
    HUD = "HUD"
    PAUSE_MENU = "Pause"
    NAME_CHECK = "Name check"

class UserInterface(pygame.sprite.Sprite):
    layer = 100 # pyright: ignore
    def __init__(self, game):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.game = game
        self.gsm : GameStateManager = None
        self.player : Player = None

        self.__current_menu : Menu = Menu.MAIN_MENU

        # Getting the font
        font_path = "./fonts/anita-semi-square.normaali.ttf" #"../../fonts/anita-semi-square.normaali.ttf"
        print(f"Trying to access file `{font_path}`")
        try:
            with open(font_path, "r"):
                pass
        except FileNotFoundError:
            print("Error: font not found")
            font_path = None
        
        # Getting the scores
        self.leaderboards_path = "./leaderboard.json"
        self.scores = ValidateLeaderboards(self.leaderboards_path)

        # Fonts
        self.font_small = pygame.font.Font(font_path, 24)
        self.font_medium = pygame.font.Font(font_path, 32)
        self.font_big = pygame.font.Font(font_path, 48)

        # Colors
        self.color_white = (200, 200, 200)
        self.color_gray = (100, 100, 100)
        self.color_blue = (100, 200, 255)
        self.color_red = (200, 0, 0)
        self.color_green = (0, 255, 0)
        self.color_golden = (255, 215, 0)

        self._initialize_main_menu()

    ### Buttons and containers

    def initialize_current_menu(self):
        match self.__current_menu:
            case Menu.MAIN_MENU:
                self._initialize_main_menu()
            case Menu.LEADERBOARDS:
                self._initialize_leaderboards()
            case Menu.HUD:
                self._initialize_hud()
            case Menu.PAUSE_MENU:
                self._initialize_pause_menu()
            case _:
                print(f"> Error: missing menu {self.__current_menu.value} in UserInterface.initialize_current_menu")

    def _initialize_main_menu(self):
        center_x = int((self.game.screen_resolution[0])/2)
        center_y = int((self.game.screen_resolution[1])/2)
        self.buttons_main_menu = (
            # Start button, starts a Round
            Button(center_x-185, center_y-136, 370, 72, 8, 8, 20, 20, 
                   self.game.game_loop,
                   lambda: True,
                   self.color_blue, self.color_gray,
                   (Text("Start", 117, 10, self.font_big, self.color_blue),
                           Allignment.NONE)),
            # Opens the Leaderboards
            Button(center_x-185, center_y-36, 370, 72, 8, 8, 20, 20, 
                   lambda: self.switch_menu(Menu.LEADERBOARDS),
                   lambda: True,
                   self.color_blue, self.color_gray,
                   (Text("Leaderboard", 16, 10, self.font_big, self.color_blue),
                           Allignment.NONE)),
            # Exits the game
            Button(center_x-185, center_y+64, 370, 72, 8, 8, 20, 20, 
                   self.game.handler_turn_off,
                   lambda: True,
                   self.color_blue, self.color_gray,
                   (Text("Exit", 135, 10, self.font_big, self.color_blue),
                           Allignment.NONE)),

            # Regenerate background
            Button(15, self.game.screen_resolution[1]-55, 40, 40, 8, 8, 8, 8,
                   self.game.handler_regenerate_background,
                   lambda: True,
                   self.color_blue, self.color_gray,
                   (Text("BG", 4, 7, self.font_small, self.color_blue),
                           Allignment.NONE)),
            # Switch Fullscreen
            Switch(70, self.game.screen_resolution[1]-55, 40, 40, 8, 8, 8, 8,
                   self.game.switch_fullscreen,
                   self.game.is_fullscreen,
                   self.color_green, self.color_blue,
                   (SymbolFullscreen(0, 0, self.color_blue), Allignment.CENTER)),

            # Cheat - Show hitbox
            Switch(self.game.screen_resolution[0]-165, self.game.screen_resolution[1]-55, 40, 40, 8, 8, 8, 8,
                   self.game.switch_hitbox,
                   self.game.cheat_hitbox,
                   self.color_golden, self.color_blue,
                   (Text("HB", 3, 7, self.font_small, self.color_blue),
                           Allignment.NONE)),
            # Cheat - Money cheat
            Switch(self.game.screen_resolution[0]-110, self.game.screen_resolution[1]-55, 40, 40, 8, 8, 8, 8,
                   self.game.switch_stonks,
                   self.game.cheat_stonks,
                   self.color_golden, self.color_blue,
                   (Text("MN", 2, 7, self.font_small, self.color_blue),
                           Allignment.NONE)),
            # Cheat - Godmode
            Switch(self.game.screen_resolution[0]-55, self.game.screen_resolution[1]-55, 40, 40, 8, 8, 8, 8,
                   self.game.switch_godmode,
                   self.game.cheat_godmode,
                   self.color_golden, self.color_blue,
                   (Text("GM", 2, 7, self.font_small, self.color_blue),
                           Allignment.NONE)),
        )

    def _initialize_leaderboards(self):
        self.buttons_leaderboards = (
            # Returns to the Main Menu
            Button(100, 68, 100, 36, 15, 3, 3, 15, 
                   lambda: self.switch_menu(Menu.MAIN_MENU),
                   lambda: True,
                   self.color_blue, self.color_gray,
                   (Text("Back", 18, 5, self.font_small, self.color_blue),
                           Allignment.NONE)),
        )
        self.containers_leaderboards = (
            # Name of the menu
            Container(self.game.screen_resolution[0] / 2 - 185, 35, 370, 72, 8, 8, 20, 20,
                      self.color_white,
                      (Text("Leaderboard", 16, 10, self.font_big, self.color_white),
                           Allignment.NONE)),
            # List of high scores
            Leaderboards(int(self.game.screen_resolution[0]/2)-540, 145, self.font_medium, self.scores)
        )

    def _initialize_hud(self):
        # Space between elements - 10
        self.containers_hud = (
            # Current weapon
            Container(25, 25, 548, 36, 10, 10, 5, 5, 
                      self.color_white,
                      (TextH("Weapon: {}.v{}", 9, 5, self.font_small, self.color_white, 
                           self.player.get_current_weapon_name,
                           self.player.get_current_weapon_level),
                           Allignment.NONE)),
            # Current score
            Container(25, 71, 176, 36, 5, 3, 5, 10, 
                      self.color_white,
                      (TextH("{}pts", 9, 5, self.font_small, self.color_white, 
                           self.gsm.get_score),
                           Allignment.NONE)),
            # Current money
            Container(211, 71, 176, 36, 3, 3, 3, 3, 
                      self.color_white,
                      (TextH("{}g", 9, 5, self.font_small, (235, 205, 0), 
                           self.player.get_money),
                           Allignment.NONE)),
            # Current health bar
            Container(397, 71, 176, 36, 3, 5, 10, 5, 
                      self.color_white,
                      (Text("Lives", 9, 5, self.font_small, self.color_white),
                            Allignment.NONE),
                      (HealthBar(102, 5, 2, 6,
                                self.player.get_lives),
                                Allignment.NONE)),
        )

    def _initialize_pause_menu(self):
        # Space between elements - 15
        offset_x = int((self.game.screen_resolution[0] - 1280)/2)
        offset_y = int((self.game.screen_resolution[1] - 720)/2)
        row_height = 51
        self.buttons_pause_menu = (
            # Model switching
            Button(offset_x+290, offset_y+65+row_height*1, 36, 36, 6, 3, 3, 6, 
                   self.player.switch_ship_model_to_previous,
                   lambda: True,
                   self.color_blue, self.color_gray,
                   (Text("<", 12, 5, self.font_small, self.color_blue),
                        Allignment.NONE)),
            Button(offset_x+709, offset_y+65+row_height*1, 36, 36, 3, 6, 6, 3, 
                   self.player.switch_ship_model_to_next,
                   lambda: True,
                   self.color_blue, self.color_gray,
                   (Text(">", 12, 5, self.font_small, self.color_blue),
                        Allignment.NONE)),
            # Heal
            Button(offset_x+709, offset_y+65+row_height*2, 36, 36, 3, 6, 6, 3,
                   self.player.buy_heal,
                   self.player.can_heal,
                   self.color_green, self.color_gray,
                   (Text("/\\", 5, 5, self.font_small, self.color_green),
                        Allignment.NONE)),
            # Magnet
            Button(offset_x+709, offset_y+65+row_height*4, 36, 36, 3, 6, 6, 3,
                   lambda: self.player.buy_upgrade(ShipPart.MAGNETRADIUS),
                   lambda: self.player.can_buy_upgrade(ShipPart.MAGNETRADIUS),
                   self.color_green, self.color_gray,
                   (Text("/\\", 5, 5, self.font_small, self.color_green),
                        Allignment.NONE)),

            # Upgrade weapons
            Button(offset_x+1179, offset_y+65+row_height*2, 36, 36, 3, 6, 6, 3,
                   lambda: self.player.buy_upgrade(ShipPart.WEAPON1),
                   lambda: self.player.can_buy_upgrade(ShipPart.WEAPON1),
                   self.color_green, self.color_gray,
                   (Text("/\\", 5, 5, self.font_small, self.color_green),
                        Allignment.NONE)),
            Button(offset_x+1179, offset_y+65+row_height*4, 36, 36, 3, 6, 6, 3,
                   lambda: self.player.buy_upgrade(ShipPart.WEAPON2),
                   lambda: self.player.can_buy_upgrade(ShipPart.WEAPON2),
                   self.color_green, self.color_gray,
                   (Text("/\\", 5, 5, self.font_small, self.color_green),
                        Allignment.NONE)),

            # Ends the run and returns to the main menu
            Button(offset_x+890, offset_y+600, 340, 72, 8, 8, 20, 20,
                   self.game.handler_finish_round,
                   lambda: True,
                   self.color_red, self.color_gray,
                   (Text("End Run", 54, 10, self.font_big, self.color_red),
                        Allignment.NONE)),
        )
        self.containers_pause_menu = (
            # Background
            Container(offset_x+50, offset_y+50, 1180, 540, 20, 20, 8, 20,
                      self.color_white),
                    
            # Current ship
            Container(offset_x+65, offset_y+65, 210, 210, 12, 6, 6, 6,
                      self.color_white,
                      (self.player.get_ship,
                            Allignment.CENTER)),

            # List - ship
            Container(offset_x+290, offset_y+65, 455, 36, 6, 6, 6, 6,
                      self.color_white,
                      (TextH("Model: {}", 12, 5, self.font_small, self.color_white,
                            self.player.get_ship_name),
                            Allignment.NONE)),
            Container(offset_x+336, offset_y+65+row_height*1, 363, 36, 3, 3, 3, 3,
                      self.color_white,
                      (Text("Switch model", 12, 5, self.font_small, self.color_white),
                            Allignment.NONE)),
            Container(offset_x+290, offset_y+65+row_height*2, 409, 36, 6, 3, 3, 6,
                      self.color_white,
                      (TextH("Heal: {}g", 12, 5, self.font_small, self.color_white,
                            self.player.get_price_heal),
                            Allignment.NONE)),
            Container(offset_x+290, offset_y+65+row_height*3, 455, 36, 6, 6, 6, 6,
                      self.color_white,
                      (TextH("Magnet.r{}", 12, 5, self.font_small, self.color_white,
                            lambda: self.player.get_upgrade_level(ShipPart.MAGNETRADIUS)),
                            Allignment.NONE)),
            Container(offset_x+290, offset_y+65+row_height*4, 409, 36, 6, 3, 3, 6,
                      self.color_white,
                      (TextH("Radius: {}g", 12, 5, self.font_small, self.color_white,
                            lambda: self.player.get_upgrade_price(ShipPart.MAGNETRADIUS)),
                            Allignment.NONE)),

            # Current stats
            Container(offset_x+760, offset_y+65, 150, 36, 6, 3, 3, 6, # Current score
                      self.color_white,
                      (TextH("{}pts", 9, 5, self.font_small, self.color_white, 
                           self.gsm.get_score),
                           Allignment.NONE)),
            Container(offset_x+920, offset_y+65, 127, 36, 3, 3, 3, 3, # Current money
                      self.color_white,
                      (TextH("{}g", 9, 5, self.font_small, (235, 205, 0), 
                           self.player.get_money),
                           Allignment.NONE)),
            Container(offset_x+1057, offset_y+65, 158, 36, 3, 6, 6, 3, # Current health bar
                      self.color_white,
                      (Text("Lives", 9, 5, self.font_small, self.color_white),
                            Allignment.NONE),
                      (HealthBar(84, 5, 2, 2,
                                self.player.get_lives),
                                Allignment.NONE)),
            # List - weapons
            Container(offset_x+760, offset_y+65+row_height*1, 455, 36, 6, 6, 6, 6,
                      self.color_white,
                      (TextH("Weapon 1: {}.v{}", 12, 5, self.font_small, self.color_white,
                            self.player.weapons[0].get_name,
                            lambda: self.player.get_upgrade_level(ShipPart.WEAPON1)),
                            Allignment.NONE)),
            Container(offset_x+760, offset_y+65+row_height*2, 409, 36, 6, 3, 3, 6,
                      self.color_white,
                      (TextH("Projectiles: {}g", 12, 5, self.font_small, self.color_white,
                            lambda: self.player.get_upgrade_price(ShipPart.WEAPON1)),
                            Allignment.NONE)),
            Container(offset_x+760, offset_y+65+row_height*3, 455, 36, 6, 6, 6, 6,
                      self.color_white,
                      (TextH("Weapon 2: {}.v{}", 12, 5, self.font_small, self.color_white,
                            self.player.weapons[1].get_name,
                            lambda: self.player.get_upgrade_level(ShipPart.WEAPON2)),
                            Allignment.NONE)),
            Container(offset_x+760, offset_y+65+row_height*4, 409, 36, 6, 3, 3, 6,
                      self.color_white,
                      (TextH("Radius: {}g", 12, 5, self.font_small, self.color_white,
                            lambda: self.player.get_upgrade_price(ShipPart.WEAPON2)),
                            Allignment.NONE)),
        )

    def _initialize_name_check(self):
        root_x = self.game.screen_resolution[0]/2-225
        root_y = self.game.screen_resolution[1]/2-105

        self.buttons_name_check = [
            Button(root_x+125, root_y+150, 200, 50, 3, 10, 3, 10,
                   self.game.finish_getting_player_name,
                   lambda: True, 
                   self.color_blue, self.color_gray,
                   (Text("Confirm", 10, 8, 
                         self.font_medium, self.color_blue),
                         Allignment.NONE)),
        ]
        self.containers_name_check = [
            Container(root_x, root_y, 450, 210, 10, 25, 10, 25, 
                      self.color_white,
                      (TextF("New record! {}pts", 15, 7, 
                            self.font_medium, self.color_white, 
                            self.game.gsm.score),
                            Allignment.NONE),
                      (Text("Enter your name:", 15, 47, 
                            self.font_medium, self.color_white), 
                            Allignment.NONE)),
            Container(root_x+10, root_y+90, 430, 50, 3, 10, 3, 10, 
                      self.color_white,
                      (TextH("{}", 10, 10, 
                            self.font_medium, self.color_white, 
                            lambda: self.game.player_name),
                            Allignment.NONE)),
        ]

    
    def start_round(self, gsm, player):
        self.gsm = gsm
        self.player = player
        self.switch_menu(Menu.HUD)

    def switch_menu(self, menu : Menu):
        self.__current_menu = menu

        match menu:
            case Menu.MAIN_MENU:
                self._initialize_main_menu()
            case Menu.LEADERBOARDS:
                self._initialize_leaderboards()
            case Menu.HUD:
                self._initialize_hud()
            case Menu.PAUSE_MENU:
                self._initialize_pause_menu()
            case Menu.NAME_CHECK:
                self._initialize_name_check()
            case _:
                print(f"> Error: missing menu {self.__current_menu.value} in UserInterface.switch_menu")
    
    def check_click(self, position):
        """Checks mouse position against all the buttons in the current menus and tries to run the button function."""
        match self.__current_menu:
            case Menu.MAIN_MENU:
                for button in self.buttons_main_menu:
                    if button.check_click(position):
                        button.run_if_possible()
                        return
            
            case Menu.LEADERBOARDS:
                for button in self.buttons_leaderboards:
                    if button.check_click(position):
                        button.run_if_possible()
                        return
            
            case Menu.HUD:
                pass # No buttons planned for HUD
            
            case Menu.PAUSE_MENU:
                for button in self.buttons_pause_menu:
                    if button.check_click(position):
                        button.run_if_possible()
                        return
            
            case Menu.NAME_CHECK:
                for button in self.buttons_name_check:
                    if button.check_click(position):
                        button.run_if_possible()
                        return

            case _:
                print("How are you here? This menu shouldn't have BUTTONS!")

    def check_score(self, new_score):
        is_updated = False

        while len(self.scores) > LEADERBOARD_LENGTH:   # Shortens leaderboard if max length was reduced
            is_updated = True
            self.scores.pop()
        
        if len(self.scores) == LEADERBOARD_LENGTH and new_score > self.scores[LEADERBOARD_LENGTH - 1]["score"]:
            is_updated = True
            self.scores.pop()
        if len(self.scores) != LEADERBOARD_LENGTH:
            is_updated = True
            self.game.get_player_name()
            self.scores.append({"name": self.game.player_name, "score": new_score})
            self.scores.sort(key=lambda x: x["score"], reverse=True)

        if not is_updated:
            return

        print(f"Saving leaderboards to `{self.leaderboards_path}`")
        with open(self.leaderboards_path, "w") as file:
            json.dump(self.scores, file)

        self._initialize_leaderboards()

    ### Drawing menus

    def draw(self, screen):
        match self.__current_menu:
            case Menu.MAIN_MENU:
                self.draw_main_menu(screen)
            case Menu.LEADERBOARDS:
                self.draw_leaderboards(screen)
            case Menu.HUD:
                self.draw_hud(screen)
            case Menu.PAUSE_MENU:
                self.draw_pause_menu(screen)
            case Menu.NAME_CHECK:
                self.draw_name_check(screen)
            case _:
                print(f"> Error: missing menu {self.__current_menu.value} in UserInterface.draw")        

    def draw_main_menu(self, screen):
        for button in self.buttons_main_menu:
            button.draw(screen)

    def draw_leaderboards(self, screen):
        for container in self.containers_leaderboards:
            container.draw(screen)

        for button in self.buttons_leaderboards:
            button.draw(screen)
            
    def draw_hud(self, screen):
        for container in self.containers_hud:
            container.draw(screen)

    def draw_pause_menu(self, screen):
        for container in self.containers_pause_menu:
            container.draw(screen)

        for button in self.buttons_pause_menu:
            button.draw(screen)

    def draw_name_check(self, screen):
        for container in self.containers_name_check:
            container.draw(screen)

        for button in self.buttons_name_check:
            button.draw(screen)
