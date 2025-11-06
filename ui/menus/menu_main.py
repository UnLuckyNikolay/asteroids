from ui.colors import *
from ui.elements.container import Container, Allignment
from ui.elements.buttons import Button, ButtonRound, Switch, InfoButton, ModKey
from ui.elements.text import TextPlain, TextUpdated
from ui.font_builder import FontBuilder
from ui.menus.enum import Menu
from player.player_stats import PlayerStats
from player.player import Player
from player.ship_enums import ShipModel
from player.ship import Ship
from ui.elements.simple_sprites.symbols import *
from ui.elements.personal_sprites.getter import get_personal_sprite

def initialize_main_menu(
    game,
    gsm,
    player_stats : PlayerStats,
    player : Player,
    fonts : FontBuilder
) -> tuple[list, list]:

    containers : list[Container] = []
    buttons : list[Button | Switch] = []

    gsm._konami_progress = 0 # Resets Konami sequence

    res = game.screen_resolution
    center_x = int((res[0])/2)
    center_y = int((res[1])/2)

    root_x = center_x-475
    root_y = 10
    text_nudge_x = 35
    
    # <> Containers <>
    
    # Profile
    c_profile = Container(
        (root_x, 10), (950, 140), (7, 7, 30, 30)
    )
    c_profile.add_element(
        TextPlain(
            "{}", fonts.big, color_white,
            player_stats.name
        ),
        nudge=(text_nudge_x+46, 18)
    )
    c_profile.add_element(
        TextPlain(
            "Max Score: {}", fonts.medium, color_white,
            player_stats.max_score
        ),
        nudge=(text_nudge_x, 77)
    )
    c_profile.add_element(
        Ship(player_stats.ship_model_value, color_profile=player_stats.ship_color_profile),
        Allignment.UPPER_RIGHT_CORNER,
        nudge=(-70, 70)
    )
    personal_sprite = get_personal_sprite(player_stats.name)
    if personal_sprite != None:
        c_profile.add_element(
            personal_sprite(10, -10),
            Allignment.BOTTOM_LEFT_CORNER
        )
    
    containers.extend(
        [c_profile]
    )
    
    # <> Buttons <>

    # Profile
    # Rename
    b_rename = Button(
        (root_x+text_nudge_x, root_y+26), (35, 35), (3, 3, 3, 3),
        lambda: gsm._rename_player(Menu.MAIN_MENU)
    )
    b_rename.add_element(
        SymbolPencil(0, 0, color_blue),
        Allignment.CENTER
    )
    # Open
    b_open_info = Button(
        (center_x-50, 125), (100, 20), (3, 3, 3, 3),
        lambda: gsm.switch_menu(Menu.PLAYER_INFO)
    )
    b_open_info.add_element(
        SymbolArrowDown(0, 0, color_blue),
        Allignment.CENTER
    )

    # Main buttons
    # Space between - 28

    amount_of_buttons = 4
    b_offset_y = (res[1] - (amount_of_buttons*100+28))/2 + 75

    # Start button, starts a Round
    b_start = Button(
        (center_x-185, b_offset_y+100*0), (370, 72), (8, 8, 20, 20), 
        game.game_loop
    )
    b_start.add_element(
        TextPlain("Start", fonts.big, color_blue),
        Allignment.CENTER
    )
    # Opens the Leaderboard
    b_leaderboard = Button(
        (center_x-185, b_offset_y+100*1), (370, 72), (8, 8, 20, 20), 
        lambda: gsm.switch_menu(Menu.LEADERBOARD)
    )
    b_leaderboard.add_element(
        TextPlain("Leaderboard", fonts.big, color_blue),
        Allignment.CENTER
    )
    # Back to profile selection
    b_profiles = Button(
        (center_x-185, b_offset_y+100*2), (370, 72), (8, 8, 20, 20), 
        gsm._return_to_profile_selection
    )
    b_profiles.add_element(
        TextPlain("Profiles", fonts.big, color_blue),
        Allignment.CENTER
    )
    # Exits the game
    b_exit = Button(
        (center_x-185, b_offset_y+100*3), (370, 72), (8, 8, 20, 20), 
        game.handler_turn_off
    )
    b_exit.add_element(
        TextPlain("Exit", fonts.big, color_blue),
        Allignment.CENTER
    )
    
    buttons.extend(
        [b_start, b_leaderboard, b_exit, b_profiles, b_open_info,
            b_rename]
    )

    return containers, buttons