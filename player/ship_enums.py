from enum import Enum

# New models should be added to:
# ship.get_name
# ship.__get_parts
# ship -> _get_parts_*model name*
# ship -> get_color_profile
class ShipModel(Enum):
    POLY1 = 11
    HAWK1 = 21
    HAWK2 = 22
    HAWK3 = 23
    UFO2 = 32

# New upgrades should be added to:
# player.get_upgrade_level 
# player.buy_upgrade
class ShipUpgrade(Enum):
    """List of player upgrades"""

    ENGINE_SPEED = "Engine: Speed"
    ENGINE_ACCELERATION = "Engine: Acceleration"
    MAGNET_RADIUS = "Magnet: Radius"
    MAGNET_STRENGTH = "Magnet: Strength"
    PLASMAGUN_PROJECTILES = "Plasma Gun: Projectiles"
    PLASMAGUN_COOLDOWN = "Plasma Gun: Cooldown"
    BOMBLAUNCHER_RADIUS = "Bomb Launcher: Radius"
    BOMBLAUNCHER_FUSE = "Bomb Launcher: Fuse"

# New parts should be added to:
# player.get_part_level
class ShipPart(Enum):
    """List of player parts"""

    ENGINE = "Engine"
    MAGNET = "Magnet"
    PLASMAGUN = "Plasma Gun"
    BOMBLAUNCHER = "Bomb Launcher"