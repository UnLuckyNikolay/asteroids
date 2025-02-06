import pygame, pygame.gfxdraw, json
from constants import *


class UserInterface(pygame.sprite.Sprite):
    layer = 100
    def __init__(self):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.game = None
        self.player = None

        self.alpha = 100
        self.font_small = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_big = pygame.font.Font(None, 72)

        self.button_big_height = 72
        self.button_big_width = 340
        self.buttons_main_menu = (
            (((SCREEN_WIDTH / 2 - 170), 200), ((SCREEN_WIDTH / 2 - 170 + self.button_big_width), (200 + self.button_big_height))),   # Start
            (((SCREEN_WIDTH / 2 - 170), 300), ((SCREEN_WIDTH / 2 - 170 + self.button_big_width), (300 + self.button_big_height))),   # Leaderboard
        )
        self.buttons_leaderboard =(
            ((50, 50), (150, 86)),  # Back
        )
        

    def draw_main_menu(self, screen):
        button_text = self.font_big.render("Start", True, (80, 180, 220, self.alpha))
        self.draw_button(screen, SCREEN_WIDTH / 2 - 170, 200, self.button_big_height, self.button_big_width, 8, 8, 20, 20)
        screen.blit(button_text, (SCREEN_WIDTH / 2 - 55, 215))

        button_text = self.font_big.render("Leaderboard", True, (80, 180, 220, self.alpha))
        self.draw_button(screen, SCREEN_WIDTH / 2 - 170, 300, self.button_big_height, self.button_big_width, 8, 8, 20, 20)
        screen.blit(button_text, (SCREEN_WIDTH / 2 - 153, 315))


    def draw_leaderboard(self, screen):
        name_text = self.font_big.render("Leaderboard", True, (200, 200, 200, self.alpha))
        self.draw_container(screen, SCREEN_WIDTH / 2 - 170, 35, self.button_big_height, self.button_big_width, 8, 8, 20, 20)
        screen.blit(name_text, (SCREEN_WIDTH / 2 - 153, 50))

        name_text = self.font_small.render("Back", True, (80, 180, 220, self.alpha))
        self.draw_button(screen, 50, 50, 36, 100, 15, 3, 3, 15)
        screen.blit(name_text, (65, 57))

        try:
            with open("leaderboard.json", "r") as file:
                scores = json.load(file)
        except FileNotFoundError:
            scores = []

        for i in range(0, min(len(scores), LEADERBOARD_LENGTH)):
            text = self.font_medium.render(f"{scores[i]["score"]} - {scores[i]["name"]}", True, (200, 200, 200, self.alpha))
            self.draw_container(screen, 100, (145 + 65 * i), 48, 1080, 15, 8, 15, 8)
            screen.blit(text, (115, (157 + 65 * i)))


    def check_click(self, position, list):
        for i in range(0, len(list)):
            if (position[0] > list[i][0][0] and
                position[0] < list[i][1][0] and
                position[1] > list[i][0][1] and
                position[1] < list[i][1][1]):
                return i + 1
        else:
            return 0
            

    # In-game UI
    def draw(self, screen):
        info_weapon = self.font_small.render(f"Weapon: {self.player.weapon.get_name()}", True, (200, 200, 200, self.alpha))
        self.draw_container(screen, 25, 25, 36, 320, 10, 10, 5, 5)
        screen.blit(info_weapon, (34, 32))

        info_score = self.font_small.render(f"Score: {self.game.score}", False, (200, 200, 200, self.alpha))
        self.draw_container(screen, 25, 71, 36, 155, 5, 3, 5, 10)
        screen.blit(info_score, (34, 78))

        info_lives = self.font_small.render(f"Lives", False, (200, 200, 200, self.alpha))
        self.draw_container(screen, 190, 71, 36, 155, 3, 5, 10, 5)
        screen.blit(info_lives, (199, 78))

        if self.game.lives == 3:
            self.draw_polygon(screen, 272, 76, 26, 20, 2, 0, 0, 2, (0, 255, 0))
            self.draw_polygon(screen, 296, 76, 26, 20, 0, 0, 0, 0, (0, 255, 0))
            self.draw_polygon(screen, 320, 76, 26, 20, 0, 2, 6, 0, (0, 255, 0))
        elif self.game.lives == 2:
            self.draw_polygon(screen, 272, 76, 26, 20, 2, 0, 0, 2, (255, 255, 0))
            self.draw_polygon(screen, 296, 76, 26, 20, 0, 2, 2, 0, (255, 255, 0))
        elif self.game.lives == 1:
            self.draw_polygon(screen, 272, 76, 26, 20, 2, 2, 2, 2, (255, 0, 0))


    def draw_container(self, screen, x, y, height, width, corner_topleft, corner_topright, corner_bottomright, corner_bottomleft):
        points = self.get_points(x, y, height, width, corner_topleft, corner_topright, corner_bottomright, corner_bottomleft)
        pygame.gfxdraw.filled_polygon(screen, points, (75, 75, 75, self.alpha))
        pygame.draw.polygon(screen, (255, 255, 255, self.alpha), points, 3)


    def draw_button(self, screen, x, y, height, width, corner_topleft, corner_topright, corner_bottomright, corner_bottomleft):
        points = self.get_points(x, y, height, width, corner_topleft, corner_topright, corner_bottomright, corner_bottomleft)
        pygame.gfxdraw.filled_polygon(screen, points, (75, 75, 75, self.alpha))
        pygame.draw.polygon(screen, (100, 200, 255, self.alpha), points, 3)


    def draw_polygon(self, screen, x, y, height, width, corner_topleft, corner_topright, corner_bottomright, corner_bottomleft, color):
        points = self.get_points(x, y, height, width, corner_topleft, corner_topright, corner_bottomright, corner_bottomleft)
        pygame.gfxdraw.filled_polygon(screen, points, (color[0], color[1], color[2], self.alpha))


    def get_points(self, x, y, height, width, corner_topleft, corner_topright, corner_bottomright, corner_bottomleft):
        points = [(x, y + corner_topleft),
                  (x + corner_topleft, y),
                  (x + width - corner_topright, y),
                  (x + width, y + corner_topright),
                  (x + width, y + height - corner_bottomright),
                  (x + width - corner_bottomright, y + height),
                  (x + corner_bottomleft, y + height),
                  (x, y + height - corner_bottomleft)]
        return points