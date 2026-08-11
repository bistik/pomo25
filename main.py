from dotenv import load_dotenv
import argparse
from pomo import log_pomo, create_pomo_data_file
import os

def run_start(task: str, pomo_data_file: str) -> None:
    try:
        log_pomo(task, pomo_data_file)
    except FileNotFoundError:
        print("We cannot find your pomo data file")

def create_data_file(data_file: str) -> None:
    try:
        create_pomo_data_file(data_file)
        do_pomo = False
    except Exception as err:
        print("Error reading POMO_DATA_FILE in your environment, create .env file or set POMO_DATA_FILE environment variable")
        print(err)

def main() -> None:
    desc= f"""A script to record pomodoro sessions.
    
    To get started, set an environment variable POMO_DATA_FILE to the path of your jsonl datafile.
    Make sure the data file exists.
        $ touch data/pomo.jsonl
        $ POMO_DATA_FILE=data/pomo.jsonl pomo25
    
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
    do_pomo = True
    load_dotenv()
    data_file=os.environ.get('POMO_DATA_FILE')
    task="Default task"

    if args.task is not None:
        task=args.task
    if args.init:
        create_data_file(data_file)
    if not data_file:
        print("Unable to read POMO_DATA_FILE environment variable.")
        do_pomo=False
    if do_pomo:
        run_start(task, data_file)

if __name__ == "__main__":
    main()
