# pyright: reportAttributeAccessIssue=false

import pygame, pygame.gfxdraw, json
from enum import Enum

from constants import *
from ui.button import Button
from ui.container import Container
from ui.text import Text
from ui.sprites.healthbar import HealthBar


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

        # Fonts
        self.alpha = 100 # REMOVE
        self.font_small = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_big = pygame.font.Font(None, 72)

        # Buttons and containers
        self.button_big_height = 72 # REMOVE
        self.button_big_width = 340 # REMOVE

        self.buttons_main_menu = (
            Button(SCREEN_WIDTH / 2 - 170, 200, 340, 72, 8, 8, 20, 20, 
                   lambda: self.game.game_loop(),
                   lambda: True,
                   (100, 200, 255, 100),
                   Text("Start", 114, 14, self.font_big, (100, 200, 255, 100))),
            Button(SCREEN_WIDTH / 2 - 170, 300, 340, 72, 8, 8, 20, 20, 
                   lambda: self.switch_menu(Menu.LEADERBOARDS),
                   lambda: True,
                   (100, 200, 255, 100),
                   Text("Leaderboard", 16, 14, self.font_big, (100, 200, 255, 100))),
            Button(SCREEN_WIDTH / 2 - 170, 400, 340, 72, 8, 8, 20, 20, 
                   lambda: self.game.handler_turn_off(),
                   lambda: True,
                   (100, 200, 255, 100),
                   Text("Exit", 120, 14, self.font_big, (100, 200, 255, 100))),
        )

        self.buttons_leaderboard = (
            Button(100, 68, 100, 36, 15, 3, 3, 15, 
                   lambda: self.switch_menu(Menu.MAIN_MENU),
                   lambda: True,
                   (100, 200, 255, 100),
                   Text("Back", 15, 7, self.font_small, (100, 200, 255, 100))),
        )

        self.containers_hud = (
            Container(25, 25, 320, 36, 10, 10, 5, 5, 
                      (200, 200, 200, 100),
                      Text("Weapon: {}", 9, 7, self.font_small, (200, 200, 200, 100), 
                           self.game.get_current_weapon_name)),
            Container(25, 71, 155, 36, 5, 3, 5, 10, 
                      (200, 200, 200, 100),
                      Text("Score: {}", 9, 7, self.font_small, (200, 200, 200, 100), 
                           self.game.get_current_score)),
            Container(190, 71, 155, 36, 3, 5, 10, 5, 
                      (200, 200, 200, 100),
                      Text("Lives", 9, 7, self.font_small, (200, 200, 200, 100)),
                      HealthBar(82, 5, 
                                self.game.get_current_lives)),
        )

        self.buttons_pause_menu = (
            Button(SCREEN_WIDTH - 390, SCREEN_HEIGHT - 122, 340, 72, 8, 8, 20, 20,
                   lambda: self.game.handler_finish_round(),
                   lambda: True,
                   (255, 0, 0, 100),
                   Text("End Run", 65, 14, self.font_big, (255, 0, 0, 100))),
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
        name_text = self.font_big.render("Leaderboard", True, (200, 200, 200, self.alpha))
        self.draw_container(screen, SCREEN_WIDTH / 2 - 170, 35, self.button_big_height, self.button_big_width, 8, 8, 20, 20)
        screen.blit(name_text, (SCREEN_WIDTH / 2 - 153, 50))

        for button in self.buttons_leaderboard:
            button.draw(screen)

        try:
            with open("leaderboard.json", "r") as file:
                scores = json.load(file)
        except FileNotFoundError:
            scores = []
        
        for i in range(0, min(len(scores), LEADERBOARD_LENGTH)):
            text = self.font_medium.render(f"{scores[i]['score']} - {scores[i]['name']}", True, (200, 200, 200, self.alpha))
            self.draw_container(screen, 100, (145 + 65 * i), 48, 1080, 15, 8, 15, 8)
            screen.blit(text, (115, (157 + 65 * i)))
            
    def draw_hud(self, screen):
        for container in self.containers_hud:
            container.draw(screen)

    def draw_pause_menu(self, screen):
        for button in self.buttons_pause_menu:
            button.draw(screen)

    ### Polygons

    def draw_container(self, screen, x, y, height, width, corner_topleft, corner_topright, corner_bottomright, corner_bottomleft):
        points = self.get_points(x, y, height, width, corner_topleft, corner_topright, corner_bottomright, corner_bottomleft)
        pygame.gfxdraw.filled_polygon(screen, points, (75, 75, 75, self.alpha))
        pygame.draw.polygon(screen, (255, 255, 255, self.alpha), points, 3)

    def draw_polygon(self, screen, x, y, height, width, corner_topleft, corner_topright, corner_bottomright, corner_bottomleft, color):
        points = self.get_points(x, y, height, width, corner_topleft, corner_topright, corner_bottomright, corner_bottomleft)
        pygame.gfxdraw.filled_polygon(screen, points, (color[0], color[1], color[2], self.alpha))

    def get_points(self, x, y, height, width, corner_topleft, corner_topright, corner_bottomright, corner_bottomleft): # DELETE
        points = [(x, y + corner_topleft),
                  (x + corner_topleft, y),
                  (x + width - corner_topright, y),
                  (x + width, y + corner_topright),
                  (x + width, y + height - corner_bottomright),
                  (x + width - corner_bottomright, y + height),
                  (x + corner_bottomleft, y + height),
                  (x, y + height - corner_bottomleft)]
        return points