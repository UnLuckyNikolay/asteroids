# Asteroids

A classic game of Asteroids built using Pygame as a Boot.dev project and then enhanced with additional features.

## Install and Run

1. Install [Python](https://www.python.org/downloads) 3.12 or higher.

2. Install Tkinter if needed:

	```bash
	sudo apt install python3-tk
	```

3. Clone the repository:

    ```bash
	git clone https://github.com/UnLuckyNikolay/asteroids
    cd asteroids
	```

4. Activate venv and install requirements:

	```bash
	python3 -m venv ./venv
	source ./venv/bin/activate
	pip install -r ./requirements.txt
	```

5. Run:

	```bash 
	python3 main.py
	```

## Features

* Comprehensive movement mechanics
* Vector graphics for the UI, Player, Asteroids, animated Explosions and background stars
* Two weapons:
	* Plasma Gun - shoots balls of plasma, has 3 levels, upgraded automatically based on the current score
	* Bomb Launcher - leaves bombs that explode after a short interval
* Four types of asteroids:
	* Normal - 3 sizes, breaks into 2 smaller asteroids
	* Explosive - always big, breaks into 8 small asteroids in all directions
	* Golden - always small, increased speed and point value
	* Homing - always small, follows the player
* Difficulty increase with time
* Configurable game settings via `constants.py` (including screen resolution, player stats, asteroid spawns and debug options)
* Local leaderboards

## Controls

* `W`/`S` - Accelerate/decelerate
* `A`/`D` - Rotate
* `Space` - Shoot the current weapon
* `1` - Switch to the Plasma Gun
* `2` - Switch to the Bomb Launcher

## Screenshots

![Gameplay Showcase 1](https://imgur.com/LEnoEWm.png)

![Gameplay Showcase 2](https://imgur.com/ATW6zDc.png)

![Gameplay Showcase 3](https://imgur.com/NBmQYrB.png)

## Technical Features

* Movement system that implements inertia and speed-up time for both moving and turning
* Game loop that uses delta and collision checks
* Point system that is used for upgrading the Plasma Gun at certain thresholds and for building a local leaderboard (saved in JSON file)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.