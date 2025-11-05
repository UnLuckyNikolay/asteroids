from enum import Enum

# New menus should be added to:
# .initialize_current_menu (+ new function in ./ui/menus/)
class Menu(Enum): # Remember not to name 2 the same ever fucking again
    PROFILE_SELECTION = "Profile selection"
    NEW_PROFILE = "New profile"
    MAIN_MENU = "Main Menu"
    PLAYER_INFO = "Player Info"
    NAME_EDIT = "Name edit"
    LEADERBOARD = "Leaderboard"
    HUD = "HUD"
    PAUSE_MENU = "Pause"
    ROUND_END = "Round End"
    TEST_MENU = "Test Menu"