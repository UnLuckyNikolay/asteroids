from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from ui.elements.buttons import InputButton
    from ui.menus.enum_menu import Menu

from groups import GroupManager
from sfx_manager import SFXManager

### Managers

GM = GroupManager()
SFXM = SFXManager() # All sfx file paths are stored inside SFXManager

### Functions

# Added during MenuManager.__init__
SWITCH_MENU : Callable[[Menu], None]
SET_INPUT_BUTTON : Callable[[InputButton], None]
REINIT_CURRENT_MENU : Callable[[None], None]