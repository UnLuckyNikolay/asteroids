# pyright: reportAttributeAccessIssue=false

import pygame, pygame.gfxdraw, json
from enum import Enum

from constants import *
from ui.button import Button


class Menu(Enum):
    MAIN_MENU = 1
    GAME_UI = 2
    PAUSE_MENU = 3
    LEADERBOARDS = 4

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

        # Buttons
        self.button_big_height = 72 # REMOVE
        self.button_big_width = 340 # REMOVE
        self.buttons_main_menu = (
            Button(SCREEN_WIDTH / 2 - 170, 200, 340, 72, 8, 8, 20, 20, self.font_big, "Start", 114, lambda: self.game.game_loop()),
            Button(SCREEN_WIDTH / 2 - 170, 300, 340, 72, 8, 8, 20, 20, self.font_big, "Leaderboard", 16, lambda: self.switch_menu(Menu.LEADERBOARDS)),
        )
        self.buttons_leaderboard = (
            Button(100, 68, 100, 36, 15, 3, 3, 15, self.font_small, "Back", 15, lambda: self.switch_menu(Menu.MAIN_MENU)),
        )

    def switch_menu(self, menu : Menu):
        self.__current_menu = menu
    
    def check_click(self, position, list = None):
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
            
            #case Menu.GAME_UI:

            case _:
                print("How are you here? This menu shouldn't have BUTTONS!")

    ### Drawing menus

    def draw(self, screen):
        match self.__current_menu:
            case Menu.MAIN_MENU:
                self.draw_main_menu(screen)
            case Menu.LEADERBOARDS:
                self.draw_leaderboards(screen)
            case Menu.GAME_UI:
                self.draw_game_ui(screen)
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
            
    def draw_game_ui(self, screen):
        info_weapon = self.font_small.render(f"Weapon: {self.player.weapon.get_name()}", True, (200, 200, 200, self.alpha))
        self.draw_container(screen, 25, 25, 36, 320, 10, 10, 5, 5)
        screen.blit(info_weapon, (34, 32))

        info_score = self.font_small.render(f"Score: {self.gsm.score}", False, (200, 200, 200, self.alpha))
        self.draw_container(screen, 25, 71, 36, 155, 5, 3, 5, 10)
        screen.blit(info_score, (34, 78))

        info_lives = self.font_small.render(f"Lives", False, (200, 200, 200, self.alpha))
        self.draw_container(screen, 190, 71, 36, 155, 3, 5, 10, 5)
        screen.blit(info_lives, (199, 78))

        if self.gsm.lives == 3:
            self.draw_polygon(screen, 272, 76, 26, 20, 2, 0, 0, 2, (0, 255, 0))
            self.draw_polygon(screen, 296, 76, 26, 20, 0, 0, 0, 0, (0, 255, 0))
            self.draw_polygon(screen, 320, 76, 26, 20, 0, 2, 6, 0, (0, 255, 0))
        elif self.gsm.lives == 2:
            self.draw_polygon(screen, 272, 76, 26, 20, 2, 0, 0, 2, (255, 255, 0))
            self.draw_polygon(screen, 296, 76, 26, 20, 0, 2, 2, 0, (255, 255, 0))
        elif self.gsm.lives == 1:
            self.draw_polygon(screen, 272, 76, 26, 20, 2, 2, 2, 2, (255, 0, 0))

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