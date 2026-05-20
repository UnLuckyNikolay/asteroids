import pygame
from typing import Callable
from enum import Enum

from ui.font_builder import FontBuilder
from game_state_manager import GameStateManager
from sfx_manager import SFXManager

from ui.menus.enum_action import Action
from ui.menus.enum_menu import Menu
from ui.menus.base_menu import _MenuBase
from ui.elements.buttons import Button, Switch
# from ui.menus.addition_mini_settings import add_mini_settings_and_cheats
from ui.menus.menu_profile_selection import MenuProfileSelection
from ui.menus.menu_new_profile import MenuNewProfile
from ui.menus.menu_main import MenuMain
from ui.menus.menu_player_info import MenuPlayerInfo
from ui.menus.menu_name_edit import MenuNameEdit
from ui.menus.menu_leaderboard import MenuLeaderboard
from ui.menus.menu_hud import MenuHud
from ui.menus.menu_pause import MenuPause
from ui.menus.menu_round_end import MenuRoundEnd
# from ui.menus.menu_test import initialize_test_menu
from ui.menus.menu_debug import MenuDebug


class MenuManager(pygame.sprite.Sprite):
    layer = 100 # pyright: ignore
    def __init__(self, gsm : GameStateManager, sfxm : SFXManager):
        if hasattr(self, "containers"):
            super().__init__(self.containers) # pyright: ignore[reportAttributeAccessIssue]
        else:
            super().__init__()

        self.gsm = gsm
        self.sfxm = sfxm

        # Fonts
        font_path = "./_internal/fonts/anita-semi-square.normaali.ttf" #"../../fonts/anita-semi-square.normaali.ttf"
        self._fonts = FontBuilder(font_path)

        self._menu_classes : dict[Menu, Callable] = {
            Menu.PROFILE_SELECTION : (lambda: self._initialize_menu(MenuProfileSelection)),
            Menu.NEW_PROFILE : (lambda: self._initialize_menu(MenuNewProfile)),
            Menu.MAIN_MENU : (lambda: self._initialize_menu(MenuMain)),
            Menu.PLAYER_INFO : (lambda: self._initialize_menu(MenuPlayerInfo)),
            Menu.NAME_EDIT : (lambda: self._initialize_menu(MenuNameEdit)),
            Menu.LEADERBOARD : (lambda: self._initialize_menu(MenuLeaderboard)),
            Menu.HUD : (lambda: self._initialize_menu(MenuHud)),
            Menu.PAUSE_MENU : (lambda: self._initialize_menu(MenuPause)),
            Menu.ROUND_END : (lambda: self._initialize_menu(MenuRoundEnd)),

            Menu.RETURN : (lambda: self._menu_classes[self._last_menu_type]),
        }

        self._current_menu_type : Menu = Menu.PROFILE_SELECTION
        self._last_menu_type : Menu
        self._current_menu : _MenuBase
        self._hovered_button : Button | Switch | None = None
        self.initialize_current_menu()

        self._is_debug_menu_shown : bool = False
        self._debug_menu : MenuDebug = self._initialize_menu(MenuDebug)

        self._mapped_actions : dict[int, Action] = {
            41 : Action.MENU_BACK, # Escape
            49 : Action.MENU_CONFIRM, # Enter
            65 : Action.MENU_SWITCH_DEBUG, # F8

            44 : Action.PLAYER_SHOOT, # Space
            26 : Action.PLAYER_MOVEMENT_FORWARD, # W
            22 : Action.PLAYER_MOVEMENT_BACKWARD, # S
            7  : Action.PLAYER_MOVEMENT_RIGHT, # D
            4  : Action.PLAYER_MOVEMENT_LEFT, # A
            82 : Action.PLAYER_MOVEMENT_FORWARD_ALT, # ArrowUp
            81 : Action.PLAYER_MOVEMENT_BACKWARD_ALT, # ArrowDown
            79 : Action.PLAYER_MOVEMENT_RIGHT_ALT, # ArrowRight
            80 : Action.PLAYER_MOVEMENT_LEFT_ALT, # ArrowLeft

            30 : Action.PLAYER_WEAPON_ONE, # 1
            31 : Action.PLAYER_WEAPON_TWO, # 2
            32 : Action.PLAYER_WEAPON_THREE, # 3
            89 : Action.PLAYER_WEAPON_ONE_ALT, # K1
            90 : Action.PLAYER_WEAPON_TWO_ALT, # K2
            91 : Action.PLAYER_WEAPON_THREE_ALT, # K3
        }
    
    def draw(self, screen):
        self._current_menu.draw(screen)

        if self._hovered_button != None:
            self._hovered_button.draw_description(screen, self.gsm.screen_resolution)

        self._debug_menu.draw(screen)
    
    def check_keyboard_input_pressed(self, event_keydown : pygame.event.Event):
        if event_keydown.type != pygame.KEYDOWN:
            return
        
        # Check special presses
        self._current_menu.check_special_input(event_keydown)

        # Get Action
        try:
            action = self._mapped_actions[event_keydown.scancode]
        except KeyError:
            return

        # Button held
        self.gsm.held_actions[action] = True

        # Button pressed
        self._current_menu.check_action(action)
        self._debug_menu.check_action(action)

    def check_keyboard_input_unpressed(self, event_keyup : pygame.event.Event):
        if event_keyup.type != pygame.KEYUP:
            return
        
        # Get Action
        try:
            action = self._mapped_actions[event_keyup.scancode]
        except KeyError:
            return
        
        # Button unpressed
        self.gsm.held_actions[action] = False
    
    def switch_menu(self, menu : Menu):
        if menu == self._current_menu_type:
            return

        if menu == Menu.RETURN:
            self._last_menu_type, self._current_menu_type = self._current_menu_type, self._last_menu_type
        else:
            self._last_menu_type = self._current_menu_type
            self._current_menu_type = menu
            
        self._current_menu.kill()
        self.initialize_current_menu()
        self._hovered_button = None
        # self.check_hovered_button()

    def initialize_current_menu(self): ### REWORK LATER
        self._current_menu = self._menu_classes[self._current_menu_type]()
    
    def _initialize_menu(self, menu_class):
        return menu_class(self.gsm, self._fonts, self.switch_menu)

    def check_hovered_button(self):
        """
        Checks mouse position against all the buttons in the current menus and tries to run the button function.
        """

        position = pygame.mouse.get_pos()

        if self._hovered_button == None:

            # Check for a button hover
            for i in range(len(self._current_menu._buttons)):
                if self._current_menu._buttons[i].check_cursor_hover(position):
                    self._hovered_button = self._current_menu._buttons[i]
                    self._hovered_button.switch_hovered_state() # pyright: ignore[reportOptionalMemberAccess]
                    return
        
        # Check if cursor moved off the button
        elif not self._hovered_button.check_cursor_hover(position):
            self._hovered_button.switch_hovered_state()
            self._hovered_button = None

    def try_button_press(self):
        if self._hovered_button == None:
            return
        
        self._hovered_button.run_if_possible(self.sfxm)
        if self._hovered_button != None and self._hovered_button.is_active == False:
            self._hovered_button = None
