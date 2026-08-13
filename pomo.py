import json
import sys
import time
from datetime import datetime
from typing import TypedDict

from nava import play

from config import Config


class PomoData(TypedDict):
    start: str
    end: str
    task: str

def clear_last_line() -> None:
    # Move cursor up 1 line (\033[1A) and clear the line (\033[2K)
    sys.stdout.write('\033[1A\033[2K')
    sys.stdout.flush()

def prompt_repeat() -> bool:
    user_input = input("\rDo you want to start a new pomodoro? [Y/n]: ").strip().lower()
    clear_last_line()
    if user_input == "" or user_input.startswith('y'):
        return True
    print("\nBye!")
    return False

def countdown_pomo(config: Config, count: int) -> str:
    end = datetime.now().astimezone().strftime(config["date_format"])
    seconds = config["pomo_duration"]
    while seconds >= 0:
        mins, secs = divmod(seconds, 60)
        print(f"\rPomodoro #{count + 1} - '{config["task_description"]}' {mins:02d}:{secs:02d}".ljust(20), end="", flush=True)
        end = datetime.now().astimezone().strftime(config["date_format"])
        time.sleep(1)
        seconds -= 1

    if config["play_sound"]:
        play(config["end_sound_file"])

    return end

# We don't save the dates on break
def countdown_break(config: Config, multiplier=1) -> None:
    seconds = config["break_duration"] * multiplier
    while seconds >= 0:
        mins, secs = divmod(seconds, 60)
        print(f"\rBreak time: {mins:02d}:{secs:02d}".ljust(80), end="", flush=True)
        time.sleep(1)
        seconds -= 1

    if config["play_sound"]:
        play(config["break_sound_file"])

def log_pomo(config: Config) -> None:
    count_pomos = 0
    try:
        while True:
            pomo_data: PomoData = {
                "task": config["task_description"],
                "start": datetime.now().astimezone().strftime(config["date_format"]),
                "end": ""
            }
            try:
                pomo_data["end"] = countdown_pomo(config, count=count_pomos)
            except KeyboardInterrupt:
                pomo_data["end"] = datetime.now().astimezone().strftime(config["date_format"])
                raise
            finally:
                write_data(pomo_data, config)

            count_pomos += 1

            if count_pomos > 0 and count_pomos % 3 == 0:
                countdown_break(config, multiplier=3)
            else:
                countdown_break(config)

            if not prompt_repeat():
                break
    except KeyboardInterrupt:
        print("\nBye!")

def write_data(data: PomoData, config: Config) -> None:
    with open(config["data_file"], "a") as file:
        json.dump(data, file)
        file.write("\n")

def create_pomo_data_file(file_path: str) -> None:
    with open(file_path, "a"):
        pass
