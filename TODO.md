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
- [x] Change how max level upgrades are displayed (will need new buttons)
- [x] Revisit visible naming scheme for ship parts
- [ ] Rename and move UserInterface class (possibly to GameStateManager), rename GameStateManager to RoundStateManager
- [ ] Upgrade movement to properly handle turning of vectors, something is broken when turning without moving
- [ ] Update screenshots in README
- [ ] Add minimum asteroid price
- [ ] Increase alpha of background of the pause menu (might need new buttons)

IDEAS:
- [x] Graphics/color adjustments for the leaderboards for top places
- [ ] Add ship recolors (might need new buttons)
- [ ] More ship skins:
    - [x] UFO - will need new parts and 2 engines
- [ ] More weapons
- [ ] Show current timer/difficulty modifier
- [ ] Additional weapon upgrades:
    - [ ] Short fuse for the Bomb Launcher
    - [ ] Faster fire rate for Plasma Gun
- [ ] Profiles
- [ ] Saved name/ship settings (will need profiles)
- [ ] Bubble explosion vfx for bombs
- [ ] Add amount limit to certain asteroids (mainly Homing)

DISTANT/POSSIBLE IDEAS:
- [ ] Sounds
- [ ] Music
- [ ] Temporary boosts as loot
- [ ] Difficulty selection (speed of difficulty ramp-up, max amount of special asteroids)
- [ ] Persistent upgrades (will need profiles)
- [ ] Game modes (Classic with only normal asteroids and white/black graphics)
- [ ] Enemy ships/bosses
- [ ] Achievements (will need profiles)
- [ ] 2 leaderboards instead (one for points, one for gold)
- [ ] Better asteroid sprite