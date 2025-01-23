import pygame
from constants import *
from circleshape import CircleShape
from circleshapes.shot import Shot
from gameinfo import GameInfo


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer_shot = 0
        self.timer_invul = 0
        self.is_invul = False
        self.color = (255, 255, 255)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.triangle(), 2)


    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt


    def move(self, dt):
        self.position += pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SPEED * dt


    def shoot(self):
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * SHOT_SPEED


    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.timer_shot += dt

        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        #if keys[pygame.K_SPACE]:
        if keys[pygame.K_SPACE] and self.timer_shot > SHOT_COOLDOWN:
            self.shoot()
            self.timer_shot = 0

        if self.is_invul:
            if self.timer_invul > 0:
                color = int(255 - self.timer_invul / 2 * 255)
                self.color = (color, color, color)
                self.timer_invul -= dt

            if self.timer_invul <= 0:
                self.timer_invul = 0
                self.is_invul = False
                color = (255, 255, 255)


    def got_shot(self, gameinfo):
        if gameinfo.lives > 0:
            gameinfo.lives -= 1
            self.timer_invul = 2
            self.is_invul = True
            return True
        else:
            print(f"Game over! Final score: {gameinfo.score}")
            return False