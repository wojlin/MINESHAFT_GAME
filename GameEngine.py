from typing import Dict
import random
import math

import Cards
from Player import Player


class GameEngine:
    def __init__(self, cells_x: int, cells_y: int, name: str, game_id: str, players: Dict[str, Player], config: dict):
        self.board_size_x = cells_x
        self.board_size_y = cells_y
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

        self.__assign_player_roles()
        self.__assign_card_amount_per_player()

        self.cards = self.__create_card_deck()

        self.current_turn_num = 0
        self.turn = list(self.players.values())[self.current_turn_num].player_id

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
                                              overwrite=False))

        for i in range(self.INITIAL_ACTION_CARDS_AMOUNT):
            action_type = str(random.randint(1, self.ACTION_CARDS_TYPES_AMOUNT))
            action_effect = bool(random.getrandbits(1))
            card_deck.append(Cards.ActionCard(action_type=action_type, is_positive_effect=action_effect))

        random.shuffle(card_deck)

        return card_deck


class Game(GameEngine):
    def __init__(self, cells_x: int, cells_y: int, name: str, game_id: str, players: Dict[str, Player], config: dict):
        GameEngine.__init__(self,
                            cells_x=cells_x,
                            cells_y=cells_y,
                            name=name,
                            game_id=game_id,
                            players=players,
                            config=config)

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

    def info(self):
        info_str = f"uuid: {self.game_id}\n" \
                   f"name: {self.name}\n"

        info_str += f"board size: {self.board_size_x}x{self.board_size_y}\n"

        info_str += f"cards: {self.INITIAL_CARDS_AMOUNT}\n"

        for card in self.cards:
            info_str += card.info() + '\n'

        info_str += f"players:\n[\n"

        for player in self.players:
            player = self.players[player]
            url_base = f"http://{self.config['host']}:{self.config['port']}/game"
            url_args = f"?game_id={self.game_id}&player_id={player.player_id}"

            info_str += f"name: {player.player_name}     id: {player.player_id}     url: {url_base + url_args}\n"

        info_str += "]\n"

        return info_str


