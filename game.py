# pyright: reportAttributeAccessIssue=false

import pygame, time

from constants import *
from game_state_manager import GameStateManager, Menu
from round_state_manager import RoundStateManager

from player.player import Player
from player.player_stats import PlayerStats
from player.weapons.projectiles.projectileplasma import ProjectilePlasma
from player.weapons.projectiles.bomb import Bomb
from player.weapons.projectiles.bombexplosion import BombExplosion
from vfx.explosions import ExplosionBase, ExplosionSpiky, ExplosionRound

from world.starfield import StarField
from world.asteroidfield import AsteroidField
from asteroids.asteroid import Asteroid
from asteroids.ores import Ore


class Game():
    def __init__(self):
        pygame.init()
        self.screen_resolution_windowed = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen_resolution_fullscreen = pygame.display.get_desktop_sizes()[0]
        self.screen_resolution = self.screen_resolution_windowed
        self.is_fullscreen = False
        self.is_window_resized = False
        self.screen = pygame.display.set_mode(self.screen_resolution, pygame.RESIZABLE, display=0)
        pygame.display.set_caption("Asteroids from Outer Space")

        self.max_fps = MAX_FPS
        self.is_slow = False
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.is_running : bool = True
        self.is_paused : bool = False
        self.getting_player_name : bool = False
        self.is_round_end : bool = False

        self.updatable = pygame.sprite.Group()   # Must have method .update(delta)
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()            # Used for colision detection
        self.loot = pygame.sprite.Group()                 # ^ + magnet
        self.projectiles = pygame.sprite.Group()          # ^
        self.explosion_hitboxes = pygame.sprite.Group()   # ^
        self.moving_objects = pygame.sprite.Group()       # Used to destroy objects that are off-screen
        self.cleanup = pygame.sprite.Group()   # This group is cleaned (object.kill()) after each round

        GameStateManager.containers = (self.drawable)
        RoundStateManager.containers = (self.updatable, self.cleanup)

        StarField.containers = (self.drawable)
        ExplosionBase.containers = (self.updatable, self.drawable, self.cleanup)

        Player.containers = (self.updatable, self.drawable) # Not part of self.cleanup, instead removed in .initialize_new_player (so only removed when swapping saves)
        ProjectilePlasma.containers = (self.projectiles, self.updatable, self.drawable, self.moving_objects, self.cleanup)
        Bomb.containers = (self.drawable, self.updatable, self.cleanup)
        BombExplosion.containers = (self.explosion_hitboxes, self.cleanup)

        AsteroidField.containers = (self.updatable, self.cleanup)
        Asteroid.containers = (self.asteroids, self.updatable, self.drawable, self.moving_objects, self.cleanup)
        Ore.containers = (self.loot, self.updatable, self.drawable, self.moving_objects, self.cleanup)

        # Layers for drawable
        # 0 - StarField
        # 10 - Explosion
        # 20 - Bomb
        # 30 - Asteroid(and children)
        # 40 - Loot
        # 50 - Player
        # 60 - ProjectilePlasma
        # 90 - ExplosionRound (overwritten, used as player's death animation)
        # 100 - UserInterface

        self.star_field = StarField(self.screen_resolution_fullscreen)
        self.gsm = GameStateManager(self)
        self.asteroid_field = None
        self.player = None

        self.initialize_new_player()
        self.gsm.initialize_current_menu()

    def initialize_new_player(self):
        if self.player != None:
            self.player.kill()
        self.player_stats : PlayerStats = PlayerStats()
        self.player : Player = Player(self, self.player_stats)
        self.player_stats.set_player(self.player)
        self.gsm.player = self.player
        self.gsm.player_stats = self.player_stats

    def run(self):
        while self.is_running:
            self.process_and_refresh()
        
        self.gsm.save_profile() # Save on exit

    def game_loop(self):
        self.rsm = RoundStateManager(self.player)
        self.asteroid_field = AsteroidField(self, self.player, self.screen_resolution)
        self.gsm.rsm = self.rsm
        self.is_paused = False
        
        self.player.teleport_and_prepare_for_round((int(self.screen_resolution[0] / 2), int(self.screen_resolution[1] / 2)))
        self.gsm.start_round(self.rsm)

        while self.player.is_alive:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                    return
                elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        if not self.is_paused:
                            self.is_paused = True
                            self.gsm.switch_menu(Menu.PAUSE_MENU)
                        else:
                            self.is_paused = False
                            self.gsm.switch_menu(Menu.HUD)
                    else:
                        self.handle_keyboard_event_for_ship_controls(event)
                else:
                    self.handle_event(event)

            # Screen update - Game Loop
            if not self.is_paused:
                for object in self.updatable:
                    object.update(self.dt)

                for object in self.moving_objects:
                    if self.check_if_object_is_off_screen(object):
                        if isinstance(object, Asteroid):
                            self.asteroid_field.kill_asteroid(object) # The field kills/splits asteroids to keep count of certain types
                        else:
                            object.kill()

                # Colision checks
                # Player hit
                for asteroid in self.asteroids:
                    if asteroid.check_colision(self.player) and not self.player.is_invul: # No check for dead asteroids because first loop, only off-screen ones are dead
                        self.player.take_damage_and_check_if_alive()
                        self.asteroid_field.kill_asteroid(asteroid)
                        ExplosionSpiky(asteroid.position, asteroid.radius)
                    
                    # Asteroid shot
                    for projectile in self.projectiles:
                        if projectile.check_colision(asteroid) and not asteroid.is_dead:
                            projectile.kill()
                            self.asteroid_field.split_asteroid(asteroid)
                            ExplosionSpiky(asteroid.position, asteroid.radius)
                            self.rsm.score += asteroid.reward
                            if not self.player.is_sus:
                                self.rsm.increase_count_stat(type(asteroid))
                    
                # Asteroid exploded
                for hitbox in self.explosion_hitboxes:
                    for asteroid in self.asteroids:
                        if hitbox.check_colision(asteroid) and not asteroid.is_dead:
                            self.asteroid_field.split_asteroid(asteroid)
                            self.rsm.score += asteroid.reward
                            if not self.player.is_sus:
                                self.rsm.increase_count_stat(type(asteroid))
                    hitbox.kill()

                # Loot collected
                for loot in self.loot:
                    if loot.check_colision(self.player):
                        self.player.collect_loot(loot.price)
                        if not self.player.is_sus:
                            self.rsm.increase_count_stat(type(loot))
                        loot.kill()
                    elif loot.check_colision(self.player.magnet):
                        loot.home_towards(self.dt, self.player.position, self.player.magnet.get_strength())

                self.dt = self.redraw_objects_and_ui()

            # Screen update - Pause Menu
            else:
                self.redraw_objects_and_ui()

        # Death enimation
        self.player.end_round()
        ExplosionRound(self.player.position)
        death_timer = 0.0
        is_player_teleported = False
        while self.is_running and death_timer < 6:
            if not is_player_teleported and death_timer > 3:
                self.player.is_hidden = True
                is_player_teleported = True
            dt = self.process_and_refresh()
            death_timer += dt
            for object in self.updatable:
                object.update(self.dt)

        # Saving score and going back to Main Menu
        if not self.player.is_sus and self.rsm.score > 0:
            self.rsm.is_new_record, self.rsm.record_place = self.gsm.check_score(self.rsm.score)
            self.player_stats.process_round_stats(self.rsm)
            self.gsm.save_profile()
            if self.rsm.is_new_record:
                self.is_round_end = True
                self.gsm.switch_menu(Menu.NAME_CHECK)
                while self.is_round_end:
                    self.process_and_refresh()
        self.gsm.switch_menu(Menu.MAIN_MENU)

        self.player.reset()
        self.rsm = None
        self.asteroid_field = None
        self.gsm.rsm = None

        for object in self.cleanup:
            object.kill()

    def finish_round(self):
        self.is_round_end = False

    ### Helpers

    def handle_keyboard_event_for_ship_controls(self, event : pygame.event.Event):
        """Used for handling inputs for controlling the ship during gameplay and pause."""

        if self.rsm == None:
            return

        match event.scancode:
            # Movement
            case 26: # W
                if event.type == pygame.KEYDOWN:
                    self.player.state_movement += 1
                if event.type == pygame.KEYUP:
                    self.player.state_movement -= 1
                    if self.player.state_movement > 0: # Checks in case WASD where pressed while starting the round
                        self.player.state_movement = 0
            case 22: # S
                if event.type == pygame.KEYDOWN:
                    self.player.state_movement -= 1
                if event.type == pygame.KEYUP:
                    self.player.state_movement += 1
                    if self.player.state_movement < 0:
                        self.player.state_movement = 0
            # Rotation
            case 4: # A
                if event.type == pygame.KEYDOWN:
                    self.player.state_rotation -= 1
                if event.type == pygame.KEYUP:
                    self.player.state_rotation += 1
                    if self.player.state_rotation < 0:
                        self.player.state_rotation = 0
            case 7: # D
                if event.type == pygame.KEYDOWN:
                    self.player.state_rotation += 1
                if event.type == pygame.KEYUP:
                    self.player.state_rotation -= 1
                    if self.player.state_rotation > 0:
                        self.player.state_rotation = 0
            # Shooting
            case 44: # Space
                if event.type == pygame.KEYDOWN:
                    self.player.is_shooting = True
                if event.type == pygame.KEYUP:
                    self.player.is_shooting = False
            # Weapon switching
            case 30 | 89: # 1 | Keypad1
                if event.type == pygame.KEYDOWN and not self.is_paused:
                    self.player.weapon_current = self.player.weapon_plasmagun
            case 31 | 90: # 2 | Keypad2
                if event.type == pygame.KEYDOWN and not self.is_paused:
                    self.player.weapon_current = self.player.weapon_bomblauncher

    def handle_event(self, event : pygame.event.Event):
        """Used for handling events in all menus."""

        # Returns to fullscreen after Alt-tabing/loosing focus
        if event.type == pygame.WINDOWFOCUSGAINED and self.is_fullscreen:
            self.__switch_to_fullscreen()
        # Try button press
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                self.gsm.try_button_press()
        # Window resizing
        elif event.type == pygame.WINDOWRESIZED and self.is_fullscreen == False:
            self.is_window_resized = True
            self.screen_resolution_windowed = (event.dict["x"], event.dict["y"])
        elif event.type == pygame.WINDOWENTER and self.is_window_resized:
            self.is_window_resized = False
            self.__switch_to_windowed()
            if self.asteroid_field != None:
                self.asteroid_field.update_spawns(self.screen_resolution)
        #elif event.type != pygame.MOUSEMOTION:
            #print(event)
        else:
            self.gsm.handle_event_for_secrets(event)

    def process_and_refresh(self) -> float:
        """
        Checks events and redraws the screen. Returns delta.

        Don't use during gameplay! Or things go kaput.
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                self.is_round_end = False
                break
            else:
                self.handle_event(event)
        
        return self.redraw_objects_and_ui()
    
    def redraw_objects_and_ui(self) -> float:
        """
        Updates and redraws the screen, returns delta time.
        
        Also used for updating UI.
        """

        self.gsm.check_hovered_button()
        for object in sorted(list(self.drawable), key = lambda object: object.layer):
            object.draw(self.screen)

        pygame.display.flip()
        return self.clock.tick(self.max_fps) / 1000
    
    def check_if_object_is_off_screen(self, object) -> bool:
        offset = 100
        return (
            object.position.x < -offset or
            object.position.x > self.screen_resolution[0]+offset or
            object.position.y < -offset or
            object.position.y > self.screen_resolution[1]+offset
        )
    
    def get_player_name(self) -> bool: # Used in profile creation in game_state_manager
        self.getting_player_name = True
        while self.getting_player_name:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                    return False
                elif event.type == pygame.KEYDOWN:
                    #print(event)
                    if event.key == pygame.K_BACKSPACE:
                        self.player_stats.name = self.player_stats.name[:-1]
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        if len(self.player_stats.name.strip()) > 0:
                            self.getting_player_name = False
                    elif event.key == pygame.K_TAB or event.key == pygame.K_ESCAPE:
                        continue
                    else:
                        k = event.dict["unicode"]
                        if k != "" and len(self.player_stats.name) < PLAYER_MAX_NAME_LENGTH:
                            self.player_stats.name = self.player_stats.name + k
                else:
                    self.handle_event(event)
            
            self.redraw_objects_and_ui()

        self.player_stats.name = self.player_stats.name.strip()
        return True

    def finish_getting_player_name(self):
        if len(self.player_stats.name.strip()) > 0:
            self.getting_player_name = False

    ### Handlers
    
    def handler_turn_off(self):
        self.is_running = False

    def handler_finish_round(self):
        self.player.is_alive = False
        self.gsm.switch_menu(Menu.HUD)

    def handler_regenerate_background(self):
        self.star_field.regenerate()

    def switch_fullscreen(self):
        if not self.is_fullscreen:
            self.is_fullscreen = True
            self.__switch_to_fullscreen()
        else:
            self.is_fullscreen = False
            self.__switch_to_windowed()

    def switch_low_fps(self):
        self.max_fps = 75 if self.max_fps == 10 else 10
        self.is_slow = False if self.is_slow else True
    
    def __switch_to_fullscreen(self):
            self.screen_resolution = self.screen_resolution_fullscreen
            flags = pygame.FULLSCREEN
            self.screen = pygame.display.set_mode(self.screen_resolution, flags)
            self.gsm.initialize_current_menu()

    def __switch_to_windowed(self):
            self.screen_resolution = self.screen_resolution_windowed
            # Changes mode twice because first change disables fullcreen,
            # second change changes window size
            self.screen = pygame.display.set_mode(self.screen_resolution)
            self.screen = pygame.display.set_mode(self.screen_resolution, pygame.RESIZABLE)
            self.gsm.initialize_current_menu()
