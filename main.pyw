import os, traceback, datetime
from game import Game


def main():
    try:
        game = Game()
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
