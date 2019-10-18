import unittest
import json

from risk import Game


class TestGame(unittest.TestCase):
    def setUp(self):
        with open('./game_configs/test.json') as f:
            self.game = Game(json.load(f))

    def test_setup_works(self):
        print(self.game)
