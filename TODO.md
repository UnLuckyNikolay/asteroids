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
- [x] Increase alpha of background of the pause menu
- [x] Revamp difficulty increase
- [x] Homing isn't affected by delta

IDEAS:
- [x] Graphics/color adjustments for the leaderboards for top places
- [x] Add auto-shoot switch
- [ ] Add ship recolors
- [ ] Additional ship skins:
    - [x] UFO - will need new parts and 2 engines
    - [ ] Classic/cartoon-ish rocket
- [ ] Additional weapons
- [ ] Additional ship upgrades:
    - [ ] Speed (might need ship vectors tweaked)
    - [ ] Rotation
- [x] Additional weapon upgrades:
    - [x] Short fuse for the Bomb Launcher
    - [x] Faster fire rate for Plasma Gun
- [ ] Additional cheats:
    - [ ] BIG cheat
- [ ] Profiles
    - [x] Player reset method
    - [x] Profile creation
    - [x] Player info
    - [ ] Saved unlocked ships (check ordered dict?)
    - [ ] New end screen
    - [ ] ???
    - [ ] Profit
- [ ] Show current timer/difficulty modifier
- [ ] Bubble explosion vfx (for bombs or better for player death)
- [x] Add amount limit to certain asteroids (mainly Homing)
- [x] Condition to activate cheat switches
- [x] Check how to save crash logs

DISTANT/POSSIBLE IDEAS:
- [ ] Save backups
- [ ] Sounds
- [ ] Music
- [ ] Temporary boosts as loot
- [ ] Difficulty selection (speed of difficulty ramp-up, max amount of special asteroids)
- [ ] Persistent upgrades (will need profiles)
- [ ] Game modes 
    - [ ] Classic with only normal asteroids and white/black graphics
    - [ ] Drift mode with no shooting and only homing asteroid (would need timer, might need difficulty revamp)
- [ ] Enemy ships/bosses
- [ ] Achievements (will need profiles)
- [ ] Better asteroid sprite