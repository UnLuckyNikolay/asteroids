import pygame


class GameInfo():
    def __init__(self):
        self.score = 0
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.position = (30, 30)
        self.color = (150, 150, 150)


    def update(self, score):
        self.score = score


    def draw(self, screen):
        score_text = self.font.render(f"Score: {self.score}", True, self.color)
        screen.blit(score_text, self.position)