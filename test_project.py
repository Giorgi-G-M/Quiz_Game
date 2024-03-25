import unittest
from unittest.mock import patch
from project import next_difficulty, format_choices, get_timer_duration

class TestQuizGame(unittest.TestCase):
    
    def test_next_difficulty(self):
        self.assertEqual(next_difficulty("Easy"), "Medium")
        self.assertEqual(next_difficulty("Medium"), "Hard")
        self.assertEqual(next_difficulty("Hard"), "Hard")

    def test_format_choices(self):
        self.assertEqual(format_choices(['A', 'B', 'C']), ['A', 'B', 'C'])
        self.assertEqual(format_choices(None), ['No choices available'])

    def test_get_timer_duration(self):
        self.assertEqual(get_timer_duration("Easy"), 120)
        self.assertEqual(get_timer_duration("Medium"), 180)
        self.assertEqual(get_timer_duration("Hard"), 240)

if __name__ == '__main__':
    unittest.main()
