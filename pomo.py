import json
from datetime import datetime
import time
import sys
from nava import play
from typing import Final

POMO_SECONDS: Final = 1*15
BREAK_SECONDS: Final = 1*5
DATE_FMT: Final = "%b %d, %Y %H:%M:%S %z"

def clear_last_line():
    # Move cursor up 1 line (\033[1A) and clear the line (\033[2K)
    sys.stdout.write('\033[1A\033[2K')
    sys.stdout.flush()

def prompt_repeat() -> bool:
    user_input = input("\rDo you want to start a new pomodoro? [Y/n]: ").strip().lower()
    clear_last_line()
    if user_input == "" or user_input.startswith('y'):
        return True
    print("Bye!")
    return False

def countdown_pomo(seconds: int, task: str, count: int, date_fmt=DATE_FMT, play_sound=True) -> datetime:
    while seconds >= 0:
        mins, secs = divmod(seconds, 60)
        print(f"\rPomodoro #{count + 1} - '{task}' {mins:02d}:{secs:02d}".ljust(20), end="", flush=True)
        end = datetime.now().astimezone().strftime(date_fmt)
        time.sleep(1)
        seconds -= 1

    if play_sound:
        play("end.wav")

    return end

# We don't record the dates
def countdown_break(seconds: int, play_sound=True) -> None:
    while seconds >= 0:
        mins, secs = divmod(seconds, 60)
        print(f"\rBreak time: {mins:02d}:{secs:02d}".ljust(80), end="", flush=True)
        time.sleep(1)
        seconds -= 1

    if play_sound:
        play("break.wav")

def log_pomo(task: str, pomo_data_file: str) -> None:
    count_pomos = 0
    while True:
        data = {"task": task, "start": datetime.now().astimezone().strftime(DATE_FMT)}
        data["end"] = countdown_pomo(seconds=POMO_SECONDS, task=task, count=count_pomos)
        write_data(data, pomo_data_file)
        count_pomos += 1

        # 15 minutes break on every 3rd consecutive pomo
        if count_pomos > 0 and count_pomos % 3 == 0:
            countdown_break(BREAK_SECONDS * 3)
        else:
            countdown_break(BREAK_SECONDS)

        if prompt_repeat() == False:
            break

def write_data(data: dict, pomo_data_file: str) -> None:
    with open(pomo_data_file, "a") as file:
        json.dump(data, file)
        file.write("\n")

def create_pomo_data_file(file_path):
    with open(file_path, "a") as f:
        pass