import os, traceback, datetime, pygame

from config import *
from game import Game


def main():
    try:
        # Pygame initialization
        pygame.mixer.pre_init(
            frequency=44100,
            size=-16,
            channels=2,
            buffer=1024,
        )
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE, display=0)
        pygame.display.set_caption("Asteroids from Outer Space")

        # Game loop starts
        game = Game(screen)
        game.run()

    except Exception:
        # Creating a `crashlogs` folder
        crashlog_folder_path = "./crashlogs/"

        if not os.path.exists(crashlog_folder_path):
            print(f"Creating a `{crashlog_folder_path}` folder")
            os.makedirs(crashlog_folder_path)

        # Saving a crashlog
        crashlog = traceback.format_exc()
        time = str(datetime.datetime.now()).replace(" ", "_").replace(":", "-").replace(".", "-")
        crashlog_name = f"{crashlog_folder_path}crashlog_{time}"

        print(f"Saving crashlog to `{crashlog_name}`")
        print(crashlog)
        with open(crashlog_name, "w") as file:
            file.write(crashlog)

if __name__ == "__main__":
    main()
