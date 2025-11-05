from ui.colors import *
from ui.elements.container import Container, Allignment
from ui.elements.buttons import Button, ButtonRound, Switch, InfoButton, ModKey
from ui.elements.text import TextPlain, TextUpdated
from ui.font_builder import FontBuilder
from ui.menus.enum import Menu
from round_state_manager import RoundStateManager
from player.player_stats import PlayerStats
from player.player import Player
from ui.elements.sprites.healthbar import HealthBar

def initialize_hud(
    game,
    gsm,
    rsm : RoundStateManager,
    player_stats : PlayerStats,
    player : Player,
    fonts : FontBuilder
) -> tuple[list, list]:
    
    containers : list[Container] = []
    buttons : list[Button | Switch] = []

    # Space between elements - 10
    
    # <> Containers <>

    # Current weapon
    c_weapon = Container((25, 25), (362, 36), (10, 5, 5, 5))
    c_weapon.add_element(
        TextUpdated(
            "{}.v{}", fonts.small, color_white, 
            player.get_current_weapon_name,
            player.get_current_weapon_level
        ),
        Allignment.LEFT_WALL,
        nudge=(9, 0)
    )
    # Timer
    c_timer = Container((397, 25), (176, 36), (5, 10, 5, 5))
    c_timer.add_element(
        TextUpdated(
            "Time: {}", fonts.small, color_white, 
            rsm.get_time_as_text
        ),
        Allignment.LEFT_WALL,
        nudge=(9, 0)
    )
    # Current score
    c_score = Container((25, 71), (176, 36), (5, 3, 5, 10))
    c_score.add_element(
        TextUpdated(
            "{}pts", fonts.small, color_white, 
            lambda: rsm.score
        ),
        Allignment.LEFT_WALL,
        nudge=(9, 0)
    )
    # Current money
    c_money = Container((211, 71), (176, 36), (3, 3, 3, 3))
    c_money.add_element(
        TextUpdated(
            "{}g", fonts.small, color_golden, 
            player.get_money
        ),
        Allignment.LEFT_WALL,
        nudge=(9, 0)
    )
    # Current health bar
    c_health = Container((397, 71), (176, 36), (3, 5, 10, 5))
    c_health.add_element(
        TextPlain("Lives", fonts.small, color_white),
        Allignment.LEFT_WALL,
        nudge=(9, 0)
    )
    c_health.add_element(
        HealthBar(
            (102, 5), 2, 6,
            player.get_lives,
            player_stats.cheat_godmode
        )
    )
    
    containers.extend(
        [c_weapon, c_score, c_money, c_health, c_timer]
    )

    # Cheats detected
    if player.is_sus:
        c_cheats = Container((game.screen_resolution[0]-399, game.screen_resolution[1]-24), (400, 25), (5, 0, 0, 0))
        c_cheats.add_element(
            TextPlain("Cheats enabled! Score won't be saved.", fonts.very_small, color_white),
            Allignment.CENTER
        )

        containers.append(c_cheats)

    return containers, buttons