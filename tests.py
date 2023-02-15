import unittest
from typing import Dict
import json
import uuid

import Cards
import const
import GameEngine

with open('settings.json') as file:
    config = json.loads(file.read())


def create_game(players_amount: int):

    players: Dict[str, GameEngine.Player] = {}

    for x in range(players_amount):
        new_id = str(uuid.uuid4())
        players[new_id] = GameEngine.Player(player_name=f"player_{x}", player_id=new_id, config=config)

    game_id = str(uuid.uuid4())
    game = GameEngine.Game('test game', game_id, players, config)
    return game


class PathfindingTest(unittest.TestCase):
    def test_close_correct(self):
        game = create_game(3)
        card = Cards.TunnelCard(True, True, True, True, False, False, False)
        pos_x = 3
        pos_y = 4
        self.assertTrue(game.check_game_tunnel_card_rules(card, pos_x, pos_y))

    def test_close_incorrect(self):
        game = create_game(3)
        card = Cards.TunnelCard(True, True, True, False, False, False, False)
        pos_x = 3
        pos_y = 4
        self.assertTrue(not game.check_game_tunnel_card_rules(card, pos_x, pos_y))

    def test_straight_far_correct(self):
        game = create_game(3)
        game.update_board(3, 4, Cards.TunnelCard(False, True, False, True, False, False, False))
        game.update_board(4, 4, Cards.TunnelCard(False, True, False, True, False, False, False))
        game.update_board(5, 4, Cards.TunnelCard(False, True, False, True, False, False, False))
        game.update_board(6, 4, Cards.TunnelCard(False, True, False, True, False, False, False))
        game.update_board(7, 4, Cards.TunnelCard(False, True, False, True, False, False, False))

        card = Cards.TunnelCard(True, True, True, True, False, False, False)
        pos_x = 8
        pos_y = 4
        self.assertTrue(game.check_game_tunnel_card_rules(card, pos_x, pos_y))

    def test_straight_far_incorrect(self):
        game = create_game(3)
        game.update_board(3, 4, Cards.TunnelCard(False, True, False, True, False, False, False))
        game.update_board(4, 4, Cards.TunnelCard(False, True, False, True, False, False, False))
        game.update_board(6, 4, Cards.TunnelCard(False, True, False, True, False, False, False))
        game.update_board(7, 4, Cards.TunnelCard(False, True, False, True, False, False, False))

        card = Cards.TunnelCard(True, True, True, True, False, False, False)
        pos_x = 8
        pos_y = 4
        self.assertTrue(not game.check_game_tunnel_card_rules(card, pos_x, pos_y))


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
