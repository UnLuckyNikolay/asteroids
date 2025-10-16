import pygame
from enum import Enum

from constants import *
from shapes.circleshape import CircleShape
from player.weapons.plasmagun import PlasmaGun
from player.weapons.bomblauncher import BombLauncher
from player.ship_parts.magnet import Magnet
from player.ship import Ship, ShipType


# New upgrades should be added to methods get_upgrade_level and buy_upgrade
class ShipPart(Enum):
    """List of player upgrades"""

    WEAPON1 = "Weapon 1"
    WEAPON2 = "Weapon 2"
    MAGNETRADIUS = "Magnet Radius"
    MAGNETSTRENGTH = "Magnet Strength"

class Player(CircleShape):
    layer = 50 # pyright: ignore
    def __init__(self, game, position : pygame.Vector2, cheat_godmode : bool, cheat_stonks : bool, cheat_hitbox : bool):
        super().__init__(position, (0,0), PLAYER_RADIUS)
        self.rotation = 180
        self.rotation_inertia = self.rotation
        self.inertia = pygame.Vector2(0, 0)
        self.__speed = 0
        self.__turning_speed = 0
        self.last_dt = 0

        self.game = game
        self.cheat_godmode = cheat_godmode

        self.timer_invul = 0
        self.is_invul = False
        self.is_alive = True
        self.is_accelerating = False

        self.unlocked_ships = [
            ShipType.POLY,
            ShipType.POLY2BP,
            ShipType.POLY2,
            ShipType.POLY3,
            ShipType.UFO,
        ]
        self.ship_model = 3
        self.ship = Ship(self.unlocked_ships[self.ship_model], self.radius, cheat_hitbox)
        self.magnet = Magnet(self.position, 100)

        self.money = 0 if not cheat_stonks else 9999
        self.lives = 3
        self.lives_max = 3
        self.times_healed = 0

        self.time_since_last_shot = 0
        self.weapons = []
        self.weapons.append(PlasmaGun())
        self.weapons.append(BombLauncher())
        self.weapon = self.weapons[0]

        self.is_sus = False
        """True if cheats are enabled"""
        if cheat_godmode or cheat_hitbox or cheat_stonks:
            self.is_sus = True
    

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
            self.position,
            self.rotation+180,
            self.magnet.radius,
            self.is_accelerating,
            self.timer_invul
        )

    def rotate(self, dt):
        self.rotation += self.turning_speed * dt

    def move(self, dt):
        self.inertia = self.inertia * ((100 - PLAYER_ACCELERATION) / 100) + pygame.Vector2(0, 1).rotate(self.rotation_inertia) * (PLAYER_ACCELERATION / 100)
        self.position += self.inertia * self.speed * dt

        screen_resolution = self.game.screen_resolution
        # Teleports player if off-screen
        if self.position.x < -ASTEROID_MAX_RADIUS:
            self.position.x = screen_resolution[0] + ASTEROID_MAX_RADIUS
        elif self.position.x > screen_resolution[0] + ASTEROID_MAX_RADIUS:
            self.position.x = -ASTEROID_MAX_RADIUS
        if self.position.y < -ASTEROID_MAX_RADIUS:
            self.position.y = screen_resolution[1] + ASTEROID_MAX_RADIUS
        elif self.position.y > screen_resolution[1] + ASTEROID_MAX_RADIUS:
            self.position.y = -ASTEROID_MAX_RADIUS

    def attempt_shot(self, time_since_last_shot) -> bool:
        return self.weapon.attempt_shot(self.position, self.rotation, time_since_last_shot)

    def update(self, dt):
        self.ship.update(dt) # For animations
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
            self.is_accelerating = True
            self.rotation_inertia = self.rotation
            self.speed += PLAYER_ACCELERATION
        elif keys[pygame.K_s] and not keys[pygame.K_w]:
            self.is_accelerating = False
            self.rotation_inertia = self.rotation
            self.speed -= PLAYER_ACCELERATION
        else:   # Deceleration
            self.is_accelerating = False
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

    def take_damage_and_check_if_alive(self, gsm) -> bool:
        if self.cheat_godmode:
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

    def collect_loot(self, price):
        self.money += price

    ### Getters
    
    def get_money(self) -> int:
        return self.money

    def get_current_weapon_name(self) -> str:
        return self.weapon.get_name()
    
    def get_current_weapon_level(self) -> int:
        return self.weapon.get_level()
    
    ### Ship

    def get_ship(self) -> Ship:
        return self.ship
    
    def get_ship_name(self) -> str:
        return self.ship.type.value
    
    def switch_ship_model_to_next(self):
        self.ship_model = (self.ship_model+1) % len(self.unlocked_ships)
        self.ship.switch_model(self.unlocked_ships[self.ship_model])
    
    def switch_ship_model_to_previous(self):
        self.ship_model = (self.ship_model-1) % len(self.unlocked_ships)
        self.ship.switch_model(self.unlocked_ships[self.ship_model])
    
    ### Health
    
    def get_lives(self) -> int:
        return self.lives

    def get_price_heal(self) -> int:
        return (1+self.times_healed) * 5
    
    def can_heal(self) -> bool:
        return (self.money >= self.get_price_heal() 
                and self.lives < self.lives_max)
    
    def buy_heal(self):
        self.money = self.money - self.get_price_heal()
        self.times_healed += 1
        if self.lives < self.lives_max:
            self.lives += 1
    
    ### Upgrades

    def get_upgrade_level(self, ship_part : ShipPart) -> int:
        match ship_part:
            case ShipPart.WEAPON1:
                return self.weapons[0].get_level()
            case ShipPart.WEAPON2:
                return self.weapons[1].get_level()
            case ShipPart.MAGNETRADIUS:
                return self.magnet.radius_level
            case ShipPart.MAGNETSTRENGTH:
                return self.magnet.strength_level
            
    def get_upgrade_price(self, ship_part : ShipPart) -> int:
        level = self.get_upgrade_level(ship_part)
        match level:
            case 1:
                return 15
            case 2:
                return 50
            case _:
                return 999999
            
    def can_buy_upgrade(self, ship_part : ShipPart) -> bool:
        return (self.money >= self.get_upgrade_price(ship_part))
    
    def buy_upgrade(self, ship_part : ShipPart):
        self.money -= self.get_upgrade_price(ship_part)
        match ship_part:
            case ShipPart.WEAPON1:
                self.weapons[0].upgrade()
            case ShipPart.WEAPON2:
                self.weapons[1].upgrade()
            case ShipPart.MAGNETRADIUS:
                self.magnet.upgrade_radius()
            case ShipPart.MAGNETSTRENGTH:
                self.magnet.upgrade_strength()
