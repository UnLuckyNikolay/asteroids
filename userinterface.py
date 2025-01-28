import pygame, pygame.gfxdraw


class UserInterface(pygame.sprite.Sprite):
    layer = 100
    def __init__(self, game, player):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.game = game
        self.player = player

        self.alpha = 100
        self.font = pygame.font.Font(None, 36)
        

    def draw(self, screen):
        info_weapon = self.font.render(f"Weapon: {self.player.weapon.get_name()}", True, (200, 200, 200, self.alpha))
        self.draw_container(screen, 25, 25, 36, 320, 10, 10, 5, 5)
        screen.blit(info_weapon, (34, 32))

        info_score = self.font.render(f"Score: {self.game.score}", False, (200, 200, 200, self.alpha))
        self.draw_container(screen, 25, 71, 36, 155, 5, 3, 5, 10)
        screen.blit(info_score, (34, 78))

        info_lives = self.font.render(f"Lives", False, (200, 200, 200, self.alpha))
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


    def draw_polygon(self, screen, x, y, height, width, corner_topleft, corner_topright, corner_bottomright, corner_bottomleft, color):
        points = self.get_points(x, y, height, width, corner_topleft, corner_topright, corner_bottomright, corner_bottomleft)
        pygame.gfxdraw.filled_polygon(screen, points, (color[0], color[1], color[2], self.alpha))


    def draw_health(self):
        pass


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