import pygame, json, os
from typing import Callable, Any
from enum import Enum

import globals as g
from json_helper.leaderboard.validator import ValidateLeaderboard
from json_helper.profile.validator import ValidateProfile

from sfx_manager import SFXManager, SFX
from groups import GroupManager
from round_stats import RoundStats
from player.ship_enums import ShipModel
from player.player import Player
from world.entity_spawner import EntitySpawner, ESMode
from world.starfield import StarField
from ui.menus.enum_menu import Menu
from vfx.explosions import ExplosionBase, ExplosionSpiky, ExplosionRound
from asteroids.asteroid import Asteroid
from ui.menus.enum_action import Action

class GameStateManager(pygame.sprite.Sprite):
    def __init__(self, sfxm : SFXManager):
        if hasattr(self, "containers"):
            super().__init__(self.containers) # pyright: ignore[reportAttributeAccessIssue]
        else:
            super().__init__()

        self.screen_resolution_windowed : tuple[int, int] = (g.SCREEN_WIDTH, g.SCREEN_HEIGHT)
        self.screen_resolution_fullscreen : tuple[int, int] = pygame.display.get_desktop_sizes()[0]
        self.screen_resolution : tuple[int, int] = self.screen_resolution_windowed
        self.is_fullscreen : bool = False
        self.is_window_resized : bool = False
        self.max_fps = g.MAX_FPS
        self.is_slow = False

        self.is_running : bool = True
        self.is_round_going : bool = False
        self.is_paused : bool = False
        self.is_finishing_a_round : bool = False
        self.death_timer : float = 0.0

        self.switch_menu : Callable[[Menu], None]
        self.update_menu : Callable
        self.held_actions : dict[Action, bool] = {}
        for action in Action:
            self.held_actions[action] = False

        self.sfxm = sfxm
        self.player : Player = Player(self.get_screen_resolution, sfxm, self.held_actions)
        self.spawner = EntitySpawner(self.player, self.get_screen_resolution)
        self.rs : RoundStats = RoundStats(self.player)
        self.star_field = StarField(self.screen_resolution_fullscreen)
        
        # Checking if ./saves/ folder exists
        self.__saves_folder_path = "./saves/"
        if not os.path.exists(self.__saves_folder_path):
            print(f"Creating a `{self.__saves_folder_path}` folder")
            os.makedirs(self.__saves_folder_path)

        # Getting the scores
        self.__leaderboard_path = f"{self.__saves_folder_path}leaderboard.json"
        self._scores = ValidateLeaderboard(self.__leaderboard_path)

        # Getting profiles
        self.__current_profile : int | None = None
        self.__profile_paths : list[str] = [
            f"{self.__saves_folder_path}profile_0.json",
            f"{self.__saves_folder_path}profile_1.json",
            f"{self.__saves_folder_path}profile_2.json"
        ]
        self._profiles : list[dict[str, Any] | None] = [
            ValidateProfile(self.__profile_paths[0]), 
            ValidateProfile(self.__profile_paths[1]), 
            ValidateProfile(self.__profile_paths[2])
        ]

        # Defaults used for loading save in profile selection if something is missing
        self._default_player_name = "Player"
        self._default_ship_index = ShipModel.HAWK3.value # Value of the ShipType Enum

        # Secrets
        self.konami_sequence : list[int] = [82, 82, 81, 81, 80, 79, 80, 79, 5, 4, 40] # Scancodes
        self.konami_progress : int = 0
    
    def update(self, dt : float):
        if self.is_round_going:
            self.update_gameplay(dt)
        elif self.is_finishing_a_round:
            self.update_round_finish(dt)
        else:
            self.update_ambient(dt)

    def update_ambient(self, dt : float):
        for object in g.GM.moving_objects:
            if self.check_if_object_is_off_screen(object):
                object.kill()

    def update_gameplay(self, dt : float):
        if self.player.is_alive and not self.is_paused:
            self.rs.update(dt)

            for object in g.GM.moving_objects:
                if self.check_if_object_is_off_screen(object):
                    if isinstance(object, Asteroid): ##### REWRITE THIS SHITE INSIDE BASE ASTEROID - FUCK IT, USE GM INSTEAD
                        self.spawner.kill_asteroid(object) # The field kills/splits asteroids to keep count of certain types
                    else:
                        object.kill()

            # Colision checks
            # Player hit
            for asteroid in g.GM.asteroids:
                if asteroid.check_colision(self.player) and not self.player.is_invul: # No check for dead asteroids because first loop, only off-screen ones are dead
                    alive = self.player.take_damage_and_check_if_alive()
                    if alive:
                        self.sfxm.play_sound(SFX.PLAYER_HIT)
                    self.spawner.kill_asteroid(asteroid)
                    ExplosionSpiky(asteroid.position, asteroid.radius)
                
                # Asteroid shot
                for projectile in g.GM.projectiles:
                    if projectile.check_colision(asteroid) and not asteroid.is_dead:
                        if projectile.is_single_use:
                            projectile.kill()
                        self.spawner.split_asteroid(asteroid)
                        ExplosionSpiky(asteroid.position, asteroid.radius)
                        self.sfxm.play_sound(SFX.ASTEROID_EXPLOSION)
                        self.rs.score += asteroid.reward
                        self.rs.increase_count_stat(type(asteroid))
                
            # Asteroid exploded
            for hitbox in g.GM.explosion_hitboxes:
                for asteroid in g.GM.asteroids:
                    if hitbox.check_colision(asteroid) and not asteroid.is_dead:
                        self.spawner.split_asteroid(asteroid)
                        self.sfxm.play_sound(SFX.ASTEROID_EXPLOSION)
                        self.rs.score += asteroid.reward
                        self.rs.increase_count_stat(type(asteroid))
                hitbox.kill()

            # Loot collected
            for loot in g.GM.loot:
                if loot.check_colision(self.player):
                    self.player.collect_loot(loot.price)
                    self.sfxm.play_sound(SFX.ORE_COLLECTED)
                    self.rs.increase_count_stat(type(loot))
                    loot.kill()
                elif loot.check_colision(self.player.magnet):
                    loot.home_towards(dt, self.player.position, self.player.magnet.get_strength())

        elif not self.player.is_alive:
            self.finish_round()

    def update_round_finish(self, dt : float):
        if self.death_timer < 2:
            if self.death_timer > 1:
                self.player.is_hidden = True
            self.death_timer += dt
        else:
            self.is_finishing_a_round = False

            # Saving score and going back to Main Menu
            if not self.player.is_sus and self.rs.score > 0:
                self.rs.is_new_record, self.rs.record_place = self.check_score(self.rs.score)
                self.player.stats.process_round_stats(self.rs)
                self.save_profile()
            self.player.teleport_away()
            self.switch_menu(Menu.ROUND_END)

    def start_round(self):
        """
        Run to start a round.
        """
        for object in g.GM.cleanup:
            object.kill()
        self.is_round_going = True
        self.is_paused = False
        self.player.teleport_and_prepare_for_round((int(self.screen_resolution[0] / 2), int(self.screen_resolution[1] / 2)))
        self.spawner.switch_mode(ESMode.ASTEROIDS_STANDARD)
        self.switch_menu(Menu.HUD)

    def finish_round(self):
        """
        Run when the player dies. Plays the death animation and switches to the Round Statistics screen.
        """
        self.is_round_going = False
        self.is_finishing_a_round = True

        if self.is_paused: # For self-destructing
            self.is_paused = False
            self.switch_menu(Menu.HUD)

        self.player.end_round()
        ExplosionRound(self.player.position)
        self.sfxm.play_sound(SFX.PLAYER_DEATH)
        self.death_timer = 0.0

    def cleanup_round(self):
        """
        Run to return from the Round Statistics screen to the main menu.
        """
        for object in g.GM.cleanup:
            object.kill()
        self.spawner.switch_mode(ESMode.AMBIENT)
        self.player.reset()
        self.switch_menu(Menu.MAIN_MENU)

    def pause_game(self):
        self.is_paused = True
        self.switch_menu(Menu.PAUSE_MENU)

    def unpause_game(self):
        self.is_paused = False
        self.switch_menu(Menu.HUD)
    
    def check_if_object_is_off_screen(self, object) -> bool:
        offset = 100
        return (
            object.position.x < -offset or
            object.position.x > self.screen_resolution[0]+offset or
            object.position.y < -offset or
            object.position.y > self.screen_resolution[1]+offset
        )

    def handler_turn_off(self):
        self.is_running = False

    def handler_regenerate_background(self):
        self.star_field.regenerate()

    def get_screen_resolution(self) -> tuple[int, int]:
        return self.screen_resolution
    
    def set_menu_functions(self, function_switch_menu : Callable[[Menu], None], function_update_menu : Callable):
        self.switch_menu = function_switch_menu
        self.update_menu = function_update_menu

    ### Saving

    def save_profile(self):
        if self.__current_profile == None: # In case game is exited before profile is chosen
            return

        path = self.__profile_paths[self.__current_profile]
        save = {
            "version" : 1,
            "player_stats_save" : self.player.stats.get_save()
        }
        print(f"Saving current profile to `{path}`")
        with open(path, "w") as file:
            json.dump(save, file)

    def _load_profile(self, index):
        self.__current_profile = index
        profile = self._profiles[index]

        if profile["version"] >= 1:
            self.player.stats.load_save(profile["player_stats_save"])

        self.switch_menu(Menu.MAIN_MENU)

    def _new_profile(self, index):
        self.switch_menu(Menu.NEW_PROFILE)
        self.__current_profile = index

    def _delete_profile(self, index):
        try:
            os.remove(self.__profile_paths[index])
            print(f"Removed file `{self.__profile_paths[index]}`")
            self._profiles[index] = None
        except Exception as e:
            print(f"Error removing file `{self.__profile_paths[index]}`: {e}")
        self.update_menu()

    # def _rename_player(self, starting_menu : Menu):
    #     self.switch_menu(Menu.NAME_EDIT)
    #     if self.game.get_player_name():
    #         self.switch_menu(starting_menu)
    #     elif self.player.stats.name == "":
    #         self.player.stats.name = "Player"

    def _return_to_profile_selection(self):
        """Used to return from the Main Menu back to the Profile Selection."""

        if self.__current_profile != None:
            self.save_profile()
            self._profiles[self.__current_profile] = ValidateProfile(self.__profile_paths[self.__current_profile])
        self.__current_profile = None
        self.player.kill()
        self.player = Player(self.get_screen_resolution, self.sfxm, self.held_actions)
        self.switch_menu(Menu.PROFILE_SELECTION)

    def check_score(self, new_score) -> tuple[bool, int]:
        """
        Returns (True, place : int) if new leaderboard record is set.
        
        Otherwise (False, 0).
        """

        is_updated = False

        # Overfilled
        while len(self._scores) > g.LEADERBOARD_LENGTH:   # Shortens leaderboard if max length was reduced
            is_updated = True
            self._scores.pop()

        # Empty
        if len(self._scores) == 0:
            self._scores.append({"name": self.player.stats.name, "score": new_score})
            self.__save_leaderboard()
            return True, 1

        # Full/Partially filled
        for i in range(len(self._scores)):
            if new_score > self._scores[i]["score"]:
                if len(self._scores) == g.LEADERBOARD_LENGTH:
                    self._scores.pop()
                self._scores.append({"name": self.player.stats.name, "score": new_score})
                self._scores.sort(key=lambda x: x["score"], reverse=True)
                self.__save_leaderboard()
                return True, i+1
            
        # New lowest :sadge:
        if len(self._scores) < g.LEADERBOARD_LENGTH:
                self._scores.append({"name": self.player.stats.name, "score": new_score})
                self.__save_leaderboard()
                return True, len(self._scores)
            
        # No new record
        if is_updated: # In case was overfilled
            self.__save_leaderboard()
        return False, 0

    def _reset_leaderboard(self):
        self._scores = []
        self.__save_leaderboard()
        self.update_menu()

    def __save_leaderboard(self):
        print(f"Saving leaderboard to `{self.__leaderboard_path}`")
        with open(self.__leaderboard_path, "w") as file:
            json.dump(self._scores, file)

    ### Secret stuff

    def unlock_cheats(self):
        self.player.stats.found_cheats = True
        self.sfxm.play_sound(SFX.SECRET_CHEATS)
        self.update_menu()

    def unlock_ship(self, ship_type : ShipModel):
        self.player.stats.unlock_ship(ship_type)
        self.update_menu()

    def switch_low_fps(self):
        self.max_fps = 75 if self.max_fps == 10 else 10
        self.is_slow = False if self.is_slow else True

    def switch_fullscreen(self):
        if not self.is_fullscreen:
            self.is_fullscreen = True
            self.switch_to_fullscreen()
        else:
            self.is_fullscreen = False
            self.switch_to_windowed()
    
    def switch_to_fullscreen(self):
            self.screen_resolution = self.screen_resolution_fullscreen
            flags = pygame.FULLSCREEN
            self.screen = pygame.display.set_mode(self.screen_resolution, flags)
            self.update_menu()

    def switch_to_windowed(self):
            self.screen_resolution = self.screen_resolution_windowed
            # Changes mode twice because first change disables fullcreen,
            # second change changes window size
            self.screen = pygame.display.set_mode(self.screen_resolution)
            self.screen = pygame.display.set_mode(self.screen_resolution, pygame.RESIZABLE)
            self.update_menu()
