import io
import unittest
from contextlib import redirect_stdout
from datetime import datetime, timedelta

from config import Config
from pomo import countdown_break, countdown_pomo


class TestCrawl(unittest.TestCase):
    def setUp(self):
        self.fmt: str = "%b %d, %Y %H:%M:%S %z"
        self.duration: int = 3
        self.config: Config = {
            "data_file": "test.jsonl",
            "date_format": self.fmt,
            "end_sound_file": 'assets/end.wav',
            "break_sound_file": 'assets/break.wav',
            "pomo_duration": self.duration,
            "break_duration": self.duration,
            "task_description": "Testing",
            "play_sound": False,
            "debug": False
        }

    def test_countdown_pomo(self):
        expected = datetime.now().astimezone() + timedelta(seconds=self.duration)
        actual = datetime.strptime(countdown_pomo(self.config, 0), self.fmt).astimezone()
        self.assertEqual(actual.strftime(self.fmt), expected.strftime(self.fmt), f"actual {actual}")

    def test_countdown_break(self):
        f = io.StringIO()
        with redirect_stdout(f):
            countdown_break(self.config)
        output = f.getvalue().strip()

        self.assertIn('Break time', output)
