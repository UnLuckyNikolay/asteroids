# Asteroids

A classic game of Asteroids built using Pygame as a Boot.dev project and then enhanced with lots of additional features.

## Install and Run

1. Install [Python](https://www.python.org/downloads) 3.12 or higher.

2. Clone the repository:

    ```bash
	git clone https://github.com/UnLuckyNikolay/asteroids
    cd asteroids
	```

3. Activate venv and install requirements:

	```bash
	python3 -m venv ./venv
	source ./venv/bin/activate
	pip install -r ./requirements.txt
	```

4. Run:

	```bash 
	python3 main.pyw
	```

## Features

* Comprehensive movement mechanics
* Vector graphics for the UI, Player, Asteroids, animated Explosions and background stars
* Two weapons:
	* Plasma Gun - shoots balls of plasma
	* Bomb Launcher - leaves bombs that explode after a short interval
* Four types of asteroids:
	* Normal - 3 sizes, breaks into 2 smaller asteroids
	* Explosive - always big, breaks into 8 small asteroids in all directions
	* Golden - always small, increased speed and point value
	* Homing - always small, follows the player
* Multiple ship skins
* Loot that can be collected to upgrade the ship and weapons
* Difficulty increase with time
* Profiles that keep track of your stats
* Local leaderboards

## Controls

* `W`/`S` - Accelerate/decelerate
* `A`/`D` - Rotate
* `Space` - Shoot the current weapon
* `1` - Switch to the Plasma Gun
* `2` - Switch to the Bomb Launcher
* `Escape` - Open the Pause menu

## Screenshots (Outdated)

![Gameplay Showcase 1](https://imgur.com/LEnoEWm.png)

![Gameplay Showcase 2](https://imgur.com/ATW6zDc.png)

![Gameplay Showcase 3](https://imgur.com/NBmQYrB.png)

## Hints for secrets

<details> 
	<summary>Cheats</summary>
	There is a famous sequence that needs to be inputed while in the main menu.
</details>

<details> 
	<summary>Suspicious saucer-looking ship</summary>
	There were reports of a stange ship that can be barely seen from a certain menu.
</details>

## Technical Features

* Movement system that implements inertia and speed-up time for both moving and turning
* Game loop that uses delta and collision checks
* Point system that is used for building a local leaderboard (saved in JSON file)
* Configurable game settings via `constants.py` (including max fps, screen resolution, player stats, asteroid spawns and debug options)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.