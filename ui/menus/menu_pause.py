from ui.colors import *
from ui.elements.container import Container, Allignment
from ui.elements.buttons import Button, ButtonRound, Switch, InfoButton, ModKey
from ui.elements.text import TextPlain, TextUpdated
from ui.font_builder import FontBuilder
from ui.menus.enum import Menu
from round_state_manager import RoundStateManager
from player.player_stats import PlayerStats
from player.player import Player, ShipUpgrade, ShipPart
from ui.elements.sprites.healthbar import HealthBar

def initialize_pause_menu(
    game,
    gsm,
    rsm : RoundStateManager,
    player_stats : PlayerStats,
    player : Player,
    fonts : FontBuilder
) -> tuple[list, list]:
    
    containers : list[Container] = []
    buttons : list[Button | Switch] = []

    # Space between elements - 15
    offset_x = int((game.screen_resolution[0] - 1280)/2)
    offset_y = int((game.screen_resolution[1] - 720)/2)
    row_height = 51
    column_1 = 290
    column_2 = 760
    
    # <> Containers <>

    # Background
    c_background = Container((offset_x+50, offset_y+50), (1180, 540), (20, 20, 8, 15))
    c_background.set_fill_color((75, 75, 100, 150))
            
    # Current ship
    c_ship = Container((offset_x+65, offset_y+65), (210, 189), (12, 6, 6, 6))
    c_ship.add_element(
        player.get_ship, 
        Allignment.CENTER
    )
    c_colors = Container((offset_x+65, offset_y+269), (210, 36), (6, 6, 6, 6))
    c_colors.add_element(
        TextPlain("Colors", fonts.small, color_white),
        Allignment.CENTER
    )

    # List - ship
    c_model = Container((offset_x+column_1, offset_y+65), (455, 36), (6, 6, 6, 6))
    c_model.add_element(
        TextUpdated(
            "Model: {}", fonts.small, color_white,
            player.ship.get_name
        ),
        Allignment.LEFT_WALL,
        nudge=(12, 0)
    )
    
    c_switch_model = Container((offset_x+column_1+46, offset_y+65+row_height*1), (363, 36), (3, 3, 3, 3))
    c_switch_model.add_element(
        TextPlain("Switch model", fonts.small, color_white),
        Allignment.LEFT_WALL,
        nudge=(12, 0)
    )
    
    c_engine = Container((offset_x+column_1, offset_y+65+row_height*2), (455, 36), (6, 6, 6, 6))
    c_engine.add_element(
        TextUpdated(
            "Engine.v{}", fonts.small, color_white,
            lambda: player.get_part_level(ShipPart.ENGINE)
        ),
        Allignment.LEFT_WALL,
        nudge=(12, 0)
    )
    
    c_engine_speed = Container((offset_x+column_1, offset_y+65+row_height*3), (409, 36), (6, 3, 3, 6))
    c_engine_speed.add_element(
        TextUpdated(
            "Speed: {}", fonts.small, color_white,
            lambda: player.get_upgrade_price_as_text(ShipUpgrade.ENGINE_SPEED)
        ),
        Allignment.LEFT_WALL,
        nudge=(12, 0)
    )
    
    c_engine_acc = Container((offset_x+column_1, offset_y+65+row_height*4), (409, 36), (6, 3, 3, 6))
    c_engine_acc.add_element(
        TextUpdated(
            "Acceleration: {}", fonts.small, color_white,
            lambda: player.get_upgrade_price_as_text(ShipUpgrade.ENGINE_ACCELERATION)
        ),
        Allignment.LEFT_WALL,
        nudge=(12, 0)
    )
    
    c_magnet = Container((offset_x+column_1, offset_y+65+row_height*5), (455, 36), (6, 6, 6, 6))
    c_magnet.add_element(
        TextUpdated(
            "Magnet.v{}", fonts.small, color_white,
            lambda: player.get_part_level(ShipPart.MAGNET)
        ),
        Allignment.LEFT_WALL,
        nudge=(12, 0)
    )
    
    c_magnet_rad = Container((offset_x+column_1, offset_y+65+row_height*6), (409, 36), (6, 3, 3, 6))
    c_magnet_rad.add_element(
        TextUpdated(
            "Radius: {}", fonts.small, color_white,
            lambda: player.get_upgrade_price_as_text(ShipUpgrade.MAGNET_RADIUS)
        ),
        Allignment.LEFT_WALL,
        nudge=(12, 0)
    )
    
    c_magnet_str = Container((offset_x+column_1, offset_y+65+row_height*7), (409, 36), (6, 3, 3, 6))
    c_magnet_str.add_element(
        TextUpdated(
            "Strength: {}", fonts.small, color_white,
            lambda: player.get_upgrade_price_as_text(ShipUpgrade.MAGNET_STRENGTH)
        ),
        Allignment.LEFT_WALL,
        nudge=(12, 0)
    )

    # Current stats
    # Score
    c_points = Container((offset_x+column_2, offset_y+65), (150, 36), (6, 3, 3, 6))
    c_points.add_element(
        TextUpdated(
            "{}pts", fonts.small, color_white, 
            lambda: rsm.score
        ),
        Allignment.LEFT_WALL,
        nudge=(9, 0)
    )
    # Money
    c_money = Container((offset_x+column_2+160, offset_y+65), (127, 36), (3, 3, 3, 3))
    c_money.add_element(
        TextUpdated(
            "{}g", fonts.small, color_golden, 
            player.get_money
        ),
        Allignment.LEFT_WALL,
        nudge=(9, 0)
    )
    # Health
    c_health = Container((offset_x+column_2+297, offset_y+65), (158, 36), (3, 6, 6, 3))
    c_health.add_element(
        TextPlain("Lives", fonts.small, color_white),
        Allignment.LEFT_WALL,
        nudge=(9, 0)
    )
    c_health.add_element(
        HealthBar(
            (84, 5), 2, 2,
            player.get_lives,
            player_stats.cheat_godmode
        )
    )
    # Heal
    c_heal = Container((offset_x+column_2, offset_y+65+row_height*1), (409, 36), (6, 3, 3, 6))
    c_heal.add_element(
        TextUpdated(
            "Heal: {}g", fonts.small, color_white,
            player.get_price_heal
        ),
        Allignment.LEFT_WALL,
        nudge=(12, 0)
    )
    # List - weapons
    # Plasma Gun
    c_weapon_1 = Container((offset_x+column_2, offset_y+65+row_height*2), (455, 36), (6, 6, 6, 6))
    c_weapon_1.add_element(
        TextUpdated(
            "Weapon 1: {}.v{}", fonts.small, color_white,
            player.weapon_plasmagun.get_name,
            lambda: player.get_part_level(ShipPart.PLASMAGUN)
        ),
        Allignment.LEFT_WALL,
        nudge=(12, 0)
    )
    c_weapon_1_proj = Container((offset_x+column_2, offset_y+65+row_height*3), (409, 36), (6, 3, 3, 6))
    c_weapon_1_proj.add_element(
        TextUpdated(
            "Projectiles: {}", fonts.small, color_white,
            lambda: player.get_upgrade_price_as_text(ShipUpgrade.PLASMAGUN_PROJECTILES)
        ),
        Allignment.LEFT_WALL,
        nudge=(12, 0)
    )
    c_weapon_1_cd = Container((offset_x+column_2, offset_y+65+row_height*4), (409, 36), (6, 3, 3, 6))
    c_weapon_1_cd.add_element(
        TextUpdated(
            "Cooldown: {}", fonts.small, color_white,
            lambda: player.get_upgrade_price_as_text(ShipUpgrade.PLASMAGUN_COOLDOWN)
        ),
        Allignment.LEFT_WALL,
        nudge=(12, 0)
    )
    #Bomb Launcher
    c_weapon_2 = Container((offset_x+column_2, offset_y+65+row_height*5), (455, 36), (6, 6, 6, 6))
    c_weapon_2.add_element(
        TextUpdated(
            "Weapon 2: {}.v{}", fonts.small, color_white,
            player.weapon_bomblauncher.get_name,
            lambda: player.get_part_level(ShipPart.BOMBLAUNCHER)
        ),
        Allignment.LEFT_WALL,
        nudge=(12, 0)
    )
    c_weapon_2_rad = Container((offset_x+column_2, offset_y+65+row_height*6), (409, 36), (6, 3, 3, 6))
    c_weapon_2_rad.add_element(
        TextUpdated(
            "Radius: {}", fonts.small, color_white,
            lambda: player.get_upgrade_price_as_text(ShipUpgrade.BOMBLAUNCHER_RADIUS)
        ),
        Allignment.LEFT_WALL,
        nudge=(12, 0)
    )
    c_weapon_2_fuse = Container((offset_x+column_2, offset_y+65+row_height*7), (409, 36), (6, 3, 3, 6))
    c_weapon_2_fuse.add_element(
        TextUpdated(
            "Fuse: {}", fonts.small, color_white,
            lambda: player.get_upgrade_price_as_text(ShipUpgrade.BOMBLAUNCHER_FUSE)
        ),
        Allignment.LEFT_WALL,
        nudge=(12, 0)
    )

    containers.extend(
        [c_background, c_ship, c_model, c_switch_model, c_heal,
            c_magnet, c_magnet_rad, c_magnet_str, c_points, c_money,
            c_health, c_weapon_1, c_weapon_1_proj, c_weapon_2, c_weapon_2_rad,
            c_weapon_2_fuse, c_weapon_1_cd, c_engine, c_engine_acc, c_engine_speed,
            c_colors]
    )
    
    # <> Buttons <>

    # Color profiles # 30 for in between, 45 for button
    b_color1 = Switch(
        (offset_x+65, offset_y+320), (45, 36), (6, 3, 3, 6),
        lambda: player.switch_color_profile(0),
        lambda: player.ship.color_profile == 0
    )
    b_color1.add_element(
        TextPlain("1", fonts.small, color_blue),
        Allignment.CENTER
    )
    b_color2 = Switch(
        (offset_x+120, offset_y+320), (45, 36), (3, 3, 3, 3),
        lambda: player.switch_color_profile(1),
        lambda: player.ship.color_profile == 1
    )
    b_color2.add_element(
        TextPlain("2", fonts.small, color_blue),
        Allignment.CENTER
    )
    b_color3 = Switch(
        (offset_x+175, offset_y+320), (45, 36), (3, 3, 3, 3),
        lambda: player.switch_color_profile(2),
        lambda: player.ship.color_profile == 2
    )
    b_color3.add_element(
        TextPlain("3", fonts.small, color_blue),
        Allignment.CENTER
    )
    b_color4 = Switch(
        (offset_x+230, offset_y+320), (45, 36), (3, 6, 6, 3),
        lambda: player.switch_color_profile(3),
        lambda: player.ship.color_profile == 3
    )
    b_color4.add_element(
        TextPlain("4", fonts.small, color_blue),
        Allignment.CENTER
    )

    # Switch - Auto-Shoot
    s_auto_shoot = Switch(
        (offset_x+65, offset_y+371), (210, 36), (6, 6, 6, 6),
        player.switch_auto_shoot,
        player.is_auto_shooting
    )
    s_auto_shoot.add_description(
        TextPlain("Automatically shoots current weapon", fonts.very_small, color_white)
    )
    s_auto_shoot.add_element(
        TextPlain("Auto-shoot", fonts.small, color_blue),
        Allignment.CENTER
    )
    # Switch - Auto-Heal
    s_auto_heal = Switch(
        (offset_x+65, offset_y+422), (210, 36), (6, 6, 6, 6),
        player.switch_auto_heal,
        player.is_auto_healing
    )
    s_auto_heal.add_description(
        TextPlain("Automatically heals if you have enough gold", fonts.very_small, color_white)
    )
    s_auto_heal.add_element(
        TextPlain("Auto-heal", fonts.small, color_blue),
        Allignment.CENTER
    )

    # Model switching
    b_model_left = Button(
        (offset_x+column_1, offset_y+65+row_height*1), (36, 36), (6, 3, 3, 6), 
        player_stats.switch_ship_model_to_previous
    )
    b_model_left.add_element(
        TextPlain("<", fonts.small, color_blue),
        Allignment.CENTER
    )

    b_model_right = Button(
        (offset_x+column_1+419, offset_y+65+row_height*1), (36, 36), (3, 6, 6, 3), 
        player_stats.switch_ship_model_to_next
    )
    b_model_right.add_element(
        TextPlain(">", fonts.small, color_blue),
        Allignment.CENTER
    )
    # Engine
    b_engine_speed = Button(
        (offset_x+column_1+419, offset_y+65+row_height*3), (36, 36), (3, 6, 6, 3),
        lambda: player.buy_upgrade(ShipUpgrade.ENGINE_SPEED),
        lambda: player.can_buy_upgrade(ShipUpgrade.ENGINE_SPEED)
    )
    b_engine_speed.set_outline_color(color_green)
    b_engine_speed.add_element(
        TextPlain("/\\", fonts.small, color_green),
        Allignment.CENTER
    )

    b_engine_acc = Button(
        (offset_x+column_1+419, offset_y+65+row_height*4), (36, 36), (3, 6, 6, 3),
        lambda: player.buy_upgrade(ShipUpgrade.ENGINE_ACCELERATION),
        lambda: player.can_buy_upgrade(ShipUpgrade.ENGINE_ACCELERATION)
    )
    b_engine_acc.set_outline_color(color_green)
    b_engine_acc.add_element(
        TextPlain("/\\", fonts.small, color_green),
        Allignment.CENTER
    )
    # Magnet
    b_magnet_rad = Button(
        (offset_x+column_1+419, offset_y+65+row_height*6), (36, 36), (3, 6, 6, 3),
        lambda: player.buy_upgrade(ShipUpgrade.MAGNET_RADIUS),
        lambda: player.can_buy_upgrade(ShipUpgrade.MAGNET_RADIUS)
    )
    b_magnet_rad.set_outline_color(color_green)
    b_magnet_rad.add_element(
        TextPlain("/\\", fonts.small, color_green),
        Allignment.CENTER
    )

    b_magnet_str = Button(
        (offset_x+column_1+419, offset_y+65+row_height*7), (36, 36), (3, 6, 6, 3),
        lambda: player.buy_upgrade(ShipUpgrade.MAGNET_STRENGTH),
        lambda: player.can_buy_upgrade(ShipUpgrade.MAGNET_STRENGTH)
    )
    b_magnet_str.set_outline_color(color_green)
    b_magnet_str.add_element(
        TextPlain("/\\", fonts.small, color_green),
        Allignment.CENTER
    )

    # Heal
    b_heal = Button(
        (offset_x+column_2+419, offset_y+65+row_height*1), (36, 36), (3, 6, 6, 3),
        player.buy_heal,
        player.can_heal
    )
    b_heal.set_outline_color(color_green)
    b_heal.add_element(
        TextPlain("/\\", fonts.small, color_green),
        Allignment.CENTER
    )
    # Upgrade weapons
    b_weapon_1_proj_up = Button(
        (offset_x+column_2+419, offset_y+65+row_height*3), (36, 36), (3, 6, 6, 3),
        lambda: player.buy_upgrade(ShipUpgrade.PLASMAGUN_PROJECTILES),
        lambda: player.can_buy_upgrade(ShipUpgrade.PLASMAGUN_PROJECTILES)
    )
    b_weapon_1_proj_up.set_outline_color(color_green)
    b_weapon_1_proj_up.add_element(
        TextPlain("/\\", fonts.small, color_green),
        Allignment.CENTER
    )
    b_weapon_1_cd_up = Button(
        (offset_x+column_2+419, offset_y+65+row_height*4), (36, 36), (3, 6, 6, 3),
        lambda: player.buy_upgrade(ShipUpgrade.PLASMAGUN_COOLDOWN),
        lambda: player.can_buy_upgrade(ShipUpgrade.PLASMAGUN_COOLDOWN)
    )
    b_weapon_1_cd_up.set_outline_color(color_green)
    b_weapon_1_cd_up.add_element(
        TextPlain("/\\", fonts.small, color_green),
        Allignment.CENTER
    )
    
    b_weapon_2_rad_up = Button(
        (offset_x+column_2+419, offset_y+65+row_height*6), (36, 36), (3, 6, 6, 3),
        lambda: player.buy_upgrade(ShipUpgrade.BOMBLAUNCHER_RADIUS),
        lambda: player.can_buy_upgrade(ShipUpgrade.BOMBLAUNCHER_RADIUS)
    )
    b_weapon_2_rad_up.set_outline_color(color_green)
    b_weapon_2_rad_up.add_element(
        TextPlain("/\\", fonts.small, color_green),
        Allignment.CENTER
    )
    b_weapon_2_fuse_up = Button(
        (offset_x+column_2+419, offset_y+65+row_height*7), (36, 36), (3, 6, 6, 3),
        lambda: player.buy_upgrade(ShipUpgrade.BOMBLAUNCHER_FUSE),
        lambda: player.can_buy_upgrade(ShipUpgrade.BOMBLAUNCHER_FUSE)
    )
    b_weapon_2_fuse_up.set_outline_color(color_green)
    b_weapon_2_fuse_up.add_element(
        TextPlain("/\\", fonts.small, color_green),
        Allignment.CENTER
    )

    # Ends the run and returns to the main menu
    b_end_run = Button(
        (offset_x+730, offset_y+600), (500, 72), (8, 8, 20, 20),
        game.handler_finish_round
    )
    b_end_run.make_weighted(ModKey.SHIFT)
    b_end_run.set_outline_color(color_red)
    b_end_run.set_fill_color(color_red_fill)
    b_end_run.add_description(
        TextPlain("SHIFT+Click to self-destruct", fonts.very_small, color_white)
    )
    b_end_run.add_element(
        TextPlain("SELF-DESTRUCT", fonts.big, color_red),
        Allignment.CENTER,
        nudge=(2, 0)
    )

    buttons.extend(
        [b_model_left, b_model_right, b_heal, b_magnet_rad, b_magnet_str,
            b_end_run, s_auto_shoot, b_weapon_1_cd_up, b_weapon_1_proj_up, b_weapon_2_fuse_up,
            b_weapon_2_rad_up, b_engine_speed, b_engine_acc, b_color1, b_color2,
            b_color3, b_color4, s_auto_heal]
    )

    return containers, buttons