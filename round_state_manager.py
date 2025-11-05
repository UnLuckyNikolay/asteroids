import pygame

from constants import *
from ui.helpers import get_time_as_text
from asteroids.asteroid import Asteroid
from asteroids.asteroidbasic import AsteroidBasic
from asteroids.asteroidexplosive import AsteroidExplosive
from asteroids.asteroidgolden import AsteroidGolden
from asteroids.asteroidhoming import AsteroidHoming
from asteroids.asteroidbouncy import AsteroidBouncy
from asteroids.ores import Ore, CopperOre, SilverOre, GoldenOre, Diamond


class RoundStateManager(pygame.sprite.Sprite):
    def __init__(self, player):
        if hasattr(self, "containers"):
            super().__init__(self.containers) # pyright: ignore[reportAttributeAccessIssue]
        else:
            super().__init__()

        self.player = player
        self.score = 0
        self.old_pb = player.stats.max_score
        self.round_time : float = 0 # In seconds

        self.is_new_record : bool = False
        self.record_place : int = 0
        
        self.destroyed_asteroids : int = 0
        self.destroyed_asteroids_basic : int = 0
        self.destroyed_asteroids_bouncy : int = 0
        self.destroyed_asteroids_explosive : int = 0
        self.destroyed_asteroids_homing : int = 0
        self.destroyed_asteroids_golden : int = 0

        self.collected_loot : int = 0
        self.collected_ores_copper : int = 0
        self.collected_ores_silver : int = 0
        self.collected_ores_golden : int = 0
        self.collected_diamonds : int = 0


    def update(self, delta : float):
        if self.player.is_alive:
            self.round_time += delta

    def get_time_as_text(self) -> str:
        return get_time_as_text(self.round_time)
    
    def increase_count_stat(self, entity_type : type):
        """Used for destroying asteroids and collecting loot."""

        if issubclass(entity_type, Asteroid):
            self.destroyed_asteroids += 1
            if entity_type == AsteroidBasic:
                self.destroyed_asteroids_basic += 1
            elif entity_type == AsteroidExplosive:
                self.destroyed_asteroids_explosive += 1
            elif entity_type == AsteroidGolden:
                self.destroyed_asteroids_golden += 1
            elif entity_type == AsteroidHoming:
                self.destroyed_asteroids_homing += 1
            elif entity_type == AsteroidBouncy:
                self.destroyed_asteroids_bouncy += 1
            else:
                print(f"ERROR: Asteroid `{entity_type}` is missing from PlayerStats.increase_count_stat.")
        elif issubclass(entity_type, Ore):
            self.collected_loot += 1
            if entity_type == CopperOre:
                self.collected_ores_copper += 1
            elif entity_type == SilverOre:
                self.collected_ores_silver += 1
            elif entity_type == GoldenOre:
                self.collected_ores_golden += 1
            elif entity_type == Diamond:
                self.collected_diamonds += 1
            else:
                print(f"ERROR: Loot `{entity_type}` is missing from PlayerStats.increase_count_stat.")
        else:
            print(f"ERROR: `{entity_type}` is missing from PlayerStats.increase_count_stat.")

    def get_round_title(self) -> str:
        """Returns the Title for the Round end screen."""

        if self.score == 69:
            return "Nice!"
        
        if self.score == 420:
            return "Blaze it!"
        
        if self.score == 1337:
            return "Leet!"

        if self.player.is_sus:
            return "Having fun?"
        
        if self.record_place > 0 and self.record_place < 5:
            return f"Top {self.record_place}!"
        
        if self.score > self.old_pb:
            return "New PB!"
        
        if self.score > 500:
            return "Good run!"
        
        return "You tried"
    