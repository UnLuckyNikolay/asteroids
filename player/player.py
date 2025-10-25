import pygame
from enum import Enum

from constants import *
from shapes.circleshape import CircleShape
from player.weapons.plasmagun import PlasmaGun
from player.weapons.bomblauncher import BombLauncher
from player.ship_parts.magnet import Magnet
from player.ship import Ship, ShipType
from player.player_stats import PlayerStats


# New upgrades should be added to:
# - .get_upgrade_level 
# - .buy_upgrade
class ShipUpgrade(Enum):
    """List of player upgrades"""

    PLASMAGUN_PROJECTILES = "Plasma Gun: Projectiles"
    PLASMAGUN_COOLDOWN = "Plasma Gun: Cooldown"
    BOMBLAUNCHER_RADIUS = "Bomb Launcher: Radius"
    BOMBLAUNCHER_FUSE = "Bomb Launcher: Fuse"
    MAGNET_RADIUS = "Magnet: Radius"
    MAGNET_STRENGTH = "Magnet: Strength"

# New parts should be added to 
# - .get_part_level
class ShipPart(Enum):
    """List of player parts"""

    PLASMAGUN = "Plasma Gun"
    BOMBLAUNCHER = "Bomb Launcher"
    MAGNET = "Magnet"

class Player(CircleShape):
    layer = 50 # pyright: ignore
    def __init__(self, game, stats):
        super().__init__(pygame.Vector2(-100, -100), (0,0), PLAYER_RADIUS)
        self.rotation = 180
        self.rotation_inertia = self.rotation
        self.inertia = pygame.Vector2(0, 0)
        self.__speed = 0
        self.__turning_speed = 0
        self.last_dt = 0

        # For controls in game.handle_event_for_ship_controls()
        self.state_movement : int = 0 # -1 - going backwards, 0 - nothing, 1 - going forward
        self.state_rotation : int = 0 # -1 - rotating left, 0 - nothing, 1 - rotating right
        self.is_shooting : bool = False

        self.game = game
        self.stats : PlayerStats = stats

        self.timer_invul = 0
        self.is_invul : bool = False
        self.is_alive : bool = True
        self.is_accelerating : bool = False
        self.is_auto_shooting : bool = False

        self.money = 0
        self.lives = 3
        self.lives_max = 3
        self.times_healed = 0

        self.ship = Ship(self.stats.unlocked_ships[self.stats.ship_model], self.radius)
        self.magnet = Magnet(self.position)
        self.weapon_plasmagun = PlasmaGun()
        self.weapon_bomblauncher = BombLauncher()
        self.time_since_last_shot = 0
        self.weapon_current = self.weapon_plasmagun

        self.is_sus : bool = False
        """True if cheats are enabled"""

    @property
    def turning_speed(self):
        return self.__turning_speed
    
    @turning_speed.setter
    def turning_speed(self, value):
        if value < -PLAYER_TURNING_MAX:
            self.__turning_speed = -PLAYER_TURNING_MAX
        elif value > PLAYER_TURNING_MAX:
            self.__turning_speed = PLAYER_TURNING_MAX
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
        else:
            self.__speed = value


    def reset(self):
        self.position = pygame.Vector2(-100, -100)
        self.rotation = 180
        self.rotation_inertia = self.rotation
        self.inertia = pygame.Vector2(0, 0)
        self.__speed = 0
        self.__turning_speed = 0
        self.last_dt = 0

        # For controls in game.handle_event_for_ship_controls()
        self.state_movement : int = 0 # -1 - going backwards, 0 - nothing, 1 - going forward
        self.state_rotation : int = 0 # -1 - rotating left, 0 - nothing, 1 - rotating right
        self.is_shooting : bool = False

        self.timer_invul = 0
        self.is_invul : bool = False
        self.is_alive : bool = True
        self.is_accelerating : bool = False
        self.is_auto_shooting : bool = False

        self.magnet = Magnet(self.position)
        
        self.money = 0
        self.lives = 3
        self.lives_max = 3
        self.times_healed = 0

        self.time_since_last_shot = 0
        self.weapon_plasmagun = PlasmaGun()
        self.weapon_bomblauncher = BombLauncher()
        self.weapon_current = self.weapon_plasmagun

    def teleport_and_prepare_for_round(self, position : tuple[int, int]):
        self.position = pygame.Vector2(position)
        self.magnet = Magnet(self.position)

        if self.stats.cheat_godmode or self.stats.cheat_hitbox or self.stats.cheat_stonks:
            self.is_sus = True
        else:
            self.is_sus = False
        if self.stats.cheat_stonks:
            self.money = 9999
        self.ship.switch_hitbox_to(self.stats.cheat_hitbox)

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
        self.inertia = self.inertia * ((100 - PLAYER_ACCELERATION * dt) / 100) + pygame.Vector2(0, 1).rotate(self.rotation_inertia) * (PLAYER_ACCELERATION * dt / 100)
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
        return self.weapon_current.attempt_shot(self.position, self.rotation, time_since_last_shot)

    def update(self, dt):
        self.ship.update(dt) # For animations
        self.last_dt = dt
        self.time_since_last_shot += dt

        # Turning
        if self.turning_speed != 0:
            self.rotate(dt)
        match self.state_rotation:
            case 1:
                self.turning_speed += PLAYER_TURNING_ACCELERATION * dt
            case -1:
                self.turning_speed -= PLAYER_TURNING_ACCELERATION * dt
            case 0: # Deceleration
                amount = PLAYER_TURNING_ACCELERATION * dt / 2
                if self.turning_speed > 0:
                    if self.turning_speed < amount:
                        self.__turning_speed = 0
                    else:
                        self.turning_speed -= amount
                elif self.turning_speed < 0:
                    if self.turning_speed > -amount:
                        self.__turning_speed = 0
                    else:
                        self.turning_speed += amount

        # Movement
        if self.speed != 0:
            self.move(dt)
        match self.state_movement:
            case 1:
                self.is_accelerating = True # For drawing engine animation
                self.rotation_inertia = self.rotation
                self.speed += PLAYER_ACCELERATION * dt
            case -1:
                self.is_accelerating = False
                self.rotation_inertia = self.rotation
                self.speed -= PLAYER_ACCELERATION * dt
            case 0: # Deceleration
                amount = PLAYER_ACCELERATION * dt / 2
                self.is_accelerating = False
                if self.speed > 0:
                    if self.speed < amount:
                        self.speed = 0
                        self.inertia = pygame.Vector2(0, 0)
                    else:
                        self.speed -= amount
                elif self.speed < 0:
                    if self.speed > -amount:
                        self.speed = 0
                        self.inertia = pygame.Vector2(0, 0)
                    else:
                        self.speed += amount

        # Shooting
        if (
            (self.is_shooting or self.is_auto_shooting) and 
            self.attempt_shot(self.time_since_last_shot)
        ):
            self.time_since_last_shot = 0

        # Invulnerability timer
        if self.is_invul:
            if self.timer_invul > 0:
                self.timer_invul -= dt

            if self.timer_invul <= 0:
                self.timer_invul = 0
                self.is_invul = False

    def take_damage_and_check_if_alive(self, gsm) -> bool:
        if self.stats.cheat_godmode:
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
        return self.weapon_current.get_name()
    
    def get_current_weapon_level(self) -> int:
        return self.weapon_current.get_level()
    
    # Helpers

    def switch_auto_shoot(self):
        self.is_auto_shooting = False if self.is_auto_shooting else True
    
    ### Ship

    def get_ship(self) -> Ship:
        return self.ship

    def get_part_level(self, part : ShipPart) -> int:
        match part:
            case ShipPart.PLASMAGUN:
                return self.weapon_plasmagun._level
            case ShipPart.BOMBLAUNCHER:
                return self.weapon_bomblauncher._level
            case ShipPart.MAGNET:
                return self.magnet._level
    
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

    def get_upgrade_level(self, ship_part : ShipUpgrade) -> int:
        match ship_part:
            case ShipUpgrade.PLASMAGUN_PROJECTILES:
                return self.weapon_plasmagun._level_projectiles
            case ShipUpgrade.PLASMAGUN_COOLDOWN:
                return self.weapon_plasmagun._level_cooldown
            case ShipUpgrade.BOMBLAUNCHER_RADIUS:
                return self.weapon_bomblauncher._level_radius
            case ShipUpgrade.BOMBLAUNCHER_FUSE:
                return self.weapon_bomblauncher._level_fuse
            case ShipUpgrade.MAGNET_RADIUS:
                return self.magnet._level_radius
            case ShipUpgrade.MAGNET_STRENGTH:
                return self.magnet._level_strength
            
    def get_upgrade_price(self, ship_part : ShipUpgrade) -> int | None:
        level = self.get_upgrade_level(ship_part)
        match level:
            case 1:
                return 15
            case 2:
                return 50
            case _:
                return None
            
    def get_upgrade_price_as_text(self, ship_part : ShipUpgrade) -> str:
        level = self.get_upgrade_level(ship_part)
        match level:
            case 1:
                return "15g"
            case 2:
                return "50g"
            case _:
                return "MAX"
            
    def can_buy_upgrade(self, ship_part : ShipUpgrade) -> bool:
        price = self.get_upgrade_price(ship_part)
        return (
            price is not None and
            self.money >= price
        )
    
    def buy_upgrade(self, ship_part : ShipUpgrade):
        price = self.get_upgrade_price(ship_part)
        if price == None:
            return

        self.money -= price
        match ship_part:
            case ShipUpgrade.PLASMAGUN_PROJECTILES:
                self.weapon_plasmagun.upgrade_projectiles()
            case ShipUpgrade.PLASMAGUN_COOLDOWN:
                self.weapon_plasmagun.upgrade_cooldown()
            case ShipUpgrade.BOMBLAUNCHER_RADIUS:
                self.weapon_bomblauncher.upgrade_radius()
            case ShipUpgrade.BOMBLAUNCHER_FUSE:
                self.weapon_bomblauncher.upgrade_fuse()
            case ShipUpgrade.MAGNET_RADIUS:
                self.magnet.upgrade_radius()
            case ShipUpgrade.MAGNET_STRENGTH:
                self.magnet.upgrade_strength()
