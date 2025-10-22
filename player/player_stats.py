from player.ship import ShipType


class PlayerStats():
    """Used to keep track of certain player stats outside of rounds."""
    def __init__(self):
        self.name : str = ""

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


    @property
    def ship_model(self):
        return self.__ship_model
    
    @ship_model.setter
    def ship_model(self, value : int):
        self.__ship_model = value
        self.player.ship.switch_model(self.unlocked_ships[self.ship_model])

    def set_player(self, player):
        self.player = player
        self.player.ship.switch_model(self.unlocked_ships[self.ship_model])

    def get_save(self) -> dict:
        player_stats_save = {
            "version" : 1,

            "name" : self.name,

            "ship_model" : self.ship_model,

            "found_cheats" : self.found_cheats,
            "cheat_godmode" : self.cheat_godmode,
            "cheat_hitbox" : self.cheat_hitbox,
            "cheat_stonks" : self.cheat_stonks,
        }

        return player_stats_save
    
    def load_save(self, player_stats_save : dict):
        if player_stats_save["version"] == 1:
            self.name = player_stats_save["name"]

            self.ship_model = player_stats_save["ship_model"]

            self.found_cheats = player_stats_save["found_cheats"]
            self.cheat_godmode = player_stats_save["cheat_godmode"]
            self.cheat_hitbox = player_stats_save["cheat_hitbox"]
            self.cheat_stonks = player_stats_save["cheat_stonks"]

    def switch_godmode(self):
        self.cheat_godmode = False if self.cheat_godmode else True

    def switch_stonks(self):
        self.cheat_stonks = False if self.cheat_stonks else True

    def switch_hitbox(self):
        self.cheat_hitbox = False if self.cheat_hitbox else True
        self.player.ship.switch_hitbox_to(self.cheat_hitbox)
        
    def switch_ship_model_to_next(self):
        self.ship_model = (self.ship_model+1) % len(self.unlocked_ships)
    
    def switch_ship_model_to_previous(self):
        self.ship_model = (self.ship_model-1) % len(self.unlocked_ships)