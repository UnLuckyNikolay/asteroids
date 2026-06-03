# pyright: reportAttributeAccessIssue=false

import pygame

import globals as g
from config import *
from game_state_manager import GameStateManager, GameState
from ui.menus.manager_menu import MenuManager
from sfx_manager import SFXManager

from player.player import Player
from player.weapons.projectiles.projectileplasma import ProjectilePlasma
from player.weapons.projectiles.bomb import Bomb
from player.weapons.projectiles.bombexplosion import BombExplosion
from player.weapons.projectiles.literally_a_fucking_meat_cleaver import LiterallyAFuckingMeatCleaverBase
from vfx.explosions import ExplosionBase, ExplosionSpiky, ExplosionRound
from ui.elements.text import TextAnimated
from ui.elements.container import Container

from world.starfield import StarField
from world.entity_spawner import EntitySpawner
from asteroids.asteroid import Asteroid
from asteroids.ores import Ore


class Game():
    def __init__(self):
        pygame.mixer.pre_init(
            frequency=44100,
            size=-16,
            channels=2,
            buffer=1024,
        )
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE, display=0)
        pygame.display.set_caption("Asteroids from Outer Space")

        self.clock = pygame.time.Clock()
        self.dt = 0
        self.is_running : bool = True
        self.is_paused : bool = False
        self.getting_player_name : bool = False
        self.is_round_end : bool = False

        self.initialize_groups()
        self.sfxm : SFXManager = SFXManager() # All sfx file paths are stored inside SFXManager
        self.gsm : GameStateManager = GameStateManager(self.sfxm)
        self.mm : MenuManager = MenuManager(self.gsm, self.sfxm)
        self.gsm.set_menu_functions(self.mm.switch_menu, self.mm.initialize_current_menu)

    def initialize_groups(self):
        MenuManager.containers = (
            g.GM.drawable
        )
        GameStateManager.containers = (
            g.GM.updatable_gameplay,
        )
        SFXManager.containers = (
            g.GM.updatable_gameplay,
        )

        TextAnimated.containers = (
            g.GM.updatable_ui,
        )
        Container.containers = (
            g.GM.updatable_ui,
        )

        StarField.containers = (
            g.GM.drawable,
        )
        ExplosionBase.containers = (
            g.GM.updatable_gameplay, 
            g.GM.drawable, 
            g.GM.cleanup,
        )

        Player.containers = (
            g.GM.updatable_gameplay, 
            g.GM.drawable,
        )
        ProjectilePlasma.containers = (
            g.GM.projectiles, 
            g.GM.updatable_gameplay, 
            g.GM.drawable, 
            g.GM.moving_objects, 
            g.GM.cleanup,
        )
        Bomb.containers = (
            g.GM.drawable, 
            g.GM.updatable_gameplay, 
            g.GM.cleanup,
        )
        BombExplosion.containers = (
            g.GM.explosion_hitboxes, 
            g.GM.cleanup,
        )
        LiterallyAFuckingMeatCleaverBase.containers = (
            g.GM.projectiles, 
            g.GM.updatable_gameplay, 
            g.GM.drawable, 
            g.GM.moving_objects, 
            g.GM.cleanup,
        )

        EntitySpawner.containers = (
            g.GM.updatable_gameplay, 
            g.GM.updatable_ambient, 
        )
        Asteroid.containers = (
            g.GM.asteroids, 
            g.GM.updatable_gameplay, 
            g.GM.updatable_ambient, 
            g.GM.drawable, 
            g.GM.moving_objects, 
            g.GM.cleanup,
        )
        Ore.containers = (
            g.GM.loot, 
            g.GM.updatable_gameplay, 
            g.GM.drawable, 
            g.GM.moving_objects, 
            g.GM.cleanup,
        )

    ### THE MAIN LOOP

    def run(self):
        """
        The main loop.
        
        Checks events, updates everything, and redraws the screen.
        """
        
        while self.gsm.is_running:
            self.update_all()
            self.dt = self.process_and_refresh()

        self.gsm.save_profile() # Save on exit
    
    def update_all(self):
        """Updates current UI, and needed entities according to the current game state."""
        for object in g.GM.updatable_ui:
            object.update(self.dt)

        match self.gsm.game_state:
            case GameState.PLAYING:
                for object in g.GM.updatable_ambient:
                    object.update(self.dt)
            case GameState.PLAYING | GameState.PLAYER_BEING_REDUCED_TO_ATOMS:
                for object in g.GM.updatable_gameplay:
                    object.update(self.dt)

    def process_and_refresh(self) -> float:
        """
        Checks events and redraws the screen. Returns delta.
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gsm.is_running = False
                break
            else: ### REWRITE WITH DICTIONARY
                # Returns to fullscreen after Alt-tabing/loosing focus
                if event.type == pygame.WINDOWFOCUSGAINED and self.gsm.is_fullscreen:
                    self.gsm.switch_to_fullscreen()
                # Try button press
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == pygame.BUTTON_LEFT:
                        self.mm.try_button_press()
                # Window resizing
                elif event.type == pygame.WINDOWRESIZED and self.gsm.is_fullscreen == False:
                    self.gsm.is_window_resized = True
                    self.gsm.screen_resolution_windowed = (event.dict["x"], event.dict["y"])
                elif event.type == pygame.WINDOWENTER and self.gsm.is_window_resized:
                    self.gsm.is_window_resized = False
                    self.gsm.switch_to_windowed()
                    self.gsm.spawner.update_spawns(self.gsm.screen_resolution)
                #elif event.type != pygame.MOUSEMOTION:
                    #print(event)
                elif event.type == pygame.KEYDOWN:
                    self.mm.check_keyboard_input_pressed(event)
                elif event.type == pygame.KEYUP:
                    self.mm.check_keyboard_input_unpressed(event)
        
        return self.redraw_objects_and_ui()
    
    def redraw_objects_and_ui(self) -> float:
        """
        Updates and redraws the screen, returns delta time.
        """

        self.mm.check_hovered_button()
        for object in sorted(list(g.GM.drawable), key = lambda object: object.layer):
            object.draw(self.screen)

        pygame.display.flip()
        dt = self.clock.tick(self.gsm.max_fps) / 1000
        return dt

    ### Helpers

    def handle_keyboard_event_for_ship_controls(self, event : pygame.event.Event):
        """Used for handling inputs for controlling the ship during gameplay and pause."""

        if self.rsm == None:
            return

        match event.scancode:
            # Weapon switching
            case 30 | 89: # 1 | Keypad1
                if event.type == pygame.KEYDOWN and not self.is_paused:
                    self.player.weapon_current = self.player.weapon_plasmagun
            case 31 | 90: # 2 | Keypad2
                if event.type == pygame.KEYDOWN and not self.is_paused:
                    self.player.weapon_current = self.player.weapon_bomblauncher
            case 32 | 91: # 3 | Keypad3
                if self.player_stats.cheat_cleavers and event.type == pygame.KEYDOWN and not self.is_paused:
                    self.player.weapon_current = self.player.weapon_meat
    
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
