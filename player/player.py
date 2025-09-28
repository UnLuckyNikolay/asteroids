import pygame, pygame.gfxdraw

from constants import *
from shapes.circleshape import CircleShape
from player.weapons.plasmagun import PlasmaGun
from player.weapons.bomblauncher import BombLauncher
from ui.sprites.ship import Ship, ShipType


class Player(CircleShape):
    layer = 50 # pyright: ignore
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

        self.ship = Ship(ShipType.POLY2, self.radius)
        self.money = 0
        self.lives = 3
        self.lives_max = 3
        self.times_healed = 0

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
        self.ship.draw_rotated(
            screen, 
            self.position.x, self.position.y,  # pyright: ignore[reportAttributeAccessIssue]
            self.rotation+180, self.timer_invul
        )

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
        if (keys[pygame.K_1] or keys[pygame.K_KP1]):
            self.weapon = self.weapons[0]
        elif (keys[pygame.K_2] or keys[pygame.K_KP2]):
            self.weapon = self.weapons[1]

        if keys[pygame.K_SPACE] and self.attempt_shot(self.time_since_last_shot):
            self.time_since_last_shot = 0

        if self.is_invul:
            if self.timer_invul > 0:
                self.timer_invul -= dt

            if self.timer_invul <= 0:
                self.timer_invul = 0
                self.is_invul = False
                self.color_outline = list(PLAYER_COLOR_OUTLINE)
                self.color_fill = list(PLAYER_COLOR_FILL)

    def take_damage_and_check_if_alive(self, gsm):
        if PLAYER_GOD_MODE:
            return self.is_alive
        elif self.lives > 1:
            self.lives -= 1
            self.timer_invul = 2
            self.is_invul = True
            return self.is_alive
        else:
            self.lives -= 1
            self.is_alive = False
            print(f"Game over! Final score: {gsm.score}")
            return self.is_alive

    def collect_ore(self, price):
        self.money += price

    ### Getters

    def get_ship(self):
        return self.ship
    
    def get_ship_name(self):
        return self.ship.type.value
    
    def get_money(self):
        return self.money
    
    ### Health
    
    def get_lives(self):
        return self.lives

    def get_price_heal(self):
        return (1+self.times_healed) * 5
    
    def can_heal(self):
        return (self.money >= self.get_price_heal() 
                and self.lives < self.lives_max)
    
    def buy_heal(self):
        self.money = self.money - self.get_price_heal()
        self.times_healed += 1
        if self.lives < self.lives_max:
            self.lives += 1
    
    ### Weapons
    
    def get_current_weapon_name(self):
        return self.weapon.get_name()
    
    def get_current_weapon_level(self):
        return self.weapon.get_level()

    def get_price_weapons(self, weapon_num):
        match self.weapons[weapon_num].get_level():
            case 1:
                return 15
            case 2:
                return 50
            case _:
                return 999999
    
    def can_upgrade_weapon(self, weapon_num):
        return (self.money >= self.get_price_weapons(weapon_num))
    
    def buy_upgrade_weapon(self, weapon_num):
        self.money = self.money - self.get_price_weapons(weapon_num)
        self.weapons[weapon_num].upgrade()
