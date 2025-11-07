from player.ship import ShipModel

from ui.helpers import get_time_as_text
from round_state_manager import RoundStateManager


class PlayerStats():
    """Used to keep track of and save certain player stats outside of rounds."""

    def __init__(self):
        self.player = None
        self.name : str = "" # Empty for the Profile creation, default while loading a save is "Player"
        self.max_score : int = 0
        self.longest_run : float = 0 # In seconds

        self.unlocked_ships : list[list[int | bool]] = [
            [int(ShipModel.POLY1.value), True],
            [int(ShipModel.HAWK1.value), True],
            [int(ShipModel.HAWK2.value), True],
            [int(ShipModel.HAWK3.value), True],
            [int(ShipModel.UFO2.value), False],
        ]
        self.unlocked_ships_amount = self.__get_amount_of_unlocked_ship()
        self.__ship_model_index : int = 3 # Index for the .unlocked_ships
        self.ship_model_value : int = self.unlocked_ships[self.ship_model_index][0] # For Profile selection ship
        self.ship_color_profile : int = 0

        self.found_cheats : bool = False
        self.cheat_godmode : bool = False
        self.cheat_stonks : bool = False
        self.cheat_cleavers : bool = False

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


    @property
    def ship_model_index(self):
        return self.__ship_model_index
    
    @ship_model_index.setter
    def ship_model_index(self, value : int):
        if self.unlocked_ships[self.ship_model_index][1]:
            self.__ship_model_index = value
            self.ship_model_value = self.unlocked_ships[self.__ship_model_index][0]
            if self.player != None:
                self.player.ship.switch_model(self.unlocked_ships[self.ship_model_index][0], self.ship_color_profile)

    def unlock_ship(self, ship_type : ShipModel):
        id = ship_type.value
        for i in range(len(self.unlocked_ships)):
            if self.unlocked_ships[i][0] == id:
                self.unlocked_ships[i][1] = True
                self.unlocked_ships_amount = self.__get_amount_of_unlocked_ship()
                return
            
    def check_unlocked_ship(self, ship_type : ShipModel) -> bool: # pyright: ignore[reportReturnType]
        id = ship_type.value
        for i in range(len(self.unlocked_ships)):
            if self.unlocked_ships[i][0] == id:
                return self.unlocked_ships[i][1] # pyright: ignore[reportReturnType]

    def process_round_stats(self, rsm : RoundStateManager):
        if rsm.score > self.max_score:
            self.max_score = rsm.score
        if rsm.round_time > self.longest_run:
            self.longest_run = rsm.round_time
        
        self.destroyed_asteroids += rsm.destroyed_asteroids
        self.destroyed_asteroids_basic += rsm.destroyed_asteroids_basic
        self.destroyed_asteroids_bouncy += rsm.destroyed_asteroids_bouncy
        self.destroyed_asteroids_explosive += rsm.destroyed_asteroids_explosive
        self.destroyed_asteroids_homing += rsm.destroyed_asteroids_homing
        self.destroyed_asteroids_golden += rsm.destroyed_asteroids_golden

        self.collected_loot += rsm.collected_loot
        self.collected_ores_copper += rsm.collected_ores_copper
        self.collected_ores_silver += rsm.collected_ores_silver
        self.collected_ores_golden += rsm.collected_ores_golden
        self.collected_diamonds += rsm.collected_diamonds

    def set_player(self, player):
        self.player = player
        self.player.ship.switch_model(self.unlocked_ships[self.ship_model_index][0], self.ship_color_profile)

    def get_save(self) -> dict:
        player_stats_save = {
            "version" : 1,

            "name" : self.name,
            "max_score" : self.max_score,
            "longest_run" : self.longest_run,

            # Ship
            "unlocked_ships" : self.unlocked_ships,
            "ship_model_index" : self.ship_model_index,
            "ship_model_value" : self.ship_model_value,
            "ship_color_profile" : self.ship_color_profile,

            # Cheats
            "found_cheats" : self.found_cheats,
            "cheat_godmode" : self.cheat_godmode,
            "cheat_stonks" : self.cheat_stonks,
            "cheat_cleavers" : self.cheat_cleavers,

            # Kills
            "destroyed_asteroids" : self.destroyed_asteroids,
            "destroyed_asteroids_basic" : self.destroyed_asteroids_basic,
            "destroyed_asteroids_bouncy" : self.destroyed_asteroids_bouncy,
            "destroyed_asteroids_explosive" : self.destroyed_asteroids_explosive,
            "destroyed_asteroids_homing" : self.destroyed_asteroids_homing,
            "destroyed_asteroids_golden" : self.destroyed_asteroids_golden,
            
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
            self.longest_run = player_stats_save.get("longest_run", self.longest_run)

            # Ship
            self.unlocked_ships = player_stats_save.get("unlocked_ships", self.unlocked_ships)
            self.ship_model_index = player_stats_save.get("ship_model_index", self.ship_model_index)
            self.ship_color_profile = player_stats_save.get("ship_color_profile", self.ship_color_profile)
            self.unlocked_ships_amount = self.__get_amount_of_unlocked_ship()

            # Cheats
            self.found_cheats = player_stats_save.get("found_cheats", self.found_cheats)
            self.cheat_godmode = player_stats_save.get("cheat_godmode", self.cheat_godmode)
            self.cheat_stonks = player_stats_save.get("cheat_stonks", self.cheat_stonks)
            self.cheat_cleavers = player_stats_save.get("cheat_cleavers", self.cheat_cleavers)
                
            # Kills
            self.destroyed_asteroids = player_stats_save.get("destroyed_asteroids", self.destroyed_asteroids)
            self.destroyed_asteroids_basic = player_stats_save.get("destroyed_asteroids_basic", self.destroyed_asteroids_basic)
            self.destroyed_asteroids_bouncy = player_stats_save.get("destroyed_asteroids_bouncy", self.destroyed_asteroids_bouncy)
            self.destroyed_asteroids_explosive = player_stats_save.get("destroyed_asteroids_explosive", self.destroyed_asteroids_explosive)
            self.destroyed_asteroids_homing = player_stats_save.get("destroyed_asteroids_homing", self.destroyed_asteroids_homing)
            self.destroyed_asteroids_golden = player_stats_save.get("destroyed_asteroids_golden", self.destroyed_asteroids_golden)
            
            # Loot
            self.collected_loot = player_stats_save.get("collected_loot", self.collected_loot)
            self.collected_ores_copper = player_stats_save.get("collected_ores_copper", self.collected_ores_copper)
            self.collected_ores_silver = player_stats_save.get("collected_ores_silver", self.collected_ores_silver)
            self.collected_ores_golden = player_stats_save.get("collected_ores_golden", self.collected_ores_golden)
            self.collected_diamonds = player_stats_save.get("collected_diamonds", self.collected_diamonds)

        if self.player != None:
            self.player.ship.switch_model(self.unlocked_ships[self.ship_model_index][0], self.ship_color_profile)

    def get_longest_time_as_text(self) -> str:
        return get_time_as_text(self.longest_run)

    def switch_godmode(self):
        self.cheat_godmode = False if self.cheat_godmode else True

    def switch_stonks(self):
        self.cheat_stonks = False if self.cheat_stonks else True

    def switch_cleavers(self):
        self.cheat_cleavers = False if self.cheat_cleavers else True
        
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