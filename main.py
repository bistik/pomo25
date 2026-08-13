import argparse
import os
from pathlib import Path

from dotenv import load_dotenv

from config import Config
from pomo import create_pomo_data_file, log_pomo

BASE_DIR = Path(__file__).resolve().parent

def run_start(config: Config) -> None:
    try:
        log_pomo(config)
    except FileNotFoundError:
        print("We cannot find your pomo data file {}".format(config["data_file"]))
        raise

def main() -> None:
    desc= """A script to record pomodoro sessions.

    To get started, set an environment variable POMO_DATA_FILE to the path of your jsonl datafile.
    Make sure the data file exists.
        $ touch data/pomo.jsonl
        $ POMO_DATA_FILE=data/pomo.jsonl

    Or create a .env file in the same directory as main.py, with contents:

    POMO_DATA_FILE=data/pomo.jsonl

    Then run: `pomo25`

    You can also create the data file with the -i or --init flag like so: `pomo25 -i`.
    You would still need to set the environment variable after creating the jsonl data file.

    With data file created and environment variable set. Just run `pomo25` to record a new pomodoro.
    To specify the name of the task do: `pomo25 -t "Baking a cake"`

    Wikipedia article on pomodoro technique - https://en.wikipedia.org/wiki/Pomodoro_Technique
    """
    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-t', '--task', help="Sets the name of task for the 25-minute pomodoro.")
    parser.add_argument('-i', '--init', action="store_true", help="Creates pomodoro data file if it doesn't exist yet. It assumes the directory of the data file exists. We do not create any subdirectory.")
    args = parser.parse_args()
    load_dotenv()
    config: Config = {
        "data_file": os.environ.get('POMO_DATA_FILE', ''),
        "date_format": os.environ.get('POMO_DATE_FMT', '%b %d, %Y %H:%M:%S %z'),
        "end_sound_file": str(BASE_DIR / 'assets' / 'break.wav'),
        "break_sound_file": str(BASE_DIR / 'assets' / 'break.wav'),
        "pomo_duration": int(os.environ.get('POMO_DURATION', '1500')),
        "break_duration": int(os.environ.get('POMO_BREAK_DURATION', '300')),
        "task_description": "Pomodoro default task",
        "play_sound": os.environ.get('POMO_SOUND_ON', '1').lower() in ('true', '1'),
        "debug": os.environ.get('POMO_DEBUG', '0').lower() in ('true', '1')
    }

    if config["debug"]:
        print(config)
        print()

    if args.task is not None:
        config["task_description"] = args.task
    if args.init:
        create_pomo_data_file(config["data_file"])
        print("Data file successully created {}".format(config["data_file"]))
    else:
        run_start(config)

if __name__ == "__main__":
    main()
