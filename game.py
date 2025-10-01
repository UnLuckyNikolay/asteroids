# pyright: reportAttributeAccessIssue=false

import pygame

from constants import *
from player.player import Player
from player.weapons.projectiles.projectileplasma import ProjectilePlasma
from player.weapons.projectiles.bomb import Bomb
from player.weapons.projectiles.bombexplosion import BombExplosion
from gamestatemanager import GameStateManager
from vfx.explosion import Explosion
from world.starfield import StarField
from world.asteroidfield import AsteroidField
from asteroids.asteroid import Asteroid
from asteroids.ores import Ore
from ui.userinterface import UserInterface, Menu


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

        self.clock = pygame.time.Clock()
        self.dt = 0
        self.is_running = True
        self.is_paused = False
        self.getting_player_name = False
        self.player_name = ""

        self.cheat_godmode = False
        self.cheat_hitbox = False

        self.updatable = pygame.sprite.Group()   # This group is cleaned (object.kill()) after each round
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()            # Used for colision detection
        self.ores = pygame.sprite.Group()                 # ^
        self.projectiles = pygame.sprite.Group()          # ^
        self.explosion_hitboxes = pygame.sprite.Group()   # ^
        self.moving_objects = pygame.sprite.Group()       # Used to destroy objects that are off-screen

        UserInterface.containers = (self.drawable)

        StarField.containers = (self.drawable)
        Explosion.containers = (self.updatable, self.drawable)

        Player.containers = (self.updatable, self.drawable)
        ProjectilePlasma.containers = (self.projectiles, self.updatable, self.drawable, self.moving_objects)
        Bomb.containers = (self.drawable, self.updatable)
        BombExplosion.containers = (self.explosion_hitboxes)

        AsteroidField.containers = (self.updatable)
        Asteroid.containers = (self.asteroids, self.updatable, self.drawable, self.moving_objects)
        Ore.containers = (self.ores, self.updatable, self.drawable, self.moving_objects)

        # Layers for drawable
        # 0 - StarField
        # 10 - Explosion
        # 20 - Bomb
        # 30 - Asteroid(and children)
        # 50 - Player
        # 60 - ProjectilePlasma
        # 100 - UserInterface

        self.star_field = StarField(self.screen_resolution_fullscreen)
        self.ui = UserInterface(self)
        self.asteroid_field = None
        self.player = None

    def run(self):
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                else:
                    self.handle_event(event)
            
            self.ui.switch_menu(Menu.NAME_CHECK)
            if self.ui.force_ui_reload:
                self.redraw_objects_and_ui()

            pygame.display.flip()
            self.clock.tick(60)

    def game_loop(self):
        self.player = Player(self, self.screen_resolution[0] / 2, self.screen_resolution[1] / 2,
                             self.cheat_godmode, self.cheat_hitbox)
        self.gsm = GameStateManager(self.player)
        self.asteroid_field = AsteroidField(self, self.player, self.screen_resolution)
        self.ui.gsm = self.gsm
        self.is_paused = False
        
        self.ui.start_round(self.gsm, self.player)


        while self.player.is_alive:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                    return
                elif event.type == pygame.KEYDOWN:
                    self.ui.force_ui_reload = True
                    if event.key == pygame.K_ESCAPE:
                        if not self.is_paused:
                            self.is_paused = True
                            self.ui.switch_menu(Menu.PAUSE_MENU)
                        else:
                            self.is_paused = False
                            self.ui.switch_menu(Menu.HUD)
                else:
                    self.handle_event(event)

            # Screen update - Game Loop
            if not self.is_paused:
                for object in self.updatable:
                    object.update(self.dt)

                for object in self.moving_objects:
                    if self.check_if_object_is_off_screen(object):
                        object.kill()

                self.redraw_objects_and_ui()

                # Colision checks
                for asteroid in self.asteroids:
                    if asteroid.check_colision(self.player) and not self.player.is_invul:
                        if self.player.take_damage_and_check_if_alive(self.gsm):
                            asteroid.kill()
                            explosion = Explosion(asteroid.position.x, asteroid.position.y, asteroid.radius)
                        
                    for projectile in self.projectiles:
                        if projectile.check_colision(asteroid) and not asteroid.has_been_hit:
                            projectile.kill()
                            asteroid.split()
                            explosion = Explosion(asteroid.position.x, asteroid.position.y, asteroid.radius)
                            self.gsm.score += asteroid.reward
                    
                for hitbox in self.explosion_hitboxes:
                    for asteroid in self.asteroids:
                        if hitbox.check_colision(asteroid) and not asteroid.has_been_hit:
                            asteroid.split()
                            self.gsm.score += asteroid.reward
                    hitbox.kill()

                for ore in self.ores:
                    if ore.check_colision(self.player):
                        self.player.collect_ore(ore.price)
                        ore.kill()

            # Screen update - Pause Menu
            else:
                if self.ui.force_ui_reload:
                    self.redraw_objects_and_ui()

            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000

        # Saving score and going back to Main Menu
        if not self.cheat_godmode and self.gsm.score > 0:
            self.ui.switch_menu(Menu.NAME_CHECK)
            self.getting_player_name = True
            while self.getting_player_name:
                print("> We here")
                self.redraw_objects_and_ui()
                self.player_name, self.getting_player_name = self.get_input_string(self.player_name)
            #self.ui.check_score(self.gsm.score)
        self.ui.switch_menu(Menu.MAIN_MENU)

        self.player = None
        self.gsm = None
        self.asteroid_field = None
        self.ui.player = None
        self.ui.gsm = None

        for object in self.updatable:
            object.kill()

    ### Helpers

    def handle_event(self, event : pygame.event.Event):
        """Used for handling events in all menus"""
        # Returns to fullscreen after Alt-tabing/loosing focus
        if event.type == pygame.WINDOWFOCUSGAINED and self.is_fullscreen:
            self.__switch_to_fullscreen()
            self.ui.force_ui_reload = True
        # Checks button press
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                self.ui.check_click(pygame.mouse.get_pos())
        # Window resizing
        elif event.type == pygame.WINDOWRESIZED and self.is_fullscreen == False:
            self.is_window_resized = True
            self.screen_resolution_windowed = (event.dict["x"], event.dict["y"])
        elif event.type == pygame.WINDOWENTER and self.is_window_resized:
            self.is_window_resized = False
            self.ui.force_ui_reload = True
            self.__switch_to_windowed()
            if self.asteroid_field != None:
                self.asteroid_field.update_spawns(self.screen_resolution)
        #elif event.type != pygame.MOUSEMOTION:
            #print(event)
    
    def redraw_objects_and_ui(self):
        self.ui.force_ui_reload = False

        for object in sorted(list(self.drawable), key = lambda object: object.layer):
            object.draw(self.screen)
    
    def check_if_object_is_off_screen(self, object) -> bool:
        offset = 100
        return (
            object.position.x < -offset or
            object.position.x > self.screen_resolution[0]+offset or
            object.position.y < -offset or
            object.position.y > self.screen_resolution[1]+offset
        )
    
    def get_input_string(self, current_string : str) -> tuple[str, bool]:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                    return current_string, False
                else:
                    self.handle_event(event)

    ### Handlers
    
    def handler_turn_off(self):
        self.is_running = False

    def handler_finish_round(self):
        if self.player != None and self.player.is_alive:
            self.player.is_alive = False

    def handler_regenerate_background(self):
        self.star_field.regenerate()

    def switch_godmode(self):
        self.cheat_godmode = False if self.cheat_godmode else True
        if self.player != None:
            self.player.cheat_godmode = self.cheat_godmode

    def switch_hitbox(self):
        self.cheat_hitbox = False if self.cheat_hitbox else True
        if self.player != None:
            self.player.ship.show_hitbox = self.cheat_hitbox

    def switch_fullscreen(self):
        if not self.is_fullscreen:
            self.is_fullscreen = True
            self.__switch_to_fullscreen()
        else:
            self.is_fullscreen = False
            self.__switch_to_windowed()
    
    def __switch_to_fullscreen(self):
            self.screen_resolution = self.screen_resolution_fullscreen
            flags = pygame.FULLSCREEN
            self.screen = pygame.display.set_mode(self.screen_resolution, flags)
            self.ui.initialize_current_menu()

    def __switch_to_windowed(self):
            self.screen_resolution = self.screen_resolution_windowed
            # Changes mode twice because first change disables fullcreen,
            # second change changes window size
            self.screen = pygame.display.set_mode(self.screen_resolution)
            self.screen = pygame.display.set_mode(self.screen_resolution, pygame.RESIZABLE)
            self.ui.initialize_current_menu()
