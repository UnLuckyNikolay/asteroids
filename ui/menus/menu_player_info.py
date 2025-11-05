from ui.colors import *
from ui.elements.container import Container, Allignment
from ui.elements.buttons import ButtonBase, Button, ButtonRound, Switch, InfoButton, ModKey
from ui.elements.text import TextPlain, TextUpdated
from ui.font_builder import FontBuilder
from ui.menus.enum import Menu
from player.player_stats import PlayerStats
from player.player import Player, ShipModel
from player.ship import Ship
from ui.elements.simple_sprites.symbols import *
from ui.elements.personal_sprites.getter import get_personal_sprite

def initialize_player_info(
    game,
    gsm,
    player_stats : PlayerStats,
    player : Player,
    fonts : FontBuilder
) -> tuple[list, list]:

    containers : list[Container] = []
    buttons : list[ButtonBase] = []
    
    res = game.screen_resolution
    center_x = int(res[0]/2)
    size_x = 950
    size_y = 550
    root_x = int(center_x-size_x/2)
    root_y = 10

    text_start_y = 10
    text_row_y = 30
    text_nudge_x = 15

    root_stats_x = root_x + 20
    root_stats_y = root_y + 125

    root_secrets_x = int(root_x+size_x*0.75-120)
    root_secrets_y = 150

    # <> Containers <>

    # Profile
    c_profile = Container(
        (root_x, root_y), (size_x, size_y), (7, 7, 30, 30)
    )
    c_profile.add_element(
        Ship(player_stats.ship_model_value, color_profile=player_stats.ship_color_profile),
        Allignment.UPPER_RIGHT_CORNER, 
        nudge=(-70, 70)
    )
    c_profile.add_element( # (35, 18)
        TextPlain(
            "{}", fonts.big, color_white,
            player_stats.name
        ),
        nudge=(81, 18)
    )
    c_profile.add_element(
        TextPlain(
            "Max Score: {}", fonts.medium, color_white,
            player_stats.max_score
        ),
        nudge=(35, 77)
    )
    c_stats = Container(
        (root_stats_x, root_stats_y), 
        (int(size_x/2-30), size_y-root_secrets_y-20), 
        (5, 5, 5, 5)
    )
    c_stats.add_element(
        TextPlain(
            "Longest run: {}", fonts.small, color_white,
            player_stats.get_longest_time_as_text()
        ),
        nudge=(text_nudge_x, text_start_y)
    )
    c_stats.add_element(
        TextPlain(
            "Asteroids destroyed: {}", fonts.small, color_white,
            player_stats.destroyed_asteroids
        ),
        nudge=(text_nudge_x, text_start_y+text_row_y*1)
    )
    c_stats.add_element(
        TextPlain(
            "- Basic: {}", fonts.small, color_white,
            player_stats.destroyed_asteroids_basic
        ),
        nudge=(text_nudge_x, text_start_y+text_row_y*2)
    )
    c_stats.add_element(
        TextPlain(
            "- Bouncy: {}", fonts.small, color_white,
            player_stats.destroyed_asteroids_bouncy
        ),
        nudge=(text_nudge_x, text_start_y+text_row_y*3)
    )
    c_stats.add_element(
        TextPlain(
            "- Explosive: {}", fonts.small, color_white,
            player_stats.destroyed_asteroids_explosive
        ),
        nudge=(text_nudge_x, text_start_y+text_row_y*4)
    )
    c_stats.add_element(
        TextPlain(
            "- Homing: {}", fonts.small, color_white,
            player_stats.destroyed_asteroids_homing
        ),
        nudge=(text_nudge_x, text_start_y+text_row_y*5)
    )
    c_stats.add_element(
        TextPlain(
            "- Golden: {}", fonts.small, color_white,
            player_stats.destroyed_asteroids_golden
        ),
        nudge=(text_nudge_x, text_start_y+text_row_y*6)
    )
    c_stats.add_element(
        TextPlain(
            "Loot collected: {}", fonts.small, color_white,
            player_stats.collected_loot
        ),
        nudge=(text_nudge_x, text_start_y+text_row_y*7)
    )
    c_stats.add_element(
        TextPlain(
            "- Copper ore: {}", fonts.small, color_white,
            player_stats.collected_ores_copper
        ),
        nudge=(text_nudge_x, text_start_y+text_row_y*8)
    )
    c_stats.add_element(
        TextPlain(
            "- Silver ore: {}", fonts.small, color_white,
            player_stats.collected_ores_silver
        ),
        nudge=(text_nudge_x, text_start_y+text_row_y*9)
    )
    c_stats.add_element(
        TextPlain(
            "- Golden ore: {}", fonts.small, color_white,
            player_stats.collected_ores_golden
        ),
        nudge=(text_nudge_x, text_start_y+text_row_y*10)
    )
    c_stats.add_element(
        TextPlain(
            "- Diamonds: {}", fonts.small, color_white,
            player_stats.collected_diamonds
        ),
        nudge=(text_nudge_x, text_start_y+text_row_y*11)
    )
    personal_sprite = get_personal_sprite(player_stats.name)
    if personal_sprite != None:
        c_profile.add_element(
            personal_sprite(10, -10),
            Allignment.BOTTOM_LEFT_CORNER
        )
    c_secrets_bg = Container(
        (int(root_x+size_x/2)+10, root_stats_y), 
        (int(size_x/2-30), size_y-root_secrets_y-20), 
        (5, 5, 5, 5)
    )
    c_secrets = Container((root_secrets_x, root_secrets_y), (240, 30), (5, 5, 5, 5))
    c_secrets.add_element(
        TextPlain("Secrets", fonts.small, color_white),
        Allignment.CENTER
    )

    containers.extend(
        [c_profile, c_stats, c_secrets_bg, c_secrets]
    )
    
    # <> Buttons <>

    # Close
    b_close_info = Button(
        (center_x-50, size_y-15), (100, 20), (3, 3, 3, 3),
        lambda: gsm.switch_menu(Menu.MAIN_MENU)
    )
    b_close_info.add_element(
        SymbolArrowUp(0, 0, color_blue),
        Allignment.CENTER
    )
    # Rename
    b_rename = Button(
        (root_x+35, root_y+26), (35, 35), (3, 3, 3, 3),
        lambda: gsm._rename_player(Menu.PLAYER_INFO)
    )
    b_rename.add_element(
        SymbolPencil(0, 0, color_blue),
        Allignment.CENTER
    )
    # Secret - Cheats
    ib_cheats = InfoButton(
        (root_secrets_x, root_secrets_y+50), (240, 30), (5, 5, 5, 5),
        player_stats.found_cheats
    )
    ib_cheats.add_element(
        TextPlain("Cheats", fonts.small, color_white),
        Allignment.CENTER
    )
    ib_cheats.add_description(
        TextPlain("There is a famous sequence that needs to be inputed while in the main menu.", fonts.very_small, color_white)
    )
    # Secret - UFO
    ib_ufo = InfoButton(
        (root_secrets_x, root_secrets_y+100), (240, 30), (5, 5, 5, 5),
        lambda: player_stats.check_unlocked_ship(ShipModel.UFO2)
    )
    ib_ufo.add_element(
        TextPlain("Suspicious ship", fonts.small, color_white),
        Allignment.CENTER
    )
    ib_ufo.add_description(
        TextPlain("There were reports of a stange ship that can be barely seen from a certain menu.", fonts.very_small, color_white)
    )

    buttons.extend(
        [b_close_info, b_rename, ib_cheats, ib_ufo]
    )

    return containers, buttons