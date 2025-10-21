For brainstorming

FIXES/TWEAKS:
- [x] AsteroidField doesn't scale with window size change. Asteroid deletion does tho
- [x] BombLauncher - Explosion isn't properly scaled with level
- [x] Check loot layer
- [x] Redo ship parts and engine (as classes) to add ability to draw different shapes and make it more readable:
    - [x] Have classes for parts and engines with draw methods, and lists of parts and engines to draw each from
    - [x] Add Line part
    - [x] Add Circle part
- [x] Check how to add support for different keyboard layouts
- [x] Tweak containers and buttons
    - [x] Press on button up instead of down
    - [x] Refactor containers and buttons
    - [x] Track hovered button
    - [x] Add descriptions while hovering
    - [x] Add weighted buttons
- [x] Change how max level upgrades are displayed
- [x] Revisit visible naming scheme for ship parts
- [x] Rename and move UserInterface class to GameStateManager, rename GameStateManager to RoundStateManager
- [ ] Upgrade movement to properly handle turning of vectors, something is broken when turning without moving
- [ ] Update screenshots in README
- [ ] Add minimum asteroid price
- [ ] Increase alpha of background of the pause menu
- [ ] Revamp difficulty increase

IDEAS:
- [x] Graphics/color adjustments for the leaderboards for top places
- [x] Add auto-shoot switch
- [ ] Add ship recolors
- [ ] More ship skins:
    - [x] UFO - will need new parts and 2 engines
- [ ] More weapons
- [ ] Additional ship upgrades:
    - [ ] Speed (might need ship vectors tweaked)
    - [ ] Rotation
- [ ] Additional weapon upgrades:
    - [ ] Short fuse for the Bomb Launcher
    - [ ] Faster fire rate for Plasma Gun
- [ ] Profiles
    - [ ] Player reset method
    - [ ] Profile creation
    - [ ] Player info
- [ ] Show current timer/difficulty modifier
- [ ] Bubble explosion vfx for bombs
- [ ] Add amount limit to certain asteroids (mainly Homing)
- [x] Condition to activate cheat switches

DISTANT/POSSIBLE IDEAS:
- [ ] Sounds
- [ ] Music
- [ ] Temporary boosts as loot
- [ ] Difficulty selection (speed of difficulty ramp-up, max amount of special asteroids)
- [ ] Persistent upgrades (will need profiles)
- [ ] Game modes 
    - [ ] Classic with only normal asteroids and white/black graphics
- [ ] Enemy ships/bosses
- [ ] Achievements (will need profiles)
- [ ] Better asteroid sprite