from player.ship import ShipType

from asteroids.asteroid import Asteroid
from asteroids.asteroidbasic import AsteroidBasic
from asteroids.asteroidexplosive import AsteroidExplosive
from asteroids.asteroidgolden import AsteroidGolden
from asteroids.asteroidhoming import AsteroidHoming
from asteroids.ores import Ore, CopperOre, SilverOre, GoldenOre, Diamond


class PlayerStats():
    """Used to keep track of certain player stats outside of rounds."""
    def __init__(self):
        self.name : str = ""
        self.max_score : int = 0

        self.__ship_model : int = 3        
        self.unlocked_ships = [
            ShipType.POLY,
            ShipType.POLY2BP,
            ShipType.POLY2,
            ShipType.POLY3,
            ShipType.UFO,
        ]

        self.found_cheats : bool = False
        self.cheat_godmode : bool = False
        self.cheat_stonks : bool = False
        self.cheat_hitbox : bool = False

        self.destroyed_asteroids : int = 0
        self.destroyed_asteroids_basic : int = 0
        self.destroyed_asteroids_explosive : int = 0
        self.destroyed_asteroids_golden : int = 0
        self.destroyed_asteroids_homing : int = 0

        self.collected_loot : int = 0
        self.collected_ores_copper : int = 0
        self.collected_ores_silver : int = 0
        self.collected_ores_golden : int = 0
        self.collected_diamonds : int = 0


    @property
    def ship_model(self):
        return self.__ship_model
    
    @ship_model.setter
    def ship_model(self, value : int):
        self.__ship_model = value
        self.player.ship.switch_model(self.unlocked_ships[self.ship_model])

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

    def set_player(self, player):
        self.player = player
        self.player.ship.switch_model(self.unlocked_ships[self.ship_model])

    def get_save(self) -> dict:
        player_stats_save = {
            "version" : 1,

            "name" : self.name,
            "max_score" : self.max_score,

            "ship_model" : self.ship_model,

            # Cheats
            "found_cheats" : self.found_cheats,
            "cheat_godmode" : self.cheat_godmode,
            "cheat_stonks" : self.cheat_stonks,
            "cheat_hitbox" : self.cheat_hitbox,

            # Kills
            "destroyed_asteroids" : self.destroyed_asteroids,
            "destroyed_asteroids_basic" : self.destroyed_asteroids_basic,
            "destroyed_asteroids_explosive" : self.destroyed_asteroids_explosive,
            "destroyed_asteroids_golden" : self.destroyed_asteroids_golden,
            "destroyed_asteroids_homing" : self.destroyed_asteroids_homing,
            
            # Loot
            "collected_loot" : self.collected_loot,
            "collected_ores_copper" : self.collected_ores_copper,
            "collected_ores_silver" : self.collected_ores_silver,
            "collected_ores_golden" : self.collected_ores_golden,
            "collected_diamonds" : self.collected_diamonds,
        }

        return player_stats_save
    
    def load_save(self, player_stats_save : dict):
        if player_stats_save["version"] == 1:
            self.name = player_stats_save.get("name", "Player")
            self.max_score = player_stats_save.get("max_score", 0)

            self.ship_model = player_stats_save.get("ship_model", 3)

            # Cheats
            self.found_cheats = player_stats_save.get("found_cheats", False)
            self.cheat_godmode = player_stats_save.get("cheat_godmode", False)
            self.cheat_stonks = player_stats_save.get("cheat_stonks", False)
            self.cheat_hitbox = player_stats_save.get("cheat_hitbox", False)
                
            # Kills
            self.destroyed_asteroids = player_stats_save.get("destroyed_asteroids", 0)
            self.destroyed_asteroids_basic = player_stats_save.get("destroyed_asteroids_basic", 0)
            self.destroyed_asteroids_explosive = player_stats_save.get("destroyed_asteroids_explosive", 0)
            self.destroyed_asteroids_golden = player_stats_save.get("destroyed_asteroids_golden", 0)
            self.destroyed_asteroids_homing = player_stats_save.get("destroyed_asteroids_homing", 0)
            
            # Loot
            self.collected_loot = player_stats_save.get("collected_loot", 0)
            self.collected_ores_copper = player_stats_save.get("collected_ores_copper", 0)
            self.collected_ores_silver = player_stats_save.get("collected_ores_silver", 0)
            self.collected_ores_golden = player_stats_save.get("collected_ores_golden", 0)
            self.collected_diamonds = player_stats_save.get("collected_diamonds", 0)

    def check_max_score(self, score : int):
        if score > self.max_score:
            self.max_score = score

    def switch_godmode(self):
        self.cheat_godmode = False if self.cheat_godmode else True

    def switch_stonks(self):
        self.cheat_stonks = False if self.cheat_stonks else True

    def switch_hitbox(self):
        self.cheat_hitbox = False if self.cheat_hitbox else True
        
    def switch_ship_model_to_next(self):
        self.ship_model = (self.ship_model+1) % len(self.unlocked_ships)
    
    def switch_ship_model_to_previous(self):
        self.ship_model = (self.ship_model-1) % len(self.unlocked_ships)