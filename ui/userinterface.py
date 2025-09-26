# pyright: reportAttributeAccessIssue=false

import pygame, json
from enum import Enum

from constants import *
from ui.button import Button
from ui.container import Container
from ui.texth import TextH
from ui.sprites.healthbar import HealthBar
from ui.sprites.leaderboards import Leaderboards


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
        self.gsm = None
        self.player = None
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
        leaderboards_path = "./leaderboard.json"
        try:
            print(f"Trying to access file `{leaderboards_path}`")
            with open(leaderboards_path, "r") as file:
                self.scores = json.load(file)
        except FileNotFoundError:
            self.scores = []

        # Fonts
        self.font_small = pygame.font.Font(font_path, 24)
        self.font_medium = pygame.font.Font(font_path, 32)
        self.font_big = pygame.font.Font(font_path, 48)

        # Colors

        self.color_white = (200, 200, 200, 100)
        self.color_blue = (100, 200, 255, 100)
        self.color_red = (255, 0, 0, 100)

        # Buttons and containers
        self.buttons_main_menu = (
            # Start button, starts a Round
            Button(SCREEN_WIDTH / 2 - 185, 200, 370, 72, 8, 8, 20, 20, 
                   self.game.game_loop,
                   lambda: True,
                   self.color_blue,
                   TextH("Start", 117, 10, self.font_big, self.color_blue)),
            # Opens the Leaderboards
            Button(SCREEN_WIDTH / 2 - 185, 300, 370, 72, 8, 8, 20, 20, 
                   lambda: self.switch_menu(Menu.LEADERBOARDS),
                   lambda: True,
                   self.color_blue,
                   TextH("Leaderboard", 16, 10, self.font_big, self.color_blue)),
            # Exits the game
            Button(SCREEN_WIDTH / 2 - 185, 400, 370, 72, 8, 8, 20, 20, 
                   self.game.handler_turn_off,
                   lambda: True,
                   self.color_blue,
                   TextH("Exit", 135, 10, self.font_big, self.color_blue)),
            Button(15, SCREEN_HEIGHT-55, 40, 40, 8, 8, 8, 8,
                   self.game.handler_regenerate_background,
                   lambda: True,
                   self.color_blue,
                   TextH("BG", 4, 7, self.font_small, self.color_blue))
        )

        self.buttons_leaderboard = (
            # Returns to the Main Menu
            Button(100, 68, 100, 36, 15, 3, 3, 15, 
                   lambda: self.switch_menu(Menu.MAIN_MENU),
                   lambda: True,
                   self.color_blue,
                   TextH("Back", 18, 5, self.font_small, self.color_blue)),
        )
        self.containers_leaderboard = (
            # Name of the menu
            Container(SCREEN_WIDTH / 2 - 185, 35, 370, 72, 8, 8, 20, 20,
                      self.color_white,
                      TextH("Leaderboard", 16, 10, self.font_big, self.color_white)),
            # List of high scores
            Leaderboards(100, 145, self.font_medium, self.scores)
        )

        self.containers_hud = (
            # Current weapon
            Container(25, 25, 362, 36, 10, 10, 5, 5, 
                      self.color_white,
                      TextH("Weapon: {}", 9, 5, self.font_small, self.color_white, 
                           self.game.get_current_weapon_name)),
            # Current score
            Container(25, 71, 176, 36, 5, 3, 5, 10, 
                      self.color_white,
                      TextH("Score: {}", 9, 5, self.font_small, self.color_white, 
                           self.game.get_current_score)),
            # Current health bar
            Container(211, 71, 176, 36, 3, 5, 10, 5, 
                      self.color_white,
                      TextH("Lives", 9, 5, self.font_small, self.color_white),
                      HealthBar(103, 5, 
                                self.game.get_current_lives)),
        )

        self.buttons_pause_menu = (
            # Ends the run and returns to the main menu
            Button(SCREEN_WIDTH - 390, SCREEN_HEIGHT - 122, 340, 72, 8, 8, 20, 20,
                   self.game.handler_finish_round,
                   lambda: True,
                   self.color_red,
                   TextH("End Run", 54, 10, self.font_big, self.color_red)),
        )

    def switch_menu(self, menu : Menu):
        self.__current_menu = menu
        print(f"Switching to {self.__current_menu.value}")
    
    def check_click(self, position):
        match self.__current_menu:
            case Menu.MAIN_MENU:
                for button in self.buttons_main_menu:
                    if button.check_click(position):
                        button.run_if_possible()
                        return
            
            case Menu.LEADERBOARDS:
                for button in self.buttons_leaderboard:
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

            case _:
                print("How are you here? This menu shouldn't have BUTTONS!")

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
        for button in self.buttons_leaderboard:
            button.draw(screen)

        for container in self.containers_leaderboard:
            container.draw(screen)
            
    def draw_hud(self, screen):
        for container in self.containers_hud:
            container.draw(screen)

    def draw_pause_menu(self, screen):
        for button in self.buttons_pause_menu:
            button.draw(screen)
