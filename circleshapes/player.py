import pygame, pygame.gfxdraw, copy, math
from constants import *
from circleshape import CircleShape
from circleshapes.shot import Shot


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 180
        self.timer_shot = 0
        self.timer_invul = 0
        self.is_invul = False
        self.color_outline = list(PLAYER_COLOR_OUTLINE)
        self.color_fill = list(PLAYER_COLOR_FILL)
        self.level_gun = 1
        
        self.parts = [[[-25, 4], [25, 4], [22, -5], [0, -11], [-22, -5]], # Wings
                      [[20, 4], [20, 9]], [[-20, 4], [-20, 9]], # Wing guns
                      [[15, 0], [-15, 0], [-10, -12], [10, -12]], # Center part
                      [[-5, -12], [5, -12], [8, -20], [-8, -20]], # Engine
                      [[7, 0], [-7, 0], [-4, 18], [4, 18]], # Cockpit
                      [[0, 18], [0, 23]] # Gun
                      ]
        
        self.rotated_sprite = self.rotate_sprite()
    

    def draw(self, screen):
        pygame.draw.circle(screen, (50, 50, 50), self.position, 1, 2)
        pygame.draw.circle(screen, (50, 50, 50), self.position, self.radius, 2)   # Draws hit-box in dark gray.

        for part in self.rotated_sprite:
            if len(part) == 2:
                pygame.gfxdraw.line(screen, part[0][0], part[0][1], part[1][0], part[1][1], self.color_outline)
            elif len(part) > 2:
                pygame.gfxdraw.filled_polygon(screen, part, self.color_fill)
                pygame.gfxdraw.aapolygon(screen, part, self.color_outline)


    def rotate_sprite(self):
        new_sprite = []
        for part in self.parts:
            current_part = []
            for dot in part:
                dot_rotated = pygame.Vector2(dot).rotate(self.rotation)
                current_part.append((int(self.position.x + dot_rotated.x), int(self.position.y + dot_rotated.y)))
            new_sprite.append(current_part)
        return new_sprite


    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt


    def move(self, dt):
        self.position += pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SPEED * dt


    def shoot(self):
        if self.level_gun == 1 or self.level_gun == 3:
            self.spawn_bullet((0, 23))

        if self.level_gun == 2 or self.level_gun == 3:
            self.spawn_bullet((20, 9))
            self.spawn_bullet((-20, 9))

        self.timer_shot = 0

    
    def spawn_bullet(self, dot):
        spawn = pygame.Vector2(dot).rotate(self.rotation)
        shot = Shot(int(self.position.x + spawn.x), int(self.position.y + spawn.y))
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * SHOT_SPEED


    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.timer_shot += dt
        self.rotated_sprite = self.rotate_sprite()

        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE] and self.timer_shot > SHOT_COOLDOWN:
            self.shoot()

        if self.is_invul:
            if self.timer_invul > 0:
                for i in range(0, 4):
                    self.color_outline[i] = int(PLAYER_COLOR_OUTLINE[i] - min(self.timer_invul, PLAYER_TIMER_INVUL) / PLAYER_TIMER_INVUL * PLAYER_COLOR_OUTLINE[i])
                    self.color_fill[i] = int(PLAYER_COLOR_FILL[i] - min(self.timer_invul, PLAYER_TIMER_INVUL) / PLAYER_TIMER_INVUL * PLAYER_COLOR_FILL[i])
                self.timer_invul -= dt

            if self.timer_invul <= 0:
                self.timer_invul = 0
                self.is_invul = False
                self.color_outline = list(PLAYER_COLOR_OUTLINE)
                self.color_fill = list(PLAYER_COLOR_FILL)


    def got_shot(self, gameinfo):
        if gameinfo.lives > 0:
            gameinfo.lives -= 1
            self.timer_invul = 2
            self.is_invul = True
            return True
        else:
            print(f"Game over! Final score: {gameinfo.score}")
            return False
        