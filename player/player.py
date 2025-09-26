import pygame, pygame.gfxdraw

from constants import *
from shapes.circleshape import CircleShape
from player.weapons.plasmagun import PlasmaGun
from player.weapons.bomblauncher import BombLauncher
from ui.sprites.ship import Ship, ShipType


class Player(CircleShape):
    layer = 50 # pyright: ignore[reportAssignmentType]
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 180
        self.rotation_inertia = self.rotation
        self.inertia = pygame.Vector2(0, 0)
        self.__speed = 0
        self.__turning_speed = 0
        self.last_dt = 0

        self.timer_invul = 0
        self.is_invul = False
        self.is_alive = True

        self.ship = Ship(ShipType.POLY2)

        self.color_outline = list(PLAYER_COLOR_OUTLINE)
        self.color_fill = list(PLAYER_COLOR_FILL)
        self.color_glass = list(PLAYER_COLOR_GLASS)

        self.time_since_last_shot = 0
        self.weapons = []
        self.weapons.append(PlasmaGun())
        self.weapons.append(BombLauncher())
        self.weapon = self.weapons[0]
        
        # Each part is [[color_override],  [list of dots]]
        self.parts = [[[],  [[-25, 4], [25, 4], [22, -5], [0, -11], [-22, -5]]], # Wings
                      [[],  [[20, 4], [20, 9]]],   # Wing guns
                      [[],  [[-20, 4], [-20, 9]]], # ^
                      [[],  [[7, 0], [-7, 0], [-4, 18], [4, 18]]], # Cockpit
                      [self.color_glass,  [[5, -3], [-5, -3], [-2, 15], [2, 15]]], # Cockpit window
                      [[],  [[15, 0], [-15, 0], [-10, -12], [10, -12]]], # Center part
                      [[],  [[-5, -12], [5, -12], [8, -20], [-8, -20]]], # Engine
                      [[],  [[0, 18], [0, 23]]] # Gun
                      ]
        
        #self.rotated_sprite = self.rotate_sprite()
    

    @property
    def turning_speed(self):
        return self.__turning_speed
    
    @turning_speed.setter
    def turning_speed(self, value):
        if value < -PLAYER_TURNING_MAX:
            self.__turning_speed = -PLAYER_TURNING_MAX
        elif value > PLAYER_TURNING_MAX:
            self.__turning_speed = PLAYER_TURNING_MAX
        elif self.__turning_speed != 0 and abs(value) < PLAYER_TURNING_ACCELERATION and abs(self.__turning_speed) < PLAYER_TURNING_ACCELERATION:
            self.__turning_speed = 0
        else:
            self.__turning_speed = value


    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, value):
        if value < -PLAYER_SPEED_MAX:
            self.__speed = -PLAYER_SPEED_MAX
        elif value > PLAYER_SPEED_MAX:
            self.__speed = PLAYER_SPEED_MAX
        elif self.__speed != 0 and abs(value) < PLAYER_ACCELERATION and abs(self.__speed) < PLAYER_ACCELERATION:
            self.__speed = 0   # Stops the player the speed is very low during deseleration, might change later
            self.inertia = pygame.Vector2(0, 0)
        else:
            self.__speed = value 


    def draw(self, screen):
        self.ship.draw_rotated(screen, self.position.x, self.position.y, self.rotation+180)
        #if PLAYER_SHOW_HITBOX:   # Draws player hit box in dark gray.
        #    pygame.draw.circle(screen, (50, 50, 50), self.position, 1, 2)
        #    pygame.draw.circle(screen, (50, 50, 50), self.position, self.radius, 2)

        #for part in self.rotated_sprite:
        #    if len(part[1]) == 2:
        #        pygame.draw.line(screen, self.color_outline, part[1][0], part[1][1], 2)
        #    elif len(part[1]) > 2:
        #        if len(part[0]) == 0:
        #            pygame.gfxdraw.filled_polygon(screen, part[1], self.color_fill)
        #           pygame.draw.polygon(screen, self.color_outline, part[1], 2)
        #       else: 
        #            pygame.gfxdraw.filled_polygon(screen, part[1], part[0])


    #def rotate_sprite(self):
    #    rotated_sprite = []
    #    for part in self.parts:
    #        rotated_part = []
    #        for dot in part[1]:
    #            dot_rotated = pygame.Vector2(dot).rotate(self.rotation)
    #            rotated_part.append((int(self.position.x + dot_rotated.x), int(self.position.y + dot_rotated.y)))
    #       rotated_sprite.append([part[0], rotated_part])
    #    return rotated_sprite


    def rotate(self, dt):
        self.rotation += self.turning_speed * dt


    def move(self, dt):
        self.inertia = self.inertia * ((100 - PLAYER_ACCELERATION) / 100) + pygame.Vector2(0, 1).rotate(self.rotation_inertia) * (PLAYER_ACCELERATION / 100)
        self.position += self.inertia * self.speed * dt

        # Teleports player if off-screen
        if self.position.x < -ASTEROID_MAX_RADIUS:
            self.position.x = SCREEN_WIDTH + ASTEROID_MAX_RADIUS
        elif self.position.x > SCREEN_WIDTH + ASTEROID_MAX_RADIUS:
            self.position.x = -ASTEROID_MAX_RADIUS
        if self.position.y < -ASTEROID_MAX_RADIUS:
            self.position.y = SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
        elif self.position.y > SCREEN_HEIGHT + ASTEROID_MAX_RADIUS:
            self.position.y = -ASTEROID_MAX_RADIUS


    def attempt_shot(self, time_since_last_shot):
        return self.weapon.attempt_shot(self.position, self.rotation, time_since_last_shot)


    def update(self, dt):
        self.last_dt = dt
        keys = pygame.key.get_pressed()
        self.time_since_last_shot += dt
        #self.rotated_sprite = self.rotate_sprite()

        # Turning
        if self.turning_speed != 0:
            self.rotate(dt)
        if keys[pygame.K_d] and not keys[pygame.K_a]:
            self.turning_speed += PLAYER_TURNING_ACCELERATION
        elif keys[pygame.K_a] and not keys[pygame.K_d]:
            self.turning_speed -= PLAYER_TURNING_ACCELERATION
        else:   # Deceleration
            if self.turning_speed > 0:
                self.turning_speed -= int(PLAYER_TURNING_ACCELERATION / 2)
            elif self.turning_speed < 0:
                self.turning_speed += int(PLAYER_TURNING_ACCELERATION / 2)

        # Movement
        if self.speed != 0:
            self.move(dt)
        if keys[pygame.K_w] and not keys[pygame.K_s]:
            self.rotation_inertia = self.rotation
            self.speed += PLAYER_ACCELERATION
        elif keys[pygame.K_s] and not keys[pygame.K_w]:
            self.rotation_inertia = self.rotation
            self.speed -= PLAYER_ACCELERATION
        else:   # Deceleration
            if self.speed > 0:
                self.speed -= int(PLAYER_ACCELERATION / 2)
            elif self.speed < 0:
                self.speed += int(PLAYER_ACCELERATION / 2)

        # Weapon change
        if keys[pygame.K_1] and self.weapon.get_name() != self.weapons[0].get_name():
            self.weapon = self.weapons[0]
        elif keys[pygame.K_2] and self.weapon.get_name() != self.weapons[1].get_name():
            self.weapon = self.weapons[1]

        if keys[pygame.K_SPACE] and self.attempt_shot(self.time_since_last_shot):
            self.time_since_last_shot = 0

        if self.is_invul:
            if self.timer_invul > 0:
                for i in range(0, 4):
                    self.color_outline[i] = int(PLAYER_COLOR_OUTLINE[i] - min(self.timer_invul, PLAYER_TIMER_INVUL) / PLAYER_TIMER_INVUL * PLAYER_COLOR_OUTLINE[i])
                    self.color_fill[i] = int(PLAYER_COLOR_FILL[i] - min(self.timer_invul, PLAYER_TIMER_INVUL) / PLAYER_TIMER_INVUL * PLAYER_COLOR_FILL[i])
                    self.color_glass[i] = int(PLAYER_COLOR_GLASS[i] - min(self.timer_invul, PLAYER_TIMER_INVUL) / PLAYER_TIMER_INVUL * PLAYER_COLOR_GLASS[i])
                self.timer_invul -= dt

            if self.timer_invul <= 0:
                self.timer_invul = 0
                self.is_invul = False
                self.color_outline = list(PLAYER_COLOR_OUTLINE)
                self.color_fill = list(PLAYER_COLOR_FILL)


    def take_damage_and_check_if_alive(self, gameinfo):
        if PLAYER_GOD_MODE:
            return self.is_alive
        elif gameinfo.lives > 1:
            gameinfo.lives -= 1
            self.timer_invul = 2
            self.is_invul = True
            return self.is_alive
        else:
            gameinfo.lives -= 1
            self.is_alive = False
            print(f"Game over! Final score: {gameinfo.score}")
            return self.is_alive
        