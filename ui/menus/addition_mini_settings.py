from ui.colors import *
from constants import DEBUG
from ui.elements.container import Container, Allignment
from ui.elements.buttons import Button, ButtonRound, Switch, InfoButton, ModKey
from ui.elements.text import TextPlain, TextUpdated
from ui.font_builder import FontBuilder
from ui.menus.enum import Menu
from player.player_stats import PlayerStats
from player.player import Player

def add_mini_settings_and_cheats(
        container_list : list, 
        button_list : list,
        game,
        gsm,
        player_stats : PlayerStats,
        player : Player,
        fonts : FontBuilder
    ):
    """Adds some options and cheats (if found at the buttom part of the screen)."""

    res = game.screen_resolution
    offset_y = 30
    container_size = (95, 20)
    button_size = (120, 20)
    button_corners = (6, 6, 6, 6)
    left_corners = (8, 2, 8, 2)
    right_corners = (2, 8, 2, 8)
    
    # <> Containers <>        

    if DEBUG:
        # Debug
        c_debug = Container((10, res[1]-offset_y*6), container_size, left_corners)
        c_debug.add_element(
            TextPlain("Debug", fonts.very_small, color_white),
            Allignment.LEFT_WALL,
            nudge=(5, 0)
        )

        container_list.append(c_debug)

    # Settings
    c_settings = Container((10, res[1]-offset_y*3), container_size, left_corners)
    c_settings.add_element(
        TextPlain("Settings", fonts.very_small, color_white),
        Allignment.LEFT_WALL,
        nudge=(5, 0)
    )

    container_list.extend(
        [c_settings]
    )

    if player_stats.found_cheats:
        # Cheats
        c_cheats = Container((res[0]-10-container_size[0], res[1]-offset_y*4), container_size, right_corners)
        c_cheats.add_element(
            TextPlain("Cheats", fonts.very_small, color_white),
            Allignment.RIGHT_WALL,
            nudge=(-5, 0)
        )
        
        container_list.extend(
            [c_cheats]
        )
    
    # <> Buttons <>
    

    if DEBUG:
        # Low FPS
        s_slow = Switch(
            (10, res[1]-offset_y*5), button_size, left_corners,
            game.switch_low_fps,
            game.is_slow
        )
        s_slow.add_description(
            TextPlain("DEBUG: Switches max FPS between 75 and 10", fonts.very_small, color_white)
        )
        s_slow.add_element(
            TextPlain("Low FPS", fonts.very_small, color_blue),
            Allignment.LEFT_WALL,
            nudge=(5, 0)
        )
        # Show hitbox
        s_hitbox = Switch(
            (10, res[1]-offset_y*4), button_size, left_corners,
            player.switch_hitbox,
            player.is_hitbox_shown
        )
        s_hitbox.add_description(
            TextPlain("DEBUG: Switches the player hitbox visibility on/off", fonts.very_small, color_white)
        )
        s_hitbox.add_element(
            TextPlain("Hitbox", fonts.very_small, color_blue),
            Allignment.LEFT_WALL,
            nudge=(5, 0)
        )

        button_list.extend([s_slow, s_hitbox])

    # Switch Fullscreen
    s_fullscreen = Switch(
        (10, res[1]-offset_y*2), button_size, left_corners,
        game.switch_fullscreen,
        game.is_fullscreen
    )
    s_fullscreen.add_description(
        TextPlain("Switches the FULLSCREEN mode on/off", fonts.very_small, color_white)
    )
    s_fullscreen.add_element(
        TextPlain("Fullscreen", fonts.very_small, color_blue),
        Allignment.LEFT_WALL,
        nudge=(5, 0)
    )
    # Regenerate background
    b_background = Button(
        (10, res[1]-offset_y*1), button_size, left_corners,
        game.handler_regenerate_background
    )
    b_background.add_description(
        TextPlain("Generates new background", fonts.very_small, color_white)
    )
    b_background.add_element(
        TextPlain("New BG", fonts.very_small, color_blue),
        Allignment.LEFT_WALL,
        nudge=(5, 0)
    )

    button_list.extend(
        [b_background, s_fullscreen]
    )

    if player_stats.found_cheats:
        # Cheat - Godmode
        s_godmode = Switch(
            (res[0]-10-button_size[0], res[1]-offset_y*3), button_size, right_corners,
            player_stats.switch_godmode,
            player_stats.cheat_godmode
        )
        s_godmode.add_description(
            TextPlain("Say `No!` to all damage!", fonts.very_small, color_white)
        )
        s_godmode.set_active_outline_color(color_golden)
        s_godmode.add_element(
            TextPlain("Godmode", fonts.very_small, color_blue),
            Allignment.RIGHT_WALL,
            nudge=(-5, 0)
        )
        # Cheat - Money cheat
        s_money = Switch(
            (res[0]-10-button_size[0], res[1]-offset_y*2), button_size, right_corners,
            player_stats.switch_stonks,
            player_stats.cheat_stonks
        )
        s_money.add_description(
            TextPlain("Sells your Bitcoin before starting a round", fonts.very_small, color_white)
        )
        s_money.set_active_outline_color(color_golden)
        s_money.add_element(
            TextPlain("Stonks", fonts.very_small, color_blue),
            Allignment.RIGHT_WALL,
            nudge=(-5, 0)
        )
        # Cheat - Cleavers
        s_cleavers = Switch(
            (res[0]-10-button_size[0], res[1]-offset_y*1), button_size, right_corners,
            player_stats.switch_cleavers,
            player_stats.cheat_cleavers
        )
        s_cleavers.add_description(
            TextPlain("Meat", fonts.very_small, color_red)
        )
        s_cleavers.set_active_outline_color(color_red)
        s_cleavers.add_element(
            TextPlain("Cleavers", fonts.very_small, color_blue),
            Allignment.RIGHT_WALL,
            nudge=(-5, 0)
        )
            
        button_list.extend(
            [s_money, s_godmode, s_cleavers]
        )