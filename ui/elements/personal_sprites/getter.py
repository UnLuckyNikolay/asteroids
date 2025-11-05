from typing import Any
from ui.elements.personal_sprites.amoguses import AmogusBlue, AmogusPink


def get_personal_sprite(player_name : str) -> Any | None:
    """
    Returns a personal sprite with __init__(local_x, local_y).
    
    Returns None if no sprite is found.
    """
    
    match player_name.lower():
        case "ben" | "plainben":
            return AmogusBlue
        case "marou":
            return AmogusPink
        case _:
            return None