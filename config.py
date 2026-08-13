from typing import TypedDict


class Config(TypedDict):
    data_file: str
    date_format: str
    end_sound_file: str
    break_sound_file: str
    pomo_duration: int
    break_duration: int
    task_description: str
    play_sound: bool
    debug: bool
