import unittest
from pomo import countdown_pomo
from datetime import datetime, timedelta

class TestCrawl(unittest.TestCase):
    def test_countdown_pomo(self):
        fmt = '%b %d, %Y %H:%M:%S %z'
        expected = datetime.now().astimezone() + timedelta(seconds=5)
        actual = datetime.strptime(countdown_pomo(5, 'test', 0, play_sound=False), fmt)
        self.assertEqual(actual.strftime(fmt), expected.strftime(fmt), f"actual {actual}")
