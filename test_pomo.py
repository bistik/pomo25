import io
import unittest
from contextlib import redirect_stdout
from pomo import countdown_pomo, countdown_break
from datetime import datetime, timedelta

class TestCrawl(unittest.TestCase):
    def test_countdown_pomo(self):
        fmt = '%b %d, %Y %H:%M:%S %z'
        expected = datetime.now().astimezone() + timedelta(seconds=5)
        actual = datetime.strptime(countdown_pomo(5, 'test', 0, play_sound=False), fmt)
        self.assertEqual(actual.strftime(fmt), expected.strftime(fmt), f"actual {actual}")

    def test_countdown_break(self):
        f = io.StringIO()

        with redirect_stdout(f):
            countdown_break(3, play_sound=False)

        output = f.getvalue().strip()

        self.assertIn('Break time', output)
