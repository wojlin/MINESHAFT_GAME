import unittest
import colour_runner
from typing import Dict
import json
import uuid

import const
import GameEngine

with open('settings.json') as file:
    config = json.loads(file.read())


def create_game(players_amount: int):

    players: Dict[str, GameEngine.Player] = {}

    for x in range(players_amount):
        new_id = str(uuid.uuid4())
        players[new_id] = GameEngine.Player(player_name=f"player_{x}", player_id=new_id)

    game_id = str(uuid.uuid4())
    game = GameEngine.Game('test game', game_id, players, config)
    return game


class GameCreationTest(unittest.TestCase):

    def test_too_low(self):
        for x in range(-100, const.MIN_AMOUNT_OF_PLAYERS):
            self.assertRaises(const.InvalidMountOfPlayersException, create_game, players_amount=x)

    def test_correct_amount(self):
        for x in range(const.MIN_AMOUNT_OF_PLAYERS, const.MAX_AMOUNT_OF_PLAYERS + 1):
            game = create_game(players_amount=x)
            self.assertTrue(game.check_game_creation_rules, const.PLAYERS_MESSAGES.CORRECT_AMOUNT)

    def test_too_much(self):
        for x in range(const.MAX_AMOUNT_OF_PLAYERS + 1, 100):
            self.assertRaises(const.InvalidMountOfPlayersException, create_game, players_amount=x)






if __name__ == "__main__":
    unittest.main(verbosity=3)
