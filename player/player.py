import pygame
from typing import Callable

from constants import *
from ui.menus.enum_action import Action
from sfx_manager import SFXManager
from shapes.circleshape import CircleShape
from player.weapons.plasmagun import PlasmaGun
from player.weapons.bomblauncher import BombLauncher
from player.weapons.literally_a_fucking_meat_cleaver_launcher import LiterallyAFuckingMeatCleaverLauncher
from player.ship_parts.magnet import Magnet
from player.ship import Ship
from player.ship_enums import ShipModel, ShipPart, ShipUpgrade
from player.player_stats import PlayerStats


class Player(CircleShape):
    layer = 50 # pyright: ignore
    def __init__(self, getter_screen_res : Callable[[], tuple[int, int]], sfxm : SFXManager, held_actions : dict[Action, bool]):
        super().__init__(pygame.Vector2(-100, -100), pygame.Vector2(0,0), PLAYER_RADIUS)
        self.velocity_target = pygame.Vector2(0, 0)
        self.rotation : float = 180
        self.__turning_speed : float = 0

        # For controls in game.handle_event_for_ship_controls()
        self.state_movement : int = 0 # -1 - going backwards, 0 - nothing, 1 - going forward
        self.state_rotation : int = 0 # -1 - rotating left, 0 - nothing, 1 - rotating right
        self.is_shooting : bool = False

        self.getter_screen_res = getter_screen_res
        self.is_hidden : bool = True
        """Used as a check when teleporting the player if off-screen."""
        self.stats : PlayerStats = PlayerStats()
        self.sfxm = sfxm
        self.held_actions = held_actions

        self.timer_invul : float = 0
        self.is_invul : bool = False
        self.is_alive : bool = True
        self.is_accelerating : bool = False
        self.is_auto_shooting : bool = False # not reset between rounds
        self.is_auto_healing : bool = False

        self.money : int = 0
        self.lives : int = 3
        self.lives_max : int = 3
        self.times_healed : int = 0

        self.ship : Ship = Ship(self.stats.get_current_ship_model(), self.radius)
        self.is_hitbox_shown : bool = False
        self.__level_engine : int = 1
        self.__level_max_engine : int = 5
        self.__level_engine_speed : int = 1
        self.__level_max_engine_speed : int = 3
        self.__engine_speed : int = 200
        self.__level_engine_acceleration : int = 1
        self.__level_max_engine_acceleration : int = 3
        self.__engine_acceleration_mp : float = 0.8
        self.magnet : Magnet = Magnet(self.position)
        self.weapon_plasmagun : PlasmaGun = PlasmaGun(self.sfxm)
        self.weapon_bomblauncher : BombLauncher = BombLauncher(self.sfxm)
        self.weapon_meat : LiterallyAFuckingMeatCleaverLauncher = LiterallyAFuckingMeatCleaverLauncher(self.sfxm)
        self.time_since_last_shot : float = 0
        self.weapons = [self.weapon_plasmagun, self.weapon_bomblauncher, self.weapon_meat]
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


    def load_save(self, player_stats):
        self.stats.load_save(player_stats)
        self.apply_saved_skin()

    def apply_saved_skin(self):
        self.ship.switch_model(self.stats.get_current_ship_model(), self.stats.ship_color_profile)
        
    def switch_ship_model_to_next(self):
        self.stats.switch_ship_model_to_next()
        self.apply_saved_skin()
    
    def switch_ship_model_to_previous(self):
        self.stats.switch_ship_model_to_previous()
        self.apply_saved_skin()

    def teleport_away(self):
        self.velocity_target.update(0, 0)
        self.velocity.update(0, 0)
        self.position.update(-100, -100)
        self.rotation = 180
        self.__turning_speed = 0

    def reset(self):
        # For controls in game.handle_event_for_ship_controls()
        self.state_movement = 0 # -1 - going backwards, 0 - nothing, 1 - going forward
        self.state_rotation = 0 # -1 - rotating left, 0 - nothing, 1 - rotating right
        self.is_shooting = False

        self.timer_invul = 0
        self.is_invul = False
        self.is_alive = True
        self.is_accelerating = False
        self.is_auto_healing = False

        self.magnet = Magnet(self.position)
        self.__level_engine = 1
        self.__level_engine_speed = 1
        self.__engine_speed = 250
        self.__level_engine_acceleration = 1
        self.__engine_acceleration_mp = 1.0
        
        self.money = 0
        self.lives = 3
        self.lives_max = 3
        self.times_healed = 0

        self.time_since_last_shot = 0
        self.weapon_plasmagun = PlasmaGun(self.sfxm)
        self.weapon_bomblauncher = BombLauncher(self.sfxm)
        self.weapon_meat = LiterallyAFuckingMeatCleaverLauncher(self.sfxm)
        self.weapons = [self.weapon_plasmagun, self.weapon_bomblauncher, self.weapon_meat]
        self.weapon_current = self.weapon_plasmagun

    def teleport_and_prepare_for_round(self, position : tuple[int, int]):
        self.apply_saved_skin()
        self.position.update(position)
        self.magnet = Magnet(self.position)
        self.is_hidden = False

        if (
            self.stats.cheat_godmode 
            or self.stats.cheat_stonks 
            or self.stats.cheat_cleavers
        ):
            self.is_sus = True
        else:
            self.is_sus = False
        if self.stats.cheat_stonks:
            self.money = 9999
        self.ship.switch_hitbox_to(self.is_hitbox_shown)

    def draw(self, screen : pygame.Surface):
        if self.is_hidden:
            return
        self.ship.draw_rotated(
            screen, 
            self.position,
            self.rotation+180,
            self.magnet.radius,
            self.is_accelerating,
            self.timer_invul
        )

    def rotate(self, dt : float):
        self.rotation += self.turning_speed * dt

    def move(self, dt : float):
        if (
            (self.held_actions[Action.PLAYER_MOVEMENT_FORWARD] or self.held_actions[Action.PLAYER_MOVEMENT_FORWARD_ALT]) 
            and not (self.held_actions[Action.PLAYER_MOVEMENT_BACKWARD] or self.held_actions[Action.PLAYER_MOVEMENT_BACKWARD_ALT])
        ):
            self.velocity_target.update(0, 1)
            self.velocity_target.rotate_ip(self.rotation)
            self.velocity.move_towards_ip(self.velocity_target, self.__engine_acceleration_mp * 1.5 * dt)
            self.is_accelerating = True # For drawing engine animation
        elif (
            (self.held_actions[Action.PLAYER_MOVEMENT_BACKWARD] or self.held_actions[Action.PLAYER_MOVEMENT_BACKWARD_ALT]) 
            and not (self.held_actions[Action.PLAYER_MOVEMENT_FORWARD] or self.held_actions[Action.PLAYER_MOVEMENT_FORWARD_ALT])
        ):
            self.velocity_target.update(0, -0.5)
            self.velocity_target.rotate_ip(self.rotation)
            self.velocity.move_towards_ip(self.velocity_target, self.__engine_acceleration_mp * 0.8 * dt)
            self.is_accelerating = False # For drawing engine animation
        else:
            self.velocity_target.update(0, 0)
            self.velocity.move_towards_ip(self.velocity_target, 0.65 * dt)
            self.is_accelerating = False # For drawing engine animation
        self.position += self.velocity * self.__engine_speed * dt

        # Teleports player if off-screen
        if not self.is_hidden:
            res = self.getter_screen_res()
            if self.position.x < -ASTEROID_MAX_RADIUS:
                self.position.x = res[0] + ASTEROID_MAX_RADIUS
            elif self.position.x > res[0] + ASTEROID_MAX_RADIUS:
                self.position.x = -ASTEROID_MAX_RADIUS
            if self.position.y < -ASTEROID_MAX_RADIUS:
                self.position.y = res[1] + ASTEROID_MAX_RADIUS
            elif self.position.y > res[1] + ASTEROID_MAX_RADIUS:
                self.position.y = -ASTEROID_MAX_RADIUS

    def attempt_shot(self, time_since_last_shot : float) -> bool:
        return self.weapon_current.attempt_shot(self.position, self.rotation, time_since_last_shot)

    def update(self, dt : float):
        self.ship.update(dt) # For animations
        self.time_since_last_shot += dt

        # Turning
        if self.turning_speed != 0:
            self.rotate(dt)
        if (
            (self.held_actions[Action.PLAYER_MOVEMENT_RIGHT] or self.held_actions[Action.PLAYER_MOVEMENT_RIGHT_ALT]) 
            and not (self.held_actions[Action.PLAYER_MOVEMENT_LEFT] or self.held_actions[Action.PLAYER_MOVEMENT_LEFT_ALT])
        ):
            self.turning_speed += PLAYER_TURNING_ACCELERATION * dt
        elif (
            (self.held_actions[Action.PLAYER_MOVEMENT_LEFT] or self.held_actions[Action.PLAYER_MOVEMENT_LEFT_ALT]) 
            and not (self.held_actions[Action.PLAYER_MOVEMENT_RIGHT] or self.held_actions[Action.PLAYER_MOVEMENT_RIGHT_ALT])
        ):
            self.turning_speed -= PLAYER_TURNING_ACCELERATION * dt
        else: # Deceleration
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
        self.move(dt)

        # Shooting
        if (
            self.is_alive and
            (self.held_actions[Action.PLAYER_SHOOT] or self.is_auto_shooting) and 
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

    def take_damage_and_check_if_alive(self) -> bool:
        if self.stats.cheat_godmode:
            return self.is_alive
        elif self.lives > 1:
            self.lives -= 1
            self.timer_invul = 2
            self.is_invul = True
            # Auto-heal
            if self.is_auto_healing and self.can_heal():
                self.buy_heal()
            return self.is_alive
        else:
            self.lives -= 1
            self.is_alive = False
            return self.is_alive
        
    def end_round(self):
        self.state_movement = 0
        self.state_rotation = 0

    def collect_loot(self, price : int):
        self.money += price
        # Auto-heal
        if self.is_auto_healing and self.can_heal():
            self.buy_heal()

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

    def switch_auto_heal(self):
        self.is_auto_healing = False if self.is_auto_healing else True
        while self.is_auto_healing and self.can_heal():
            self.buy_heal()

    def switch_hitbox(self):
        self.is_hitbox_shown = False if self.is_hitbox_shown else True
    
    def switch_weapon(self, index : int):
        if index == 2 and not self.stats.cheat_cleavers:
            return
        self.weapon_current = self.weapons[index] # God save you if you create an IndexError 
    
    ### Ship

    def get_ship(self) -> Ship:
        return self.ship

    def get_part_level(self, part : ShipPart) -> int:
        match part:
            case ShipPart.ENGINE:
                return self.__level_engine
            case ShipPart.MAGNET:
                return self.magnet._level
            case ShipPart.PLASMAGUN:
                return self.weapon_plasmagun._level
            case ShipPart.BOMBLAUNCHER:
                return self.weapon_bomblauncher._level
            case ShipPart.LITERALLYAFUCKINGMEATCLEAVERLAUNCHER:
                return self.weapon_meat._level

    def get_part_level_max(self, part : ShipPart) -> int:
        match part:
            case ShipPart.ENGINE:
                return self.__level_max_engine
            case ShipPart.MAGNET:
                return self.magnet._level_max
            case ShipPart.PLASMAGUN:
                return self.weapon_plasmagun._level_max
            case ShipPart.BOMBLAUNCHER:
                return self.weapon_bomblauncher._level_max
            case ShipPart.LITERALLYAFUCKINGMEATCLEAVERLAUNCHER:
                return self.weapon_meat._level_max
    
    def switch_color_profile(self, number : int):
        self.ship.switch_color_profile(number)
        self.stats.ship_color_profile = number
    
    ### Health
    
    def get_lives(self) -> int:
        return self.lives

    def get_price_heal(self) -> int:
        return (1+self.times_healed) * 5
    
    def can_heal(self) -> bool:
        return (self.money >= self.get_price_heal() 
                and self.lives < self.lives_max)
    
    def buy_heal(self):
        if self.lives >= self.lives_max:
            return
        self.money = self.money - self.get_price_heal()
        self.times_healed += 1
        self.lives += 1
    
    ### Upgrades

    def get_upgrade_level(self, ship_part : ShipUpgrade) -> int:
        match ship_part:
            case ShipUpgrade.ENGINE_SPEED:
                return self.__level_engine_speed
            case ShipUpgrade.ENGINE_ACCELERATION:
                return self.__level_engine_acceleration
            case ShipUpgrade.MAGNET_RADIUS:
                return self.magnet._level_radius
            case ShipUpgrade.MAGNET_STRENGTH:
                return self.magnet._level_strength
            case ShipUpgrade.PLASMAGUN_PROJECTILES:
                return self.weapon_plasmagun._level_projectiles
            case ShipUpgrade.PLASMAGUN_COOLDOWN:
                return self.weapon_plasmagun._level_cooldown
            case ShipUpgrade.BOMBLAUNCHER_RADIUS:
                return self.weapon_bomblauncher._level_radius
            case ShipUpgrade.BOMBLAUNCHER_FUSE:
                return self.weapon_bomblauncher._level_fuse
            case ShipUpgrade.LITERALLYAFUCKINGMEATCLEAVERLAUNCHER_MEAT:
                return self.weapon_meat._level_meat

    def get_upgrade_level_max(self, ship_part : ShipUpgrade) -> int:
        match ship_part:
            case ShipUpgrade.ENGINE_SPEED:
                return self.__level_max_engine_speed
            case ShipUpgrade.ENGINE_ACCELERATION:
                return self.__level_max_engine_acceleration
            case ShipUpgrade.MAGNET_RADIUS:
                return self.magnet._level_max_radius
            case ShipUpgrade.MAGNET_STRENGTH:
                return self.magnet._level_max_strength
            case ShipUpgrade.PLASMAGUN_PROJECTILES:
                return self.weapon_plasmagun._level_max_projectiles
            case ShipUpgrade.PLASMAGUN_COOLDOWN:
                return self.weapon_plasmagun._level_max_cooldown
            case ShipUpgrade.BOMBLAUNCHER_RADIUS:
                return self.weapon_bomblauncher._level_max_radius
            case ShipUpgrade.BOMBLAUNCHER_FUSE:
                return self.weapon_bomblauncher._level_max_fuse
            case ShipUpgrade.LITERALLYAFUCKINGMEATCLEAVERLAUNCHER_MEAT:
                return self.weapon_meat._level_max_meat
            
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
            case ShipUpgrade.ENGINE_SPEED:
                self.__upgrade_engine_speed()
            case ShipUpgrade.ENGINE_ACCELERATION:
                self.__upgrade_engine_acceleration()
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
            case ShipUpgrade.LITERALLYAFUCKINGMEATCLEAVERLAUNCHER_MEAT:
                self.weapon_meat.upgrade_meat()

    def __upgrade_engine_speed(self):
        match self.__level_engine_speed:
            case 1:
                self.__level_engine += 1
                self.__level_engine_speed += 1
                self.__engine_speed = 250
            case 2:
                self.__level_engine += 1
                self.__level_engine_speed += 1
                self.__engine_speed = 300

    def __upgrade_engine_acceleration(self):
        match self.__level_engine_acceleration:
            case 1:
                self.__level_engine += 1
                self.__level_engine_acceleration += 1
                self.__engine_acceleration_mp = 1
            case 2:
                self.__level_engine += 1
                self.__level_engine_acceleration += 1
                self.__engine_acceleration_mp = 1.2
    