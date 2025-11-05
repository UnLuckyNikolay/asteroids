from ui.colors import *
from ui.elements.container import Container, Allignment
from ui.elements.buttons import Button, ButtonRound, Switch, InfoButton, ModKey
from ui.elements.text import TextPlain, TextUpdated
from ui.font_builder import FontBuilder
from ui.menus.enum import Menu
from round_state_manager import RoundStateManager
from player.player_stats import PlayerStats
from player.player import Player

def initialize_round_end(
    game,
    gsm,
    rsm : RoundStateManager,
    player_stats : PlayerStats,
    player : Player,
    fonts : FontBuilder
) -> tuple[list, list]:
    
    containers : list[Container] = []
    buttons : list[Button | Switch] = []
    
    res = game.screen_resolution
    size_x = 900
    size_y = 405
    root_x = int(res[0]/2-size_x/2)
    root_y = int(res[1]/2-size_y/2)

    nudge_x_1 = 36
    nudge_x_2 = int(nudge_x_1+size_x/2)

    text_start_y = 50
    text_row_y = 30

    # <> Containers <>

    # Profile
    c_background = Container(
        (root_x, root_y), (size_x, size_y), (30, 30, 30, 30)
    )
    c_title = Container(
        (int(root_x+size_x/2-250), root_y+10), (500, 75), (10, 10, 10, 10)
    )
    c_title.set_outline_color(color_golden)
    c_title.add_element(
        TextPlain(
            rsm.get_round_title(), fonts.big, color_golden
        ),
        Allignment.CENTER
    )
    c_stats = Container(
        (root_x+10, root_y+95), (size_x-20, size_y-165), (10, 10, 10, 10)
    )
    c_stats.add_element(
        TextPlain(
            "Score: {}", fonts.medium, color_white,
            rsm.score
        ),
        nudge=(nudge_x_1, 11)
    )
    c_stats.add_element(
        TextPlain(
            "Time: {}", fonts.medium, color_white,
            rsm.get_time_as_text()
        ),
        nudge=(nudge_x_2, 11)
    )
    c_stats.add_element(
        TextPlain(
            "Asteroids destroyed: {}", fonts.small, color_white,
            rsm.destroyed_asteroids
        ),
        nudge=(nudge_x_1, text_start_y)
    )
    c_stats.add_element(
        TextPlain(
            "- Basic: {}", fonts.small, color_white,
            rsm.destroyed_asteroids_basic
        ),
        nudge=(nudge_x_1, text_start_y+text_row_y*1)
    )
    c_stats.add_element(
        TextPlain(
            "- Bouncy: {}", fonts.small, color_white,
            rsm.destroyed_asteroids_bouncy
        ),
        nudge=(nudge_x_1, text_start_y+text_row_y*2)
    )
    c_stats.add_element(
        TextPlain(
            "- Explosive: {}", fonts.small, color_white,
            rsm.destroyed_asteroids_explosive
        ),
        nudge=(nudge_x_1, text_start_y+text_row_y*3)
    )
    c_stats.add_element(
        TextPlain(
            "- Homing: {}", fonts.small, color_white,
            rsm.destroyed_asteroids_homing
        ),
        nudge=(nudge_x_1, text_start_y+text_row_y*4)
    )
    c_stats.add_element(
        TextPlain(
            "- Golden: {}", fonts.small, color_white,
            rsm.destroyed_asteroids_golden
        ),
        nudge=(nudge_x_1, text_start_y+text_row_y*5)
    )
    c_stats.add_element(
        TextPlain(
            "Loot collected: {}", fonts.small, color_white,
            rsm.collected_loot
        ),
        nudge=(nudge_x_2, text_start_y)
    )
    c_stats.add_element(
        TextPlain(
            "- Copper ore: {}", fonts.small, color_white,
            rsm.collected_ores_copper
        ),
        nudge=(nudge_x_2, text_start_y+text_row_y*1)
    )
    c_stats.add_element(
        TextPlain(
            "- Silver ore: {}", fonts.small, color_white,
            rsm.collected_ores_silver
        ),
        nudge=(nudge_x_2, text_start_y+text_row_y*2)
    )
    c_stats.add_element(
        TextPlain(
            "- Golden ore: {}", fonts.small, color_white,
            rsm.collected_ores_golden
        ),
        nudge=(nudge_x_2, text_start_y+text_row_y*3)
    )
    c_stats.add_element(
        TextPlain(
            "- Diamonds: {}", fonts.small, color_white,
            rsm.collected_diamonds
        ),
        nudge=(nudge_x_2, text_start_y+text_row_y*4)
    )
    # personal_sprite = get_personal_sprite(self.player_stats.name)
    # if personal_sprite != None:
    #     c_round_stats.add_element(
    #         personal_sprite(10, -10),
    #         Allignment.BOTTOM_LEFT_CORNER
    #     )

    containers.extend(
        [c_background, c_stats, c_title]
    )
    
    # <> Buttons <>

    b_confirm = Button(
        (int(root_x+size_x/2-100), root_y+size_y-60), (200, 50), (3, 10, 3, 10),
        game.finish_round
    )
    b_confirm.add_element(
        TextPlain("Confirm", fonts.medium, color_blue),
        Allignment.CENTER
    )

    buttons.extend(
        [b_confirm]
    )

    return containers, buttons