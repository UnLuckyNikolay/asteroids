from ui.colors import *
from ui.elements.container import Container, Allignment
from ui.elements.buttons import Button, ButtonRound, Switch, InfoButton, ModKey
from ui.elements.text import TextPlain, TextUpdated
from ui.font_builder import FontBuilder
from ui.menus.enum import Menu
from player.player_stats import PlayerStats
from player.player import Player, ShipModel
from ui.elements.sprites.leaderboard import Leaderboard

def initialize_leaderboard(
    game,
    gsm,
    player_stats : PlayerStats,
    player : Player,
    fonts : FontBuilder
) -> tuple[list, list]:

    containers : list[Container | Leaderboard] = []
    buttons : list[Button | Switch] = []

    res = game.screen_resolution
    
    # <> Containers <>

    # Name of the menu
    c_menu_name = Container((res[0] / 2 - 185, 35), (370, 72), (8, 8, 20, 20))
    c_menu_name.add_element(
        TextPlain("Leaderboard", fonts.big, color_white),
        Allignment.CENTER
    )
    # List of high __scores
    c_leaderboard = Leaderboard(int(res[0]/2)-540, 145, 
        fonts.medium, gsm._scores
    )
    
    containers.extend(
        [c_menu_name, c_leaderboard]
    )
    
    # <> Buttons <>

    # Returns to the Main Menu
    b_back = Button(
        (100, 68), (100, 36), (15, 3, 3, 15), 
        lambda: gsm.switch_menu(Menu.MAIN_MENU)
    )
    b_back.add_element(
        TextPlain("Back", fonts.small, color_blue),
        Allignment.CENTER
    )
    
    buttons.extend(
        [b_back]
    )
    # Reset the leaderboard
    b_reset = Button(
        (res[0]-200, 68), (100, 36), (3, 6, 3, 6), 
        gsm._reset_leaderboard
    )
    b_reset.set_fill_color(color_red_fill)
    b_reset.make_weighted(ModKey.SHIFT)
    b_reset.set_outline_color(color_red)
    b_reset.add_description(
        TextPlain("SHIFT+Click to RESET the leaderboard", fonts.very_small, color_white)
    )
    b_reset.add_element(
        TextPlain("Reset", fonts.small, color_red),
        Allignment.CENTER
    )
    
    buttons.extend(
        [b_back, b_reset]
    )

    # UFO secret
    if not player_stats.check_unlocked_ship(ShipModel.UFO2):
        b_ufo = ButtonRound(
            (res[0]-30, res[1]-20), 6,
            lambda: gsm.unlock_ship(ShipModel.UFO2)
        )
        b_ufo.set_outline_color(color_gray)
        b_ufo.set_fill_color(color_green)
        b_ufo.set_hover_fill_color(color_green)
        b_ufo.add_description(
            TextPlain("Do you want to believe?", fonts.very_small, color_green)
        )
        
        buttons.append(b_ufo)

    return containers, buttons