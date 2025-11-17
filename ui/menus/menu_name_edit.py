from ui.colors import *
from ui.elements.container import Container, Allignment
from ui.elements.buttons import Button, ButtonRound, Switch, InfoButton, ModKey
from ui.elements.text import TextPlain, TextUpdated
from ui.font_builder import FontBuilder
from ui.menus.enum import Menu
from player.player_stats import PlayerStats
from player.player import Player

def initialize_name_edit(
    game,
    gsm,
    player_stats : PlayerStats,
    player : Player,
    fonts : FontBuilder
) -> tuple[list, list]:

    containers : list[Container] = []
    buttons : list[Button | Switch] = []

    root_x = game.screen_resolution[0]/2-225
    root_y = game.screen_resolution[1]/2-85
    
    # <> Containers <>

    c_background = Container((root_x, root_y), (450, 170), (10, 25, 10, 25))
    c_background.add_element(
        TextPlain("Edit your name:", fonts.medium, color_white),
        nudge=(15, 7)
    )

    c_name = Container((root_x+10, root_y+50), (430, 50), (3, 10, 3, 10))
    c_name.add_element(
        TextUpdated(
            "{}", fonts.medium, color_white, 
            lambda: player_stats.name
            ),
            Allignment.LEFT_WALL,
            nudge=(10, 0)

    )

    containers.extend(
        [c_background, c_name]
    )
    
    # <> Buttons <>

    b_confirm = Button(
        (root_x+125, root_y+110), (200, 50), (3, 10, 3, 10),
        game.finish_getting_player_name,
        lambda: len(player_stats.name) > 0
    )
    b_confirm.add_element(
        TextPlain("Confirm", fonts.medium, color_blue),
        Allignment.CENTER
    )

    buttons.extend(
        [b_confirm]
    )

    return containers, buttons