from typing import Dict
import random
import math

import Cards
from Player import Player


class GameEngine:
    def __init__(self, name: str, game_id: str, players: Dict[str, Player], config: dict):
        self.BOARD_SIZE_X = 12
        self.BOARD_SIZE_Y = 9
        self.name = name
        self.game_id = game_id
        self.players = players
        self.config = config

        self.GOOD_PLAYER = "Solider"
        self.BAD_PLAYER = "Saboteur"

        self.ACTION_CARDS_TYPES_AMOUNT = 3

        self.INITIAL_TUNNEL_CARDS_AMOUNT = 44
        self.INITIAL_ACTION_CARDS_AMOUNT = 27
        self.INITIAL_CARDS_AMOUNT = self.INITIAL_TUNNEL_CARDS_AMOUNT + self.INITIAL_ACTION_CARDS_AMOUNT

        self.SABOTEUR_AMOUNT = self.__assign_saboteurs_amount()
        self.CARDS_PER_PLAYER_AMOUNT = self.__assign_card_amount_per_player()

        self.__assign_player_actions()
        self.__assign_player_roles()
        self.__assign_card_amount_per_player()

        self.cards = self.__create_card_deck()
        self.__assign_initial_cards_to_players()

        self.current_turn_num = 0
        self.turn = list(self.players.values())[self.current_turn_num].player_id

        self.round = 1
        self.ROUNDS_AMOUNT = 3

        self.EMPTY_CARD = Cards.TunnelCard(False, False, False, False, True, True, True, 'empty')
        self.board = self.__create_game_board()

    def __create_game_board(self):
        board = [[self.EMPTY_CARD for x in range(self.BOARD_SIZE_X)] for y in range(self.BOARD_SIZE_Y)]
        board[4][2] = Cards.TunnelCard(way_top=True,
                                       way_right=True,
                                       way_bottom=True,
                                       way_left=True,
                                       destructible=False,
                                       overwrite=False,
                                       empty=False,
                                       card_name="start")

        board[2][10] = Cards.TunnelCard(way_top=True,
                                       way_right=True,
                                       way_bottom=True,
                                       way_left=True,
                                       destructible=False,
                                       overwrite=False,
                                       empty=False,
                                       card_name="false")

        board[4][10] = Cards.TunnelCard(way_top=True,
                                        way_right=True,
                                        way_bottom=True,
                                        way_left=True,
                                        destructible=False,
                                        overwrite=False,
                                        empty=False,
                                        card_name="true")

        board[6][10] = Cards.TunnelCard(way_top=True,
                                        way_right=True,
                                        way_bottom=True,
                                        way_left=True,
                                        destructible=False,
                                        overwrite=False,
                                        empty=False,
                                        card_name="false")

        return board

    def __assign_player_actions(self):
        for player_id, player_obj in self.players.items():
            player_obj.add_actions(self.ACTION_CARDS_TYPES_AMOUNT)

    def __assign_player_roles(self):
        for player_id, player_obj in self.players.items():
            player_obj.player_role = self.GOOD_PLAYER

        saboteurs = []
        while len(saboteurs) < self.SABOTEUR_AMOUNT:
            player_id, player_obj = random.choice(list(self.players.items()))
            if player_id not in saboteurs:
                saboteurs.append(player_id)
                player_obj.player_role = self.BAD_PLAYER

    def __assign_saboteurs_amount(self):
        return math.floor(len(self.players) / 2.1)

    def __assign_card_amount_per_player(self):
        x = len(self.players)
        return 6 if 3 <= x <= 5 else 4 if 6 <= x <= 10 else 0

    def __create_card_deck(self):
        card_deck = []

        for i in range(self.INITIAL_TUNNEL_CARDS_AMOUNT):
            way_top = bool(random.getrandbits(1))
            way_right = bool(random.getrandbits(1))
            way_bottom = bool(random.getrandbits(1))
            way_left = bool(random.getrandbits(1))
            card_deck.append(Cards.TunnelCard(way_top=way_top,
                                              way_right=way_right,
                                              way_bottom=way_bottom,
                                              way_left=way_left,
                                              destructible=True,
                                              empty=False,
                                              overwrite=False))

        for i in range(self.INITIAL_ACTION_CARDS_AMOUNT):
            action_type = str(random.randint(0, self.ACTION_CARDS_TYPES_AMOUNT - 1))
            action_effect = bool(random.getrandbits(1))
            card_deck.append(Cards.ActionCard(action_type=action_type, is_positive_effect=action_effect))

        random.shuffle(card_deck)

        return card_deck

    def __assign_initial_cards_to_players(self):
        for player_id, player_obj in self.players.items():
            for i in range(self.CARDS_PER_PLAYER_AMOUNT):
                player_obj.player_cards.append(self.cards[-1])
                self.cards.pop()


class Game(GameEngine):
    def __init__(self, name: str, game_id: str, players: Dict[str, Player], config: dict):
        GameEngine.__init__(self, name=name, game_id=game_id, players=players, config=config)

    def end_turn(self):
        self.current_turn_num = self.current_turn_num + 1 if self.current_turn_num < len(self.players) else 0
        self.turn = list(self.players.values())[self.current_turn_num].player_id
        return f"turn ended, now its '{self.players[self.turn].player_name}' turn"

    def check_game_creation_rules(self):
        if len(self.players) < 3:
            return {"message_type": "error", "message_content": "not enough players"}
        elif len(self.players) > 10:
            return {"message_type": "error", "message_content": "too much players"}
        else:
            return {"message_type": "status", "message_content": "game can be created"}

    def check_game_tunnel_card_rules(self, card: Cards.TunnelCard, pos_x, pos_y):

        if type(pos_x) != int or type(pos_y) != int:
            return False
        if pos_x < 0 or pos_y < 0:
            return False
        if pos_x > len(self.board[0]) - 1 or pos_y > len(self.board) - 1:
            return False

        place = self.board[pos_y][pos_x]

        if place.empty is not True and card.overwrite is False:
            return False
        if place.empty is not True and place.destructible is False:
            return False

        test_card_top = None
        test_card_right = None
        test_card_bottom = None
        test_card_left = None

        if pos_y - 1 < 0:
            test_card_top = self.EMPTY_CARD
        if pos_y > len(self.board[0]) - 1:
            test_card_bottom = self.EMPTY_CARD
        if pos_x - 1 < 0:
            test_card_left = self.EMPTY_CARD
        if pos_x > len(self.board) - 1:
            test_card_right = self.EMPTY_CARD

        if test_card_top is None:
            test_card_top = self.board[pos_y - 1][pos_x]
        if test_card_right is None:
            test_card_right = self.board[pos_y][pos_x + 1]
        if test_card_bottom is None:
            test_card_bottom = self.board[pos_y + 1][pos_x]
        if test_card_left is None:
            test_card_left = self.board[pos_y][pos_x - 1]

        top_side = test_card_top
        right_side = test_card_right
        bottom_side = test_card_bottom
        left_side = test_card_left

        print(f"top: {top_side.symbol()}")
        print(f"right: {right_side.symbol()}")
        print(f"bottom: {bottom_side.symbol()}")
        print(f"left: {left_side.symbol()}")

        if card.way_top and not top_side.way_bottom and not top_side.empty:
            return False
        if card.way_right and not right_side.way_left and not right_side.empty:
            return False
        if card.way_bottom and not bottom_side.way_top and not bottom_side.empty:
            return False
        if card.way_left and not left_side.way_right and not left_side.empty:
            return False

        if not card.way_top and top_side.way_bottom and not top_side.empty:
            return False
        if not card.way_right and right_side.way_left and not right_side.empty:
            return False
        if not card.way_bottom and bottom_side.way_top and not bottom_side.empty:
            return False
        if not card.way_left and left_side.way_right and not left_side.empty:
            return False

        return True

    def info(self):
        info_str = f"uuid: {self.game_id}\n" \
                   f"name: {self.name}\n"

        info_str += f"board size: {self.BOARD_SIZE_X}x{self.BOARD_SIZE_Y}\n"

        info_str += f"cards: {self.INITIAL_CARDS_AMOUNT}\n"

        for card in self.cards:
            info_str += card.info() + '\n'

        info_str += f"board:\n[\n"
        for y in range(len(self.board)):
            info_str += '['
            for x in range(len(self.board[y])):
                info_str += f"[{self.board[y][x].symbol()}]"
            info_str += ']\n'

        info_str += f"]\n"

        info_str += f"players:\n[\n"

        for player in self.players:
            player = self.players[player]
            url_base = f"http://{self.config['host']}:{self.config['port']}/game"
            url_args = f"?game_id={self.game_id}&player_id={player.player_id}"

            info_str += f"name: {player.player_name}     id: {player.player_id}     url: {url_base + url_args}\n"

        info_str += "]\n"

        return info_str


