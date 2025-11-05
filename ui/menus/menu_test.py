from ui.colors import *
from ui.elements.container import Container, Allignment
from ui.elements.buttons import Button, ButtonRound, Switch, InfoButton, ModKey
from ui.elements.text import TextPlain, TextUpdated
from ui.font_builder import FontBuilder
from ui.menus.enum import Menu
from player.player_stats import PlayerStats
from player.player import Player

def initialize_test_menu(
    game,
    gsm,
    player_stats : PlayerStats,
    player : Player,
    fonts : FontBuilder
):
    """Place stuff here and assign as starting menu to test things without breaking anything else."""

    containers : list[Container] = []
    buttons : list[Button | Switch] = []

    res = game.screen_resolution

    # <> Containers <>

    container = Container((10, 10), (res[0]-20, res[1]-20), (5, 5, 5, 5))

    containers.extend(
        [container]
    )
    
    # <> Buttons <>

    buttons.extend(
        []
    )

    return containers, buttons