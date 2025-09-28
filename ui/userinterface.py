# pyright: reportAttributeAccessIssue=false

import pygame, json
from enum import Enum
from tkinter import Tk, simpledialog

from constants import *
from ui.button import Button
from ui.container import Container, Allignment
from ui.text import Text, TextH, TextF
from ui.sprites.healthbar import HealthBar
from ui.sprites.leaderboards import Leaderboards
from gamestatemanager import GameStateManager
from player.player import Player


class Menu(Enum):
    MAIN_MENU = "Main Menu"
    HUD = "HUD"
    PAUSE_MENU = "Pause"
    LEADERBOARDS = "Leaderboards"

class UserInterface(pygame.sprite.Sprite):
    layer = 100 # pyright: ignore
    def __init__(self, game):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.game = game
        self.gsm :GameStateManager = None
        self.player : Player = None

        self.force_ui_reload = True
        self.__current_menu : Menu = Menu.MAIN_MENU

        # Getting the font
        font_path = "./fonts/anita-semi-square.normaali.ttf" #"../../fonts/anita-semi-square.normaali.ttf"
        try:
            print(f"Trying to access file `{font_path}`")
            with open(font_path, "r"):
                pass
        except FileNotFoundError:
            print("Error: font not found")
            font_path = None
        
        # Getting the scores
        self.leaderboards_path = "./leaderboard.json"
        try:
            print(f"Trying to access file `{self.leaderboards_path}`")
            with open(self.leaderboards_path, "r") as file:
                self.scores = json.load(file)
        except FileNotFoundError:
            self.scores = []

        # Fonts
        self.font_small = pygame.font.Font(font_path, 24)
        self.font_medium = pygame.font.Font(font_path, 32)
        self.font_big = pygame.font.Font(font_path, 48)

        # Colors
        self.color_white = (200, 200, 200)
        self.color_gray = (100, 100, 100)
        self.color_blue = (100, 200, 255)
        self.color_red = (255, 0, 0)
        self.color_green = (0, 255, 0)

        self._initialize_main_menu()

    ### Buttons and containers

    def _initialize_main_menu(self):
        self.buttons_main_menu = (
            # Start button, starts a Round
            Button(SCREEN_WIDTH / 2 - 185, 200, 370, 72, 8, 8, 20, 20, 
                   self.game.game_loop,
                   lambda: True,
                   self.color_blue, self.color_gray,
                   (Text("Start", 117, 10, self.font_big, self.color_blue),
                           Allignment.NONE)),
            # Opens the Leaderboards
            Button(SCREEN_WIDTH / 2 - 185, 300, 370, 72, 8, 8, 20, 20, 
                   lambda: self.switch_menu(Menu.LEADERBOARDS),
                   lambda: True,
                   self.color_blue, self.color_gray,
                   (Text("Leaderboard", 16, 10, self.font_big, self.color_blue),
                           Allignment.NONE)),
            # Exits the game
            Button(SCREEN_WIDTH / 2 - 185, 400, 370, 72, 8, 8, 20, 20, 
                   self.game.handler_turn_off,
                   lambda: True,
                   self.color_blue, self.color_gray,
                   (Text("Exit", 135, 10, self.font_big, self.color_blue),
                           Allignment.NONE)),
            Button(15, SCREEN_HEIGHT-55, 40, 40, 8, 8, 8, 8,
                   self.game.handler_regenerate_background,
                   lambda: True,
                   self.color_blue, self.color_gray,
                   (Text("BG", 4, 7, self.font_small, self.color_blue),
                           Allignment.NONE))
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
            Container(SCREEN_WIDTH / 2 - 185, 35, 370, 72, 8, 8, 20, 20,
                      self.color_white,
                      (Text("Leaderboard", 16, 10, self.font_big, self.color_white),
                           Allignment.NONE)),
            # List of high scores
            Leaderboards(100, 145, self.font_medium, self.scores)
        )

    def _initialize_hud(self):
        self.containers_hud = (
            # Current weapon
            Container(25, 25, 548, 36, 10, 10, 5, 5, 
                      self.color_white,
                      (TextH("Weapon: {}", 9, 5, self.font_small, self.color_white, 
                           self.player.get_weapon_name),
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
                      (HealthBar(103, 5, 
                                self.player.get_lives),
                                Allignment.NONE)),
        )

    def _initialize_pause_menu(self):
        self.buttons_pause_menu = (
            # Ends the run and returns to the main menu
            Button(890, 600, 340, 72, 8, 8, 20, 20,
                   self.game.handler_finish_round,
                   lambda: True,
                   self.color_red, self.color_gray,
                   (Text("End Run", 54, 10, self.font_big, self.color_red),
                        Allignment.NONE)),
            # Heal
            Button(709, 116, 36, 36, 6, 6, 6, 6,
                   self.player.buy_heal,
                   self.player.can_heal,
                   self.color_green, self.color_gray,
                   (Text("/\\", 5, 5, self.font_small, self.color_green),
                        Allignment.NONE)),
            # Upgrade weapons
            Button(1179, 116, 36, 36, 6, 6, 6, 6,
                   lambda: self.player.buy_upgrade_weapon(0),
                   lambda: self.player.can_upgrade_weapon(0),
                   self.color_green, self.color_gray,
                   (Text("/\\", 5, 5, self.font_small, self.color_green),
                        Allignment.NONE)),
        )
        self.containers_pause_menu = (
            # Background
            Container(50, 50, 1180, 540, 20, 20, 8, 20,
                      self.color_white),
            # Current ship
            Container(65, 65, 210, 210, 12, 6, 6, 6,
                      self.color_white,
                      (self.player.get_ship,
                            Allignment.CENTER)),
            # List - ship
            Container(290, 65, 455, 36, 6, 6, 6, 6,
                      self.color_white,
                      (TextH("Model: {}", 12, 5, self.font_small, self.color_white,
                            self.player.get_ship_name),
                            Allignment.NONE)),
            Container(290, 116, 404, 36, 6, 6, 6, 6,
                      self.color_white,
                      (TextH("Heal: {}g", 12, 5, self.font_small, self.color_white,
                            self.player.get_price_heal),
                            Allignment.NONE)),
            # List - weapons
            Container(760, 65, 455, 36, 6, 12, 6, 6,
                      self.color_white,
                      (TextH("Weapon 1: {}.v{}", 12, 5, self.font_small, self.color_white,
                            self.player.weapons[0].get_name,
                            self.player.weapons[0].get_level),
                            Allignment.NONE)),
            Container(760, 116, 404, 36, 6, 6, 6, 6,
                      self.color_white,
                      (TextH("Projectiles: {}g", 12, 5, self.font_small, self.color_white,
                            lambda: self.player.get_price_weapons(0)),
                            Allignment.NONE)),
        )

    
    def round_start(self, gsm, player):
        self.gsm = gsm
        self.player = player
        self._initialize_hud()
        self._initialize_pause_menu()

    def switch_menu(self, menu : Menu):
        match menu:
            case Menu.LEADERBOARDS:
                self._initialize_leaderboards()

        self.__current_menu = menu
        print(f"Switching to {self.__current_menu.value}")
    
    def check_click(self, position):
        """Checks mouse position against all the buttons in the current menus and tries to run the button function."""
        match self.__current_menu:
            case Menu.MAIN_MENU:
                for button in self.buttons_main_menu:
                    if button.check_click(position):
                        if button.run_if_possible():
                            self.force_ui_reload = True
                        return
            
            case Menu.LEADERBOARDS:
                for button in self.buttons_leaderboards:
                    if button.check_click(position):
                        if button.run_if_possible():
                            self.force_ui_reload = True
                        return
            
            case Menu.HUD:
                pass # No buttons planned for HUD
            
            case Menu.PAUSE_MENU:
                for button in self.buttons_pause_menu:
                    if button.check_click(position):
                        if button.run_if_possible():
                            self.force_ui_reload = True
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
            name = self.ask_player_name()
            self.scores.append({"name": name, "score": new_score})
            self.scores.sort(key=lambda x: x["score"], reverse=True)

        if not is_updated:
            return

        print(f"Saving leaderboards to `./{self.leaderboards_path}`")
        with open(self.leaderboards_path, "w") as file:
            json.dump(self.scores, file)

        self._initialize_leaderboards()

    def ask_player_name(self):
        root = Tk()
        root.withdraw()

        name = simpledialog.askstring("New record!", "Please enter your name: ")

        root.destroy()

        return name if name else "Player"

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
            case _:
                print("Menu not implemented yet!")        

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
