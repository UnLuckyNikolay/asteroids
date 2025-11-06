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

def initialize_profile_selection(
    game,
    gsm,
    player_stats : PlayerStats,
    player : Player,
    fonts : FontBuilder
) -> tuple[list, list]:

    containers : list[Container] = []
    buttons : list[Button | Switch] = []
    
    res = game.screen_resolution
    offset_x = res[0]/2-400
    offset_y = res[1]/2-285

    # 30 between elements

    # <> Containers <>

    c_menu_name = Container((offset_x+75, offset_y), (650, 60), (20, 20, 8, 8))
    c_menu_name.add_element(
        TextPlain("Select the Profile", fonts.big, color_white),
        Allignment.CENTER
    )

    containers.extend(
        [c_menu_name]
    )
    
    # <> Buttons <>

    b_corners = (7, 30, 7, 30)
    # Profile 0
    if gsm._profiles[0] != None:
        b_pf0 = Button(
            (offset_x, offset_y+90+170*0), (800, 140), b_corners,
            lambda: gsm._load_profile(0)
        )
        b_pf0.add_element(
            TextPlain(
                "{}", fonts.big, color_blue,
                gsm._profiles[0]["player_stats_save"].get("name", gsm._default_player_name)
            ),
            nudge=(35, 18)
        )
        b_pf0.add_element(
            TextPlain(
                "Max Score: {}", fonts.medium, color_white,
                gsm._profiles[0]["player_stats_save"].get("max_score", 0)
            ),
            nudge=(35, 77),
            color_override_and_lock=color_white
        )
        b_pf0.add_element(
            Ship(
                gsm._profiles[0]["player_stats_save"].get("ship_model_value", gsm._default_ship_model),
                color_profile=gsm._profiles[0]["player_stats_save"].get("ship_color_profile", 0)
            ),
            Allignment.UPPER_RIGHT_CORNER,
            nudge=(-70, 70)
        )
        personal_sprite = get_personal_sprite(gsm._profiles[0]["player_stats_save"].get("name", gsm._default_player_name))
        if personal_sprite != None:
            b_pf0.add_element(
                personal_sprite(10, -10),
                Allignment.BOTTOM_LEFT_CORNER
            )
            
        b_pf0_delete = Button(
            (offset_x+830, offset_y+140+170*0), (40, 40), (8, 8, 8, 8),
            lambda: gsm._delete_profile(0)
        )
        b_pf0_delete.make_weighted(ModKey.SHIFT)
        b_pf0_delete.set_outline_color(color_red)
        b_pf0_delete.set_fill_color(color_red_fill)
        b_pf0_delete.add_description(
            TextPlain("SHIFT+Click to DELETE the Profile", fonts.very_small, color_white)
        )
        b_pf0_delete.add_element(
            SymbolCross(0, 0, color_red), 
            Allignment.CENTER
        )

        buttons.extend(
            [b_pf0_delete]
        )
        
    else: # Empty profile
        b_pf0 = Button(
            (offset_x, offset_y+90+170*0), (800, 140), b_corners,
            lambda: gsm._new_profile(0)
        )
        b_pf0.add_element(
            TextPlain("Null", fonts.big, color_blue),
            nudge=(35, 18)
        )

    # Profile 1
    if gsm._profiles[1] != None:
        b_pf1 = Button(
            (offset_x, offset_y+90+170*1), (800, 140), b_corners,
            lambda: gsm._load_profile(1)
        )
        b_pf1.add_element(
            TextPlain(
                "{}", fonts.big, color_blue,
                gsm._profiles[1]["player_stats_save"].get("name", gsm._default_player_name)
            ),
            nudge=(35, 18)
        )
        b_pf1.add_element(
            TextPlain(
                "Max Score: {}", fonts.medium, color_white,
                gsm._profiles[1]["player_stats_save"].get("max_score", 0)
            ),
            nudge=(35, 77),
            color_override_and_lock=color_white
        )
        b_pf1.add_element(
            Ship(
                gsm._profiles[1]["player_stats_save"].get("ship_model_value", gsm._default_ship_model),
                color_profile=gsm._profiles[1]["player_stats_save"].get("ship_color_profile", 0)
            ),
            Allignment.UPPER_RIGHT_CORNER,
            nudge=(-70, 70)
        )
        personal_sprite = get_personal_sprite(gsm._profiles[1]["player_stats_save"].get("name", gsm._default_player_name))
        if personal_sprite != None:
            b_pf1.add_element(
                personal_sprite(10, -10),
                Allignment.BOTTOM_LEFT_CORNER
            )

        b_pf1_delete = Button(
            (offset_x+830, offset_y+140+170*1), (40, 40), (8, 8, 8, 8),
            lambda: gsm._delete_profile(1)
        )
        b_pf1_delete.make_weighted(ModKey.SHIFT)
        b_pf1_delete.set_outline_color(color_red)
        b_pf1_delete.set_fill_color(color_red_fill)
        b_pf1_delete.add_description(
            TextPlain("SHIFT+Click to DELETE the Profile", fonts.very_small, color_white)
        )
        b_pf1_delete.add_element(
            SymbolCross(0, 0, color_red), 
            Allignment.CENTER
        )

        buttons.extend(
            [b_pf1_delete]
        )

    else: # Empty profile
        b_pf1 = Button(
            (offset_x, offset_y+90+170*1), (800, 140), b_corners,
            lambda: gsm._new_profile(1)
        )
        b_pf1.add_element(
            TextPlain("Null", fonts.big, color_blue),
            nudge=(35, 18)
        )

    # Profile 2
    if gsm._profiles[2] != None:
        b_pf2 = Button(
            (offset_x, offset_y+90+170*2), (800, 140), b_corners,
            lambda: gsm._load_profile(2)
        )
        b_pf2.add_element(
            TextPlain(
                "{}", fonts.big, color_blue,
                gsm._profiles[2]["player_stats_save"].get("name", gsm._default_player_name)
            ),
            nudge=(35, 18)
        )
        b_pf2.add_element(
            TextPlain(
                "Max Score: {}", fonts.medium, color_white,
                gsm._profiles[2]["player_stats_save"].get("max_score", 0)
            ),
            nudge=(35, 77),
            color_override_and_lock=color_white
        )
        b_pf2.add_element(
            Ship(
                gsm._profiles[2]["player_stats_save"].get("ship_model_value", gsm._default_ship_model),
                color_profile=gsm._profiles[2]["player_stats_save"].get("ship_color_profile", 0)
            ),
            Allignment.UPPER_RIGHT_CORNER,
            nudge=(-70, 70)
        )
        personal_sprite = get_personal_sprite(gsm._profiles[2]["player_stats_save"].get("name", gsm._default_player_name))
        if personal_sprite != None:
            b_pf2.add_element(
                personal_sprite(10, -10),
                Allignment.BOTTOM_LEFT_CORNER
            )

        b_pf2_delete = Button(
            (offset_x+830, offset_y+140+170*2), (40, 40), (8, 8, 8, 8),
            lambda: gsm._delete_profile(2)
        )
        b_pf2_delete.make_weighted(ModKey.SHIFT)
        b_pf2_delete.set_outline_color(color_red)
        b_pf2_delete.set_fill_color(color_red_fill)
        b_pf2_delete.add_description(
            TextPlain("SHIFT+Click to DELETE the Profile", fonts.very_small, color_white)
        )
        b_pf2_delete.add_element(
            SymbolCross(0, 0, color_red), 
            Allignment.CENTER
        )

        buttons.extend(
            [b_pf2_delete]
        )
        
    else: # Empty profile
        b_pf2 = Button(
            (offset_x, offset_y+90+170*2), (800, 140), b_corners,
            lambda: gsm._new_profile(2)
        )
        b_pf2.add_element(
            TextPlain("Null", fonts.big, color_blue),
            nudge=(35, 18)
        )

    buttons.extend(
        [b_pf0, b_pf1, b_pf2]
    )

    return containers, buttons