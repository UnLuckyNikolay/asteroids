from player.ship import ShipType

from asteroids.asteroid import Asteroid
from asteroids.asteroidbasic import AsteroidBasic
from asteroids.asteroidexplosive import AsteroidExplosive
from asteroids.asteroidgolden import AsteroidGolden
from asteroids.asteroidhoming import AsteroidHoming
from asteroids.ores import Ore, CopperOre, SilverOre, GoldenOre, Diamond


class PlayerStats():
    """Used to keep track of and save certain player stats outside of rounds."""

    def __init__(self):
        self.player = None
        self.name : str = "" # Empty for the Profile creation, default while loading a save is "Player"
        self.max_score : int = 0

        self.unlocked_ships : list[list[int | bool]] = [
            [int(ShipType.POLY.value), True],
            [int(ShipType.POLY2BP.value), True],
            [int(ShipType.POLY2.value), True],
            [int(ShipType.POLY3.value), True],
            [int(ShipType.UFO.value), False],
        ]
        self.unlocked_ships_amount = self.__get_amount_of_unlocked_ship()
        self.__ship_model_index : int = 3 # Index for the .unlocked_ships
        self.ship_model_value : int = self.unlocked_ships[self.ship_model_index][0] # For Profile selection ship

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
    def ship_model_index(self):
        return self.__ship_model_index
    
    @ship_model_index.setter
    def ship_model_index(self, value : int):
        if self.unlocked_ships[self.ship_model_index][1]:
            self.__ship_model_index = value
            self.ship_model_value = self.unlocked_ships[self.__ship_model_index][0]
            if self.player != None:
                self.player.ship.switch_model(self.unlocked_ships[self.ship_model_index][0])

    def unlock_ship(self, ship_type : ShipType):
        id = ship_type.value
        for i in range(len(self.unlocked_ships)):
            if self.unlocked_ships[i][0] == id:
                self.unlocked_ships[i][1] = True
                self.unlocked_ships_amount = self.__get_amount_of_unlocked_ship()
                return
            
    def check_unlocked_ship(self, ship_type : ShipType):
        id = ship_type.value
        for i in range(len(self.unlocked_ships)):
            if self.unlocked_ships[i][0] == id:
                return self.unlocked_ships[i][1]
                

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
        self.player.ship.switch_model(self.unlocked_ships[self.ship_model_index][0])

    def get_save(self) -> dict:
        player_stats_save = {
            "version" : 1,

            "name" : self.name,
            "max_score" : self.max_score,

            # Ship
            "unlocked_ships" : self.unlocked_ships,
            "ship_model_index" : self.ship_model_index,
            "ship_model_value" : self.ship_model_value,

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
            self.name = player_stats_save.get("name", "Player") # Different to default
            self.max_score = player_stats_save.get("max_score", self.max_score)

            # Ship
            self.unlocked_ships = player_stats_save.get("unlocked_ships", self.unlocked_ships)
            self.ship_model_index = player_stats_save.get("ship_model_index", self.ship_model_index)
            self.unlocked_ships_amount = self.__get_amount_of_unlocked_ship()

            # Cheats
            self.found_cheats = player_stats_save.get("found_cheats", self.found_cheats)
            self.cheat_godmode = player_stats_save.get("cheat_godmode", self.cheat_godmode)
            self.cheat_stonks = player_stats_save.get("cheat_stonks", self.cheat_stonks)
            self.cheat_hitbox = player_stats_save.get("cheat_hitbox", self.cheat_hitbox)
                
            # Kills
            self.destroyed_asteroids = player_stats_save.get("destroyed_asteroids", self.destroyed_asteroids)
            self.destroyed_asteroids_basic = player_stats_save.get("destroyed_asteroids_basic", self.destroyed_asteroids_basic)
            self.destroyed_asteroids_explosive = player_stats_save.get("destroyed_asteroids_explosive", self.destroyed_asteroids_explosive)
            self.destroyed_asteroids_golden = player_stats_save.get("destroyed_asteroids_golden", self.destroyed_asteroids_golden)
            self.destroyed_asteroids_homing = player_stats_save.get("destroyed_asteroids_homing", self.destroyed_asteroids_homing)
            
            # Loot
            self.collected_loot = player_stats_save.get("collected_loot", self.collected_loot)
            self.collected_ores_copper = player_stats_save.get("collected_ores_copper", self.collected_ores_copper)
            self.collected_ores_silver = player_stats_save.get("collected_ores_silver", self.collected_ores_silver)
            self.collected_ores_golden = player_stats_save.get("collected_ores_golden", self.collected_ores_golden)
            self.collected_diamonds = player_stats_save.get("collected_diamonds", self.collected_diamonds)

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
        next = (self.ship_model_index+1) % self.unlocked_ships_amount
        while True:
            if self.unlocked_ships[next][1]:
                self.ship_model_index = next
                return
            next = (next+1) % self.unlocked_ships_amount
    
    def switch_ship_model_to_previous(self):
        next = (self.ship_model_index-1) % self.unlocked_ships_amount
        while True:
            if self.unlocked_ships[next][1]:
                self.ship_model_index = next
                return
            next = (next-1) % self.unlocked_ships_amount
    
    def __get_amount_of_unlocked_ship(self) -> int:
        amount = 0
        for ship in self.unlocked_ships:
            if ship[1]:
                amount += 1
        return amount